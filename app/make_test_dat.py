import pandas as pd 
import random
import uuid
from datetime import datetime, timedelta

# 1. 기초 데이터 설정 (서버에 이미 등록된 제조사명이 아니어도 서버가 자동으로 생성함)
manufacturers = ["대동", "LS엠트론", "TYM", "John Deere", "Kubota", "Fendt", "Massey Ferguson"]

data = []
# 중복 방지를 위한 시드값
unique_suffix = datetime.now().strftime("%H%M")

for i in range(1, 101):
    m_name = random.choice(manufacturers)
    
    # 날짜: 출고일과 도착일 설정
    release_dt = datetime.now() - timedelta(days=random.randint(10, 500))
    arrival_dt = release_dt + timedelta(days=random.randint(7, 30))

    # 위치별 관세율 설정 (프론트엔드 계산 로직과 일치)
    loc = random.choice(["KOREA", "SHIPPING", "INDONESIA", "VIETNAM"])
    if loc == "INDONESIA": t_rate = 15.0
    elif loc == "VIETNAM": t_rate = 10.0
    else: t_rate = 0.0

    # 서버 api/tractors.py의 row.get() 메서드가 찾는 정확한 소문자 필드명
    data.append({
        "serial_number": f"SN-2025-{unique_suffix}-{i:04d}", # 시리얼 번호 중복 방지
        "model": f"{m_name[:2]}-{random.randint(100, 900)}X",
        "manufacturer_name": m_name,       # 서버에서 제조사 조회의 기준
        "horsepower": random.choice([45, 65, 100, 250]),
        "base_price": float(random.randint(2000, 7500) * 10000),
        "tax_rate": t_rate,
        "location": loc,
        "status": random.choice(["STOCK", "EXPORT_READY", "CLEARANCE", "DELIVERED"]),
        "release_date": release_dt.strftime("%Y-%m-%d"),
        "arrival_date": arrival_dt.strftime("%Y-%m-%d")
    })

# 2. 엑셀 파일 저장
df = pd.DataFrame(data)
file_name = "tractor_scm_upload_final.xlsx"

# index=False는 반드시 유지 (서버에서 컬럼 밀림 방지)
df.to_excel(file_name, index=False)

print(f"✅ 생성 완료: {file_name}")
print(f"📌 총 {len(df)}대의 트랙터 데이터가 서버 규격에 맞게 준비되었습니다.")