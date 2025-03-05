import streamlit as st
import os
from utils.storage import ensure_data_dir
from st_pages import add_page_title, get_nav_from_toml

# 초기 설정
def initialize():
    # 앱 설정
    st.set_page_config(
        page_title="Gemini 프롬프트 관리 시스템",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 데이터 파일 초기화
    ensure_data_dir()
    
    # 세션 상태 초기화
    if "api_url" not in st.session_state:
        st.session_state.api_url = "http://www.test.ai.com/cam"

# 메인 앱
def main():
    initialize()
    
    # 페이지 네비게이션 설정
    nav = get_nav_from_toml(".streamlit/pages.toml")
    pg = st.navigation(nav)
    add_page_title(pg)
    
    pg.run()

if __name__ == "__main__":
    main()
