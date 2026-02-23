# 1. 프로젝트 개요

본 프로젝트는 네이버 플레이스 리뷰 데이터를 크롤링하여,  
중복 리뷰를 해시(Hash) 기반으로 검증한 뒤 데이터베이스에 적재하는 자동화 ETL 파이프라인입니다.

Airflow 기반으로 구성되었으며,  
크롤링 → 중복 검증 → Upsert 적재 흐름을 안정적으로 운영합니다.

이미 수집된 리뷰를 기억해두고(최근 Hash 로드),  
신규 리뷰만 선별적으로 저장하는 구조입니다

---

# 2. 전체 처리 흐름

```text
[리뷰 크롤링 시작]
        ↓
[최근 Hash 로드]
        ↓
[리뷰 카드 파싱]
        ↓
[리뷰 Hash 생성]
        ↓
[기존 데이터 비교]
        ↓
[중복 발견 시 중단]
        ↓
[Upsert 적재]
```

---

# 3. 처리 로직 핵심

## 3.1 최근 데이터 로드

```python
existing_hashes = get_recent_hashes(engine, limit=50)
```

- 최근 50개 리뷰의 hash 값을 로드
- 기존 데이터 비교 기준 확보

---

## 3.2 리뷰 단위 Hash 생성

```python
review_hash = generate_review_hash(
    review_text=row["review_text"],
    visit_date=row.get("visit_date"),
    designer=row["designer"],
)
```

Hash 생성 기준:

- 리뷰 내용
- 방문 날짜
- 디자이너

동일 리뷰는 동일한 hash를 생성합니다.

---

## 3.3 중복 발견 시 중단 로직

```python
if review_hash in existing_hashes:
    print("기존 데이터 발견 → 중단")
    break
```

정책:

- 기존 데이터 발견 시 즉시 중단
- 불필요한 재크롤링 방지
- DB 중복 적재 차단

---

## 3.4 최종 적재

```python
upsert_reviews(engine, df)
```

- 신규 리뷰만 DataFrame 구성
- Upsert 방식으로 안전하게 저장

---

# 4. 데이터 모델 요약

## review 테이블

| Column        | Description |
|--------------|------------|
| review_id    | 리뷰 PK |
| customer_id  | 고객 ID (FK) |
| designer_id  | 디자이너 ID |
| review_text  | 리뷰 본문 |
| keywords     | 후기 키워드 배열 |
| visit_date   | 방문 날짜 |
| is_reserved  | 예약 여부 |
| review_hash  | 중복 검증용 Hash |

---

# 5. 디렉토리 구조

```
airflow/
 ├─ dags/
 ├─ plugins/
 ├─ docker-compose.yaml

src/
 ├─ browser/ 
 ├─ review_parser/
 ├─ db/
 ├─ navigation/
 ├─ scroll/
 ├─ utils
 └─ config/
```

---

# 6. 기술 스택

- Orchestration: Apache Airflow  
- Crawling: Selenium  
- Processing: Python  
- Storage: PostgreSQL  
- Infra: Docker Compose  
- OS: Linux  

---

# 7. 설계 특징

## 1. Hash 기반 중복 차단

- 최근 데이터 기준 비교
- 전체 테이블 스캔 방지

## 2. 점진적 수집 구조

- 최신 리뷰부터 수집
- 기존 데이터 발견 시 즉시 종료.

## 3. Upsert 기반 안전 적재

- 중복 입력 방지
- 데이터 정합성 유지

---

# 정리

네이버 플레이스 리뷰를 크롤링하고,  
Hash 기반 중복 검증을 통해 신규 데이터만 적재하는  
Airflow 기반 자동화 ETL 파이프라인입니다.
