# 영수증 관리 및 지출 추적

## 프로젝트 개요
이 프로젝트는 사용자가 영수증을 업로드하고, **Azure Form Recognizer**를 활용하여 관련 정보를 추출한 후, **지출 내역을 추적하는 웹 애플리케이션**입니다. Flask와 Streamlit을 사용하여 개발되었으며, **SQLite 데이터베이스**에 데이터를 저장합니다. 사용자는 **월별 지출 보고서 생성 및 시각화** 기능을 활용할 수 있습니다.

## 주요 기능
- **영수증 이미지 업로드** 및 상점 이름, 거래 날짜, 총 금액 등의 정보 자동 추출
- **Azure Form Recognizer**를 이용한 OCR 데이터 처리
- **SQLite 데이터베이스에 영수증 정보 저장**
- **월별 지출 보고서 시각화** (그래프 및 표)
- **Streamlit을 활용한 대시보드** 제공

## 프로젝트 구조
```
receipt-expense-tracker/
│── app.py  # Flask 웹 애플리케이션 실행 파일
│── streamlit_app.py  # Streamlit 대시보드 실행 파일
│── expenses.db  # SQLite 데이터베이스
│── report_2020_01.png  # 예제 보고서 이미지
│── requirements.txt  # 필요 라이브러리 목록
│── .env  # 환경 변수 (Azure API Key 저장)
└── README.md  # 프로젝트 설명 파일
```

## 설치 및 실행 방법
### 1. 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 2. Flask 서버 실행
```bash
python app.py
```

### 3. Streamlit 대시보드 실행
```bash
streamlit run streamlit_app.py
```

## API 사용 방법
### 1. 영수증 업로드 및 데이터 추출 (`POST /upload_receipt`)
- **요청 예시**:
    ```json
    {
        "image": "receipt.jpg"
    }
    ```
- **응답 예시**:
    ```json
    {
        "store_name": "ABC Mart",
        "date": "2024-03-01",
        "total": 29.99
    }
    ```

### 2. 월별 지출 보고서 생성 (`GET /generate_report`)
- **응답 예시**:
    ```json
    {
        "month": "March",
        "total_spent": 320.50,
        "top_categories": ["Groceries", "Dining"]
    }
    ```

## 필요 라이브러리
- `Flask`
- `Streamlit`
- `sqlite3`
- `requests`

## 환경 변수 설정 (.env 파일 필요)
```
AZURE_FORM_RECOGNIZER_ENDPOINT=<your_endpoint>
AZURE_FORM_RECOGNIZER_API_KEY=<your_api_key>
```

## 기여 방법
1. 본 레포지토리를 포크합니다.
2. 새로운 브랜치를 생성합니다.
3. 변경 사항을 커밋하고 푸시합니다.
4. Pull Request를 생성하여 기여합니다.

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.

