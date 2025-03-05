import streamlit as st
from utils.storage import save_endpoint, load_endpoints, delete_endpoint
import time  # 파일 상단에 추가

class SettingPage:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if "show_endpoints" not in st.session_state:
            st.session_state.show_endpoints = False
    
    def render_endpoint_input(self):
        """엔드포인트 입력 섹션"""
        st.header("API 엔드포인트 관리")
        
        # container를 사용하여 입력 필드와 버튼을 감싸기
        with st.container():
            # 더 나은 정렬을 위해 columns 비율 조정
            col1, col2 = st.columns([4, 1])
            
            with col1:
                new_endpoint = st.text_input(
                    "API 엔드포인트 URL",
                    placeholder="https://api.example.com",
                    label_visibility="collapsed"  # 레이블 숨기기
                )
            
            with col2:
                # 버튼의 위치를 조정하기 위해 빈 공간 추가
                st.write("")  # 텍스트 입력 필드의 레이블 공간만큼 오프셋 추가
                if st.button("등록", use_container_width=True):
                    if not new_endpoint:
                        st.error("URL을 입력해주세요.")
                    else:
                        if save_endpoint(new_endpoint):
                            success_message = st.success("엔드포인트가 등록되었습니다.")
                            time.sleep(2)  # 2초 동안 메시지 표시
                            success_message.empty()  # 메시지 제거
                            st.rerun()
                        else:
                            st.warning("이미 등록된 엔드포인트입니다.")
    
    def render_endpoint_list(self):
        """엔드포인트 목록 표시 섹션"""
        # 전체 확인 토글 버튼
        if st.button(
            "엔드포인트 목록 전체 확인" if not st.session_state.show_endpoints else "엔드포인트 목록 닫기",
            use_container_width=True
        ):
            st.session_state.show_endpoints = not st.session_state.show_endpoints
            st.rerun()  # 상태 변경 후 즉시 페이지 리로드
        
        # 엔드포인트 목록 표시
        if st.session_state.show_endpoints:
            endpoints = load_endpoints()
            if not endpoints:
                st.info("등록된 엔드포인트가 없습니다.")
            else:
                st.subheader("등록된 엔드포인트 목록")
                for endpoint in endpoints:
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.code(endpoint)
                    with col2:
                        if st.button("삭제", key=f"del_{endpoint}", use_container_width=True):
                            if delete_endpoint(endpoint):
                                st.success("엔드포인트가 삭제되었습니다.")
                                st.rerun()
    
    def render(self):
        """페이지 전체 렌더링"""
        self.render_endpoint_input()
        st.markdown("---")
        self.render_endpoint_list()

# 전역 인스턴스 생성
page = SettingPage()
# 페이지 렌더링
page.render()