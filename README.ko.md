# File Organizer Agent

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

파일 확장자를 기반으로 디렉토리의 파일을 자동으로 분류하고 정리하는 Python 기반 도구입니다. 이 도구는 유사한 파일을 적절한 카테고리 폴더로 그룹화하여 깨끗하고 구조화된 파일 시스템을 유지하는 데 도움이 됩니다.

이 프로젝트는 AI 에이전트 기반 워크플로우를 활용하여 기획, 구현, 검토, 테스트, 문서화 단계를 나누어 개발되었습니다.

## 기능

- **자동 파일 분류**: 파일 확장자를 기반으로 미리 정의된 카테고리로 파일을 정리
- **드라이런 모드**: 적용하기 전에 정리 변경 사항을 미리보기
- **중복 처리**: 파일명에 번호를 추가하여 중복 파일명을 자동으로 처리
- **종합 로깅**: 모든 작업을 파일과 콘솔에 기록
- **명령줄 인터페이스**: 유연한 옵션이 있는 간단하고 직관적인 CLI
- **확장 가능한 카테고리**: 새로운 파일 카테고리와 확장자를 쉽게 추가
- **크로스 플랫폼**: Windows, macOS, Linux에서 작동

### 지원되는 카테고리

- **PDF**: `.pdf`
- **Slides**: `.pptx`, `.ppt`, `.odp`
- **Docs**: `.docx`, `.doc`, `.odt`, `.txt`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
- **Installers**: `.exe`, `.msi`, `.dmg`, `.pkg`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Code**: `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h`
- **Data**: `.csv`, `.xlsx`, `.xls`, `.json`, `.xml`
- **Others**: 기타 모든 파일 확장자

## 설치

### 사전 요구사항

- Python 3.7 이상
- pip (Python 패키지 설치 프로그램)

### 소스에서 설치

1. 저장소를 클론하거나 다운로드:
   ```bash
   git clone <repository-url>
   cd file-organizer-agent
   ```

2. 종속성 설치:
   ```bash
   pip install -r requirements.txt
   ```

이 프로그램은 최소한의 종속성을 가지며 대부분의 Python 설치에서 즉시 작동합니다.

## 사용법

### 기본 사용법

Downloads 폴더의 파일을 정리 (드라이런 모드):
```bash
python -m src.main
```

특정 디렉토리의 파일 정리:
```bash
python -m src.main --target /path/to/your/directory
```

정리 적용 (파일 이동):
```bash
python -m src.main --target /path/to/your/directory --apply
```

**참고**: `.DS_Store`, `.localized` 등 시스템 파일의 우발적 이동을 방지하기 위해 `.`으로 시작하는 숨김 파일은 자동으로 정리 대상에서 제외됩니다.

### 명령줄 옵션

- `--target PATH`: 정리할 대상 디렉토리 지정 (기본값: ~/Downloads)
- `--apply`: 정리 적용하여 파일 이동 (기본값: 드라이런 모드만)

### 예제

#### 예제 1: Downloads 폴더 정리 미리보기
```bash
python -m src.main
```
출력:
```
Planned to organize 15 files:
  PDF: 3 files
  Images: 5 files
  Docs: 2 files
  Archives: 2 files
  Others: 3 files
Would move document.pdf to PDF/document.pdf
Would move photo.jpg to Images/photo.jpg
...
```

#### 예제 2: 특정 폴더 정리
```bash
python -m src.main --target ./messy_folder --apply
```
출력:
```
Planned to organize 8 files:
  Code: 3 files
  Data: 2 files
  Others: 3 files
Moved script.py to Code/script.py
Moved data.csv to Data/data.csv
...
```

#### 예제 3: 중복 파일명 처리
동일한 이름의 파일이 여러 개 있는 경우, 정리 도구가 자동으로 고유한 이름을 생성합니다:
```
original.txt -> Docs/original.txt
original.txt -> Docs/original_1.txt
original.txt -> Docs/original_2.txt
```

## 설정

### 기본 대상 디렉토리

기본적으로 정리 도구는 시스템의 Downloads 폴더를 대상으로 합니다:
- **macOS/Linux**: `~/Downloads`
- **Windows**: `C:\Users\<username>\Downloads`

`src/config.py`를 수정하여 이 기본값을 변경할 수 있습니다:
```python
DEFAULT_TARGET = Path.home() / "Downloads"  # 이 경로를 변경
```

### 새 카테고리 추가

새 파일 카테고리를 추가하려면 `src/config.py`를 편집하세요:
```python
CATEGORIES = {
    "PDF": ["pdf"],
    "Slides": ["pptx", "ppt", "odp"],
    "YourNewCategory": ["ext1", "ext2", "ext3"],  # 카테고리 추가
    "Others": []
}
```

## 로깅

정리 도구는 모든 작업의 상세 로그를 생성합니다:

- **로그 파일**: `logs/organizer.log`
- **콘솔 출력**: 실시간 진행 상황과 결과
- **로그 형식**: 타임스탬프, 레벨, 메시지

로그 항목 예시:
```
2024-01-15 10:30:15 - INFO - Starting file organizer on /Users/user/Downloads, apply=False
2024-01-15 10:30:15 - INFO - DRY RUN: Would move document.pdf to PDF/document.pdf
2024-01-15 10:30:16 - INFO - File organization completed.
```

## 요구사항

- **Python**: 3.7+
- **종속성**: 없음 (Python 표준 라이브러리만 사용)
- **운영체제**: Windows, macOS, Linux

### 개발 종속성

테스트 및 개발용:
- pytest
- pytest-cov

## 테스트

프로젝트에는 포괄적인 단위 테스트와 통합 테스트가 포함되어 있습니다.

### 테스트 실행

테스트 종속성 설치:
```bash
pip install -r requirements.txt
```

모든 테스트 실행:
```bash
pytest
```

커버리지와 함께 실행:
```bash
pytest --cov=src --cov-report=html
```

특정 테스트 카테고리 실행:
```bash
pytest -m "not slow"  # 느린 테스트 건너뛰기
pytest tests/test_organizer.py  # 특정 테스트 파일 실행
```

### 수동 테스트

수동 테스트 절차는 `MANUAL_TESTING.md`를 참조하세요.

## 면접 대비 문서

프로젝트 설명 흐름, 안전한 자동화 설계, 문제 해결 과정, 면접 답변 포인트는 [`docs/interview-notes.md`](./docs/interview-notes.md)에 정리했습니다.

## 프로젝트 구조

```
file-organizer-agent/
├── src/
│   ├── main.py          # CLI 진입점
│   ├── organizer.py     # 핵심 정리 로직
│   ├── config.py        # 설정 및 카테고리
│   └── utils.py         # 유틸리티 함수
├── tests/
│   ├── test_*.py        # 단위 테스트
│   └── conftest.py      # 테스트 픽스처
├── logs/                # 로그 파일 (런타임에 생성)
├── sample_downloads/    # 테스트용 샘플 파일
├── requirements.txt     # Python 종속성
├── pytest.ini          # Pytest 설정
├── MANUAL_TESTING.md   # 수동 테스트 가이드
└── README.md           # 이 파일
```

## 기여

기여를 환영합니다! 다음 가이드라인을 따라주세요:

### 개발 설정

1. 저장소 포크
2. 기능 브랜치 생성: `git checkout -b feature/your-feature-name`
3. 개발 종속성 설치: `pip install -r requirements.txt`
4. 테스트 실행: `pytest`
5. 변경 사항 적용
6. 새 기능에 대한 테스트 추가
7. 모든 테스트 통과 확인
8. 필요한 경우 문서 업데이트
9. 변경 사항 커밋: `git commit -m "Add your feature"`
10. 포크에 푸시: `git push origin feature/your-feature-name`
11. Pull Request 생성

### 코드 스타일

- PEP 8 스타일 가이드라인 준수
- 함수 매개변수와 반환 값에 타입 힌트 사용
- 설명적인 커밋 메시지 작성
- 모든 공개 함수와 클래스에 독스트링 추가

### 테스트

- 모든 새 기능에 단위 테스트 작성
- 테스트 커버리지 80% 이상 유지
- 엣지 케이스와 에러 조건 테스트
- PR 제출 전 전체 테스트 스위트 실행

### 이슈 보고

버그를 보고하거나 기능을 요청할 때:

1. 기존 이슈 먼저 확인
2. 명확하고 설명적인 제목 사용
3. 이슈 재현 단계 제공
4. 환경 정보 포함 (OS, Python 버전)
5. 관련 로그 파일 첨부 (가능한 경우)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 라이선스됩니다 - 자세한 내용은 LICENSE 파일을 참조하세요.

## 변경 로그

### 버전 1.0.0
- 초기 릴리스
- 기본 파일 정리 기능
- 드라이런 모드
- 명령줄 인터페이스
- 포괄적인 테스트 스위트
- 로깅 지원

## 지원

문제가 발생하거나 질문이 있는 경우:

1. `MANUAL_TESTING.md`의 문제 해결 섹션 확인
2. `logs/organizer.log`의 로그 검토
3. GitHub의 기존 이슈 검색
4. 자세한 정보와 함께 새 이슈 생성

## 로드맵

향후 개선 사항:
- GUI 인터페이스
- 설정 파일을 통한 사용자 정의 카테고리 정의
- 실행 취소 기능
- 파일 관리자와 통합
- 클라우드 저장소 지원
- 고급 필터링 옵션
