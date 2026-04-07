# Data Pipeline DSL Workflow (Summary)

## 1. Objective

Excel 기반 복잡한 레시피 문서를 구조화하여
재사용 가능한 DSL → 자동 실행 파이프라인으로 전환

---

## 2. Overall Architecture

```
Excel (xlsx)
  ↓
Parser (xlwings + pandas)
  ↓
Structured JSON
  ↓
[clineSR] → Sheet 단위 분할 + 압축
  ↓
[Qwen] → DSL 생성
  ↓
[Nemotron] → DSL 검증 및 수정
  ↓
[clineSR] → 실행 가능한 DSL로 정제
  ↓
Python Code Generation
  ↓
Execution (pandas pipeline)
```

---

## 3. Key Components

### 3.1 Excel Parser

* xlwings: 수식 / 구조 추출
* pandas: 테이블 데이터 처리
* 출력: LLM 입력용 JSON

---

### 3.2 JSON 분할 (clineSR)

* Sheet 단위로 분리
* 토큰 최적화 (샘플/노트 축소)
* 파일 단위 병렬 처리 가능

---

### 3.3 DSL 생성 (Qwen)

* JSON → YAML DSL 변환
* steps 기반 구조 생성
* formula / filter / merge 등 정의

---

### 3.4 DSL 검증 (Nemotron)

* 논리 오류 탐지
* 누락 step 보완
* dependency 검증

---

### 3.5 DSL 정제 (clineSR)

* pandas 실행 가능 형태로 변환
* input/output 명확화
* DataFrame 흐름 정의

---

### 3.6 코드 생성 (clineSR)

* DSL → Python 코드 자동 변환
* pandas 기반 실행 함수 생성
* 예외 처리 포함

---

## 4. Validation Layer

### Mermaid Visualization

* DSL → 그래프 변환
* 흐름 검증 (누락/순서 오류 확인)

---

## 5. Key Design Principles

* **Chunking First**: 대용량 입력은 반드시 분할
* **DSL 중심 설계**: 모든 로직은 DSL로 추상화
* **Separation of Roles**:

  * Qwen: 생성
  * Nemotron: 검증
  * clineSR: 실행화
* **Execution-Ready DSL**: pandas 기준으로 바로 실행 가능

---

## 6. Outcome

* Excel 기반 수작업 제거
* 레시피 재사용 가능 구조 확보
* 자동 코드 생성 파이프라인 구축
* 확장 가능한 사내 데이터 처리 시스템 기반 확보

---

## 7. Next Steps

* DSL → Execution Engine 고도화
* 에러 로깅 및 모니터링 추가
* Report 자동 생성 (PDF/Excel)
* 내부 서비스화 (UI/API)

---
