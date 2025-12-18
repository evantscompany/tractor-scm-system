from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. DB 설정 및 모델 로드
from app.config import engine, Base
# 중요: 테이블 생성을 위해 모델을 반드시 임포트해야 합니다.
from app.models.tractor import Tractor
from app.models.manufacturer import Manufacturer
from app. models.farmer import Farmer #추가
from app.models.history import MaintenanceHistory #추가


# 2. API 라우터 임포트 (이름 충돌을 피하기 위해 별칭 사용)
from app.api import tractor as tractor_api
from app.api import manufacturer as manufacturer_api
from app.api import farmer as farmer_api
from app.api import history as history_api
from app.api import upload as upload_api

# 3. 서버 실행 시 DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tractor SCM System")

# --- CORS 설정 ---
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. 라우터 등록 (위에서 정한 별칭 'tractor_api' 사용)
app.include_router(tractor_api.router)
app.include_router(manufacturer_api.router)
app.include_router(farmer_api.router)
app.include_router(history_api.router)
app.include_router(upload_api.router) # 추가


@app.get("/")
def root():
    return {"message": "Tractor SCM API is running"}