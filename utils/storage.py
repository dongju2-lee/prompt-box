import os
import json
from datetime import datetime
import uuid

# 데이터 경로를 현재 디렉토리로 설정
DATA_PATH = "./app_data"  # 현재 디렉토리
PROMPTS_FILE = os.path.join(DATA_PATH, "prompts.json")
HISTORY_FILE = os.path.join(DATA_PATH, "history.json")
ENDPOINTS_FILE = os.path.join(DATA_PATH, "endpoints.json")

def ensure_data_dir():
    """데이터 디렉토리와 필요한 파일들이 존재하는지 확인하고 없으면 생성"""
    # 데이터 디렉토리 확인
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    
    # 프롬프트 파일 초기화
    if not os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, "w") as f:
            json.dump([], f)
    
    # 이력 파일 초기화
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)
    
    # 엔드포인트 파일 초기화
    if not os.path.exists(ENDPOINTS_FILE):
        with open(ENDPOINTS_FILE, "w") as f:
            json.dump([], f)

def load_prompts():
    """저장된 프롬프트 목록 로드"""
    try:
        with open(PROMPTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 파일이 없거나 손상된 경우 빈 리스트 반환
        return []

def save_prompts(prompts):
    """프롬프트 목록 저장"""
    with open(PROMPTS_FILE, "w") as f:
        json.dump(prompts, f, indent=4)

def load_history():
    """API 호출 이력 로드"""
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 파일이 없거나 손상된 경우 빈 리스트 반환
        return []

def save_history_entry(prompt, image_path, response, status):
    """새로운 API 호출 이력 저장"""
    history = load_history()
    
    # 새 이력 생성
    entry_id = str(uuid.uuid4())
    history_entry = {
        "id": entry_id,
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "image_path": image_path,
        "response": response,
        "status": status
    }
    
    # 이력에 추가
    history.append(history_entry)
    
    # 파일에 저장
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
    
    return entry_id

def get_history_by_id(history_id):
    """ID로 특정 이력 조회"""
    history = load_history()
    return next((h for h in history if h["id"] == history_id), None)

def add_history_to_prompt(prompt_id, history_id):
    """프롬프트에 이력 ID 추가"""
    prompts = load_prompts()
    for prompt in prompts:
        if prompt["id"] == prompt_id:
            if "related_history" not in prompt:
                prompt["related_history"] = []
            prompt["related_history"].append(history_id)
            save_prompts(prompts)
            return True
    return False

def load_endpoints():
    """저장된 엔드포인트 목록 로드"""
    try:
        with open(ENDPOINTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_endpoint(url):
    """새로운 엔드포인트 추가"""
    endpoints = load_endpoints()
    
    # 중복 검사
    if url in endpoints:
        return False
    
    endpoints.append(url)
    with open(ENDPOINTS_FILE, "w") as f:
        json.dump(endpoints, f, indent=4)
    return True

def delete_endpoint(url):
    """엔드포인트 삭제"""
    endpoints = load_endpoints()
    if url in endpoints:
        endpoints.remove(url)
        with open(ENDPOINTS_FILE, "w") as f:
            json.dump(endpoints, f, indent=4)
        return True
    return False
