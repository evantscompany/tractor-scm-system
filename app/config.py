from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 파일 기반의 SQLite 데이터베이스 사용
DATABASE_URL = "sqlite:///./tractor.db"

# 2. SQLite 엔진 생성 및 스레드 체크 비활성화
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# DB 세션 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()