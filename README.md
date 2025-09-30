# Olist 고객 충성도 분석 및 재구매 예측 모델

[![Streamlit App](https://img.shields.io/badge/Live_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://olist-dashboard-xqwt8ppwsnpabjqykshqxd.streamlit.app/)

## 프로젝트 개요

Olist는 브라질의 대규모 이커머스 플랫폼이지만<br>
**신규 고객의 재구매율이 약 3%에 불과**하다는 심각한 문제를 안고 있습니다. <br>
본 프로젝트는 데이터 분석을 통해 '한 번 구매한 고객을 어떻게 충성 고객으로 만들 것인가?'라는 핵심 질문에 답하고자 합니다.

단순한 현상 분석을 넘어, **고객의 첫 구매 경험이 미래의 충성도에 미치는 영향**을 과학적으로 증명하고 이를 기반으로 구체적인 비즈니스 전략을 제시하는 것을 목표로 합니다.

---

## 핵심 목표 및 가설

* **Main Goal:** 신규 고객의 재구매를 유도하는 핵심 요인을 발굴하고 재구매 가능성이 높은 고객을 예측하는 머신러닝 모델 개발<br>
* **Hypothesis:** 좋은 **관문 상품(Gateway Product)**은 고객의 긍정적인 첫 구매 경험을 유도하여 미래의 재구매를 이끌어낼 것이다.

---

## 분석 과정 및 방법론

본 프로젝트는 다음과 같은 체계적인 단계를 거쳐 진행되었습니다.

1.  **EDA (탐색적 데이터 분석):** Olist 데이터셋의 전반적인 구조를 파악하고 고객 및 주문 데이터의 분포와 성장 추세를 시각화하여 비즈니스 현황을 진단했습니다.

2.  **핵심 지표 정의:**<br>
      가설 검증을 위해 '관문 상품'의 효과를 측정할 수 있는 **관문 점수(Gateway Score)**를 새롭게 정의했습니다. <br>
      이는 LTV(고객 생애 가치), 재구매율, 전환율 등 여러 KPI를 종합한 지표입니다.

4.  **머신러닝 모델링:**
      신규 고객의 정보를 바탕으로 **미래 재구매 여부를 예측**하는 분류 모델(Random Forest)을 구축했습니다.<br>
      이를 통해 마케팅 자원을 효율적으로 분배할 수 있는 기반을 마련했습니다.<br>
    * **Target:** `is_loyal` (재구매 여부)
    * **Features:** 첫 구매 관련 정보 (카테고리, 가격, 할부 개월 수, 배송 시간 등)

6.  **모델 해석 (XAI):**
      예측 모델이 '왜' 그렇게 판단했는지 이해하기 위해 **SHAP(SHapley Additive exPlanations) 분석**을 수행했습니다.<br>
      이를 통해 어떤 변수가 고객의 재구매 결정에 가장 큰 영향을 미치는지 과학적으로 증명했습니다.

---

## 주요 발견 (Key Insights)

데이터 분석을 통해 모델의 예측을 해석한 결과, 다음과 같은 매우 의미 있는 인사이트를 발견했습니다.

> **"고객의 첫 구매 금액이 낮을수록, 그리고 할부 개월 수가 짧을수록 해당 고객은 충성 고객이 될 확률이 압도적으로 높다."**

이는 '비싼 상품을 팔아야 이익이 남는다'는 통념을 뒤집는 결과입니다. <br>
Olist의 성장을 위해서는 **저렴한 '관문 상품'으로 진입 장벽을 낮추고, 긍정적인 첫 구매 경험을 제공하여 고객을 플랫폼에 락인(Lock-in)시키는 전략**이 무엇보다 중요합니다.

---

## 프로젝트 구조

```
.
├── 📂 code
│   └── 📜 final_code.ipynb       # 데이터 전처리, 모델링, SHAP 분석 등 모든 분석 과정
│
├── 📂 data
│   └── (raw data files)         # Olist 제공 원본 데이터셋
│
├── 📂 rslt
│   ├── 📄 category_state_distribution.xlsx
│   ├── 📄 category_state_loyal_customers.xlsx
│   ├── 📄 final_kpi_table.xlsx
│   ├── 📄 model_predictions_by_state.xlsx
│   ├── 📄 random_forest_pipeline.joblib  # 학습 완료된 머신러닝 모델
│   ├── 📄 state_kpi_data.xlsx
│   └── 📄 state_logistics_data.xlsx
│
├── 📂 dashboard
│   ├── 📜 app04.py               # Streamlit 인터랙티브 대시보드 앱 코드
│   └── (dashboard data)       # 대시보드 구동에 필요한 데이터 파일
├── 📄 list_pdf                # 발표 자료
│
│
└── 📜 README.md                  # 프로젝트 설명 파일
```

---

## 대시보드 실행 방법

**직접 페이지로 들어갈 수 있는 링크 : https://olist-dashboard-xqwt8ppwsnpabjqykshqxd.streamlit.app/**

본 프로젝트의 분석 결과를 마케팅 담당자나 의사결정자가 쉽게 탐색하고 활용할 수 있도록 인터랙티브 대시보드를 구축했습니다.

1.  **필요 라이브러리 설치:**
    ```bash
    pip install streamlit pandas scikit-learn joblib
    ```

2.  **대시보드 실행:**
    터미널(CLI)에서 아래 명령어를 입력하여 대시보드를 실행합니다.
    ```bash
    streamlit run dashboard/app04.py
    ```

---
