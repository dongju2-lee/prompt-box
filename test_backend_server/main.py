from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn
from typing import List

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/single")
async def process_image(image: UploadFile = File(...)):
    """이미지를 받아서 랜덤한 음식 3개를 반환합니다."""
    food_list = ["콜라", "햄버거", "머스타드 소스", "치즈", "계란"]
    selected_foods = random.sample(food_list, 3)
    
    return [{"food_name": food} for food in selected_foods]

@app.get("/user/info")
async def get_user_info():
    """랜덤한 나이와 주소를 반환합니다."""
    age = random.randint(10, 70)
    address = random.choice(["서울", "김포", "일산"])
    
    return {
        "age": str(age),
        "address": address
    }

@app.get("/quota")
async def get_quota():
    """랜덤한 사용량을 반환합니다."""
    used = random.randint(0, 100)
    return {"used": str(used)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9001, reload=True) 