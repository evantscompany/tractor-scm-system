# 🚜 트랙터 통합 관리 시스템 (Phase 2) 히스토리

## 📌 현재 진행 상황 (2025-12-17 기준)
- [x] Phase 1: 기본 재고 관리 시스템 완성 (FastAPI + React)
- [x] Git 초기화 및 GitHub 원격 저장소 연결 완료 (`main`, `v1-origin`, `develop`)
- [ ] Phase 2: CRM(농민) 및 생애주기 관리 설계 중 (현재 단계)

## 🏗️ 시스템 아키텍처 (Key Points)
- **Backend**: FastAPI (api/crud/models/schemas 분리 구조)
- **Frontend**: React (Vite)
- **Database**: SQLite (SQLAlchemy ORM 사용)
- **Branch 전략**: 
  - `main`: 배포용
  - `v1-origin`: Phase 1 박제본 (안전장치)
  - `develop`: 신규 기능 개발용 (현재 작업 브랜치)

## 🛠️ 다음 설계 목표 (Todo List)
1. **Models 확장**:
   - `Farmer`: 인적사항, 토지정보(면적/작물)
   - `MaintenanceHistory`: 수리비, 교육시간, 당시 가동시간 기록
2. **Relationships**:
   - `Tractor` (N) : (1) `Farmer` (소유주 연결)
   - `Tractor` (1) : (N) `MaintenanceHistory` (이력 누적)

## 📝 개발자 노트
- 유지보수를 위해 모든 신규 테이블은 `app/models/` 내에 개별 파일로 생성할 것.
- 트랙터 가동시간(`current_hours`)은 수리 이력이 등록될 때마다 업데이트되는 로직 필요.