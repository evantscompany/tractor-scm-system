import pandas as pd
import random

# 1. 주신 파일에서 시리얼 번호와 로케이션 추출
df_tractor = pd.read_excel('tractor_scm_upload_final.xlsx')
serials = df_tractor['serial_number'].tolist()
locations = df_tractor['location'].tolist()

# 2. 랜덤 데이터 풀 정의
crops = {
    'KOREA': ['벼', '사과', '배추', '인삼'],
    'VIETNAM': ['커피', '쌀', '고무', '용과'],
    'INDONESIA': ['팜유', '카카오', '옥수수', '카사바'],
    'SHIPPING': ['미정']
}

names_ko = ['김철수', '이영희', '박지성', '최민수', '정우성', '강호동']
names_vn = ['Nguyen Van A', 'Tran Thi B', 'Le Van C', 'Pham Van D']
names_id = ['Budi', 'Siti', 'Agus', 'Dewi', 'Eko']

# 3. 데이터 생성
farmer_data = []
for sn, loc in zip(serials, locations):
    if loc == 'KOREA':
        name = random.choice(names_ko) + str(random.randint(1, 99))
        phone = f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        crop = random.choice(crops['KOREA'])
    elif loc == 'VIETNAM':
        name = random.choice(names_vn)
        phone = f"+84-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        crop = random.choice(crops['VIETNAM'])
    else:
        name = random.choice(names_id)
        phone = f"+62-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        crop = random.choice(crops['INDONESIA'])
    
    farmer_data.append({
        'name': name,
        'phone': phone,
        'address': f"{loc} 지역 상세 주소",
        'main_crop': crop,
        'land_size': random.randint(1000, 5000), # 평 또는 sqm
        'tractor_sn': sn, # 매칭 키
        'joined_at': '2025-01-01'
    })

df_farmers = pd.DataFrame(farmer_data)
df_farmers.to_excel('random_farmers_master.xlsx', index=False)