import streamlit as st
import requests
import json
import time
import hashlib
import uuid
from datetime import datetime
from utils.storage import load_prompts, save_prompts, save_history_entry

class TesterPage:
    def __init__(self):
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if "prompt_save_status" not in st.session_state:
            st.session_state.prompt_save_status = "save"
        if "api_request_status" not in st.session_state:
            st.session_state.api_request_status = {"text": "send", "color": "primary", "result": None}
    
    def get_prompt_hash(self, prompt_text):
        """프롬프트 텍스트의 해시값을 계산하여 중복 확인에 사용"""
        return hashlib.md5(prompt_text.encode()).hexdigest()
    
    def render_api_settings(self):
        """API 설정 섹션 렌더링"""
        st.write("**현재 API 서버 주소:**")
        st.code(st.session_state.api_url)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            url_path = st.text_input("URL 경로", value="/single/cam", 
                                   help="API 서버 주소 뒤에 추가될 경로")
        with col2:
            http_method = st.selectbox("HTTP 메소드", options=["GET", "POST"])
        
        full_url = f"{st.session_state.api_url.rstrip('/')}{url_path}"
        st.write("**요청 URL:**", full_url)
        return full_url, http_method
    
    def render_prompt_section(self):
        """프롬프트 섹션 렌더링"""
        st.subheader("프롬프트")
        saved_prompts = load_prompts()
        prompt_names = ["직접 입력"] + [p["name"] for p in saved_prompts]
        selected_prompt_name = st.selectbox("프롬프트 선택", prompt_names)
        
        save_col, text_col = st.columns([1, 5])
        
        with save_col:
            button_color = "primary" if st.session_state.prompt_save_status == "save" else "secondary"
            save_clicked = st.button(st.session_state.prompt_save_status, type=button_color, key="save_prompt_btn")
        
        with text_col:
            prompt = self.handle_prompt_input(selected_prompt_name, saved_prompts)
        
        if save_clicked:
            self.handle_prompt_save(prompt, saved_prompts)
            
        return prompt
    
    def handle_prompt_input(self, selected_prompt_name, saved_prompts):
        """프롬프트 입력 처리"""
        if selected_prompt_name == "직접 입력":
            prompt = st.text_area("프롬프트 입력", height=150, key="prompt_input")
            if "last_prompt" not in st.session_state or st.session_state.last_prompt != prompt:
                st.session_state.prompt_save_status = "save"
                st.session_state.last_prompt = prompt
        else:
            selected_prompt = next((p for p in saved_prompts if p["name"] == selected_prompt_name), None)
            if selected_prompt:
                prompt = st.text_area("프롬프트 입력", value=selected_prompt["content"], height=150, key="prompt_input")
                if "last_prompt" not in st.session_state or st.session_state.last_prompt != prompt:
                    st.session_state.prompt_save_status = "already"
                    st.session_state.last_prompt = prompt
            else:
                prompt = st.text_area("프롬프트 입력", height=150, key="prompt_input")
        return prompt
    
    def handle_prompt_save(self, prompt, saved_prompts):
        """프롬프트 저장 처리"""
        if not prompt:
            st.error("저장할 프롬프트를 입력해주세요.")
            return
        
        with st.spinner("프롬프트 저장 중..."):
            prompt_hash = self.get_prompt_hash(prompt)
            if any(self.get_prompt_hash(p["content"]) == prompt_hash for p in saved_prompts):
                st.session_state.prompt_save_status = "already"
                st.warning("이미 동일한 내용의 프롬프트가 저장되어 있습니다.")
                return
            
            existing_numbers = [int(p["name"].split("#")[1]) if "#" in p["name"] else 0 for p in saved_prompts]
            next_number = max(existing_numbers) + 1 if existing_numbers else 1
            
            new_prompt = {
                "id": str(uuid.uuid4()),
                "name": f"Prompt #{next_number}",
                "description": f"자동 저장된 프롬프트 #{next_number}",
                "content": prompt,
                "created_at": datetime.now().isoformat(),
                "related_history": []
            }
            
            saved_prompts.append(new_prompt)
            save_prompts(saved_prompts)
            
            time.sleep(0.5)
            st.session_state.prompt_save_status = "saved"
            st.success(f"프롬프트가 '{new_prompt['name']}'으로 저장되었습니다.")
    
    def render_data_input(self):
        """데이터 입력 섹션 렌더링"""
        st.subheader("데이터 입력")
        data_type = st.radio("데이터 유형 선택", ["이미지", "문자열", "JSON"], horizontal=True)
        
        data = None
        if data_type == "이미지":
            uploaded_file = st.file_uploader("이미지 파일 업로드", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
                data = uploaded_file
        elif data_type == "문자열":
            data = st.text_area("문자열 입력", height=100)
        else:  # JSON
            json_text = st.text_area("JSON 입력", value="{}", height=150)
            try:
                if json_text:
                    data = json.loads(json_text)
            except json.JSONDecodeError:
                st.error("유효한 JSON 형식이 아닙니다.")
        
        return data_type, data
    
    def handle_api_request(self, full_url, http_method, prompt, data_type, data):
        """API 요청 처리"""
        if not prompt:
            st.error("프롬프트를 입력해주세요.")
            return
        
        try:
            response = self.send_api_request(full_url, http_method, prompt, data_type, data)
            self.handle_api_response(response, prompt, data_type, data)
        except Exception as e:
            self.handle_api_error(e, prompt, data_type, data)
    
    def send_api_request(self, full_url, http_method, prompt, data_type, data):
        """API 요청 전송"""
        if http_method == "POST":
            if data_type == "이미지":
                files = {'image': data}
                data = {'prompt': prompt}
                return requests.post(full_url, files=files, data=data)
            else:
                request_data = {'prompt': prompt}
                if data_type == "문자열":
                    request_data['text'] = data
                else:  # JSON
                    request_data['data'] = data
                return requests.post(full_url, json=request_data)
        else:  # GET
            params = {'prompt': prompt}
            if data_type == "문자열":
                params['text'] = data
            elif data_type == "JSON":
                params.update(data)
            return requests.get(full_url, params=params)
    
    def render(self):
        """페이지 전체 렌더링"""
        full_url, http_method = self.render_api_settings()
        prompt = self.render_prompt_section()
        data_type, data = self.render_data_input()
        
        # API 요청 버튼 및 상태 표시
        status_col, send_col = st.columns([1, 5])
        with send_col:
            send_clicked = st.button(
                st.session_state.api_request_status["text"],
                type=st.session_state.api_request_status["color"],
                key="send_request_btn"
            )
        
        with status_col:
            if st.session_state.api_request_status["result"] == "OK":
                st.success("OK")
            elif st.session_state.api_request_status["result"] == "FAIL":
                st.error("FAIL")
        
        if send_clicked:
            self.handle_api_request(full_url, http_method, prompt, data_type, data)

# 전역 인스턴스 생성
page = TesterPage()
# 페이지 렌더링
page.render()