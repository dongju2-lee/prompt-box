import streamlit as st
import os
from utils.storage import load_endpoints

class StartFrontPage:
    def __init__(self):
        self.data_path = "./app_data"
    
    def render(self):
        self.show_title()
        self.show_welcome_message()
        self.show_announcements()
        self.show_system_status()
    
    def show_title(self):
        st.title("🤖 Gemini 프롬프트 관리 시스템")
    
    def show_welcome_message(self):
        st.header("환영합니다!")
        st.markdown("""
        ### 시스템 소개

        이 시스템은 Gemini API 호출을 테스트하고, 프롬프트를 관리하며, 호출 이력을 추적할 수 있는 도구입니다.

        ### 주요 기능

        - **🧪 API 테스트**: Gemini API에 다양한 프롬프트와 데이터를 전송하고 결과를 확인
        - **📝 프롬프트 이력**: 효과적인 프롬프트를 저장하고 관리
        - **🔬 실험실**: 다양한 실험 결과와 데이터 이력을 확인
        - **⚙️ 환경설정**: API 서버 URL 등 시스템 설정 관리

        ### 시작하기

        왼쪽 사이드바에서 원하는 기능을 선택하여 시작하세요.
        """)
    
    def show_announcements(self):
        st.subheader("📢 공지사항")
        with st.container():
            st.info("""
            **최신 업데이트 (2025-03-05)**
            
            - 다양한 데이터 유형(이미지, 문자열, JSON) 지원 추가
            - 프롬프트 저장 및 관리 기능 개선
            - API 호출 이력 추적 시스템 구현
            
            문의사항이 있으시면 관리자에게 연락해주세요.
            """)
    
    def show_system_status(self):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("등록된 API Endpoint 정보")
            
            # 엔드포인트 목록 불러오기
            endpoints = load_endpoints()
            
            # 엔드포인트 수와 목록 보기 버튼을 한 줄에 배치
            status_col, button_col = st.columns([3, 1])
            with status_col:
                st.write(f"**등록된 엔드포인트:** {len(endpoints)}개")
            
            with button_col:
                if "show_endpoint_list" not in st.session_state:
                    st.session_state.show_endpoint_list = False
                    
                if st.button(
                    "list 닫기" if st.session_state.show_endpoint_list else "list 보기",
                    use_container_width=True
                ):
                    st.session_state.show_endpoint_list = not st.session_state.show_endpoint_list
                    st.rerun()
            
            # 엔드포인트 목록 표시
            if st.session_state.show_endpoint_list:
                if endpoints:
                    for endpoint in endpoints:
                        st.code(endpoint)
                else:
                    st.warning("등록된 API 엔드포인트가 없습니다.")
                    if st.button("환경설정에서 등록하기", type="primary"):
                        st.switch_page("pages/setting.py")

        with col2:
            st.subheader("데이터 저장 위치")
            data_path = "./app_data"  # 앱 데이터 디렉토리
            st.code(f"데이터 경로: {os.path.abspath(data_path)}")
    

# 전역 인스턴스 생성
page = StartFrontPage()

# Streamlit이 페이지를 로드할 때 자동으로 실행되는 코드
page.render()