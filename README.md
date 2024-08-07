# 영수증 관리 및 지출 추적

이 프로젝트는 사용자가 영수증을 업로드하고, Azure Form Recognizer를 사용하여 관련 정보를 추출한 후, 지출 내역을 추적하는 웹 애플리케이션입니다. Flask와 Streamlit을 사용하여 구축되었으며, 추출된 데이터는 SQLite 데이터베이스에 저장됩니다. 사용자는 월별 지출 보고서를 생성하고 지출을 시각화할 수 있습니다.

## 기능

- 영수증 이미지 업로드 및 상점 이름, 거래 날짜, 총 금액 등의 정보 추출
- 추출된 영수증 정보를 SQLite 데이터베이스에 저장
- 시각화된 월별 지출 보고서 생성
- Streamlit을 사용한 사용자 친화적인 인터페이스

## 시작하기

### 사전 요구 사항

- Python 3.7+
- Azure Form Recognizer 리소스 (엔드포인트 및 API 키)

### 설치

1. 저장소를 클론합니다:

   ```bash
   git clone https://github.com/your-username/receipt-management.git
   cd receipt-management
