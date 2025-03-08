import requests
import json
import streamlit as st
from typing import Dict, Any, Optional, Tuple

class APIHandler:
    @staticmethod
    def handle_api_request(url: str, method: str, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        API 요청을 처리하는 메서드
        
        Args:
            url (str): API 엔드포인트 URL
            method (str): HTTP 메소드 (GET 또는 POST)
            data (Dict[str, Any]): 요청 데이터
            
        Returns:
            Tuple[Optional[Dict[str, Any]], Optional[str]]: (응답 데이터, 에러 메시지)
        """
        try:
            headers = {'Content-Type': 'application/json'}
            
            if method == "GET":
                response = requests.get(url, params=data, headers=headers)
            else:  # POST
                response = requests.post(url, json=data, headers=headers)
            
            response.raise_for_status()  # HTTP 에러 체크
            
            return response.json(), None
            
        except requests.exceptions.RequestException as e:
            error_msg = f"API 요청 실패: {str(e)}"
            return None, error_msg
        except json.JSONDecodeError:
            error_msg = "응답을 JSON으로 파싱할 수 없습니다."
            return None, error_msg
        except Exception as e:
            error_msg = f"예상치 못한 에러 발생: {str(e)}"
            return None, error_msg
