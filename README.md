# 루틴메이트 (RoutineMate)

목표 · 오늘 쓸 수 있는 시간 · 현재 컨디션을 입력하면 AI가 지금 바로 실천할 수 있는
맞춤 미니 루틴을 추천해주는 웹 서비스입니다.

**배포 URL:** https://routinemate.vercel.app  *(Vercel 배포 후 실제 주소로 교체하세요)*

---

## 1. 서비스 소개

- 거창한 습관 앱 대신, "오늘 이 시간에 이걸 하면 된다"는 아주 구체적인 실행안 하나를 제안합니다.
- 회원가입 없이 바로 사용할 수 있습니다.
- 총 4개 섹션(홈 / 서비스 소개 / AI 루틴 추천 / 문의하기)으로 구성되어 있고, 상단 내비게이션으로 이동합니다.

## 2. 기술 스택

| 영역 | 스택 |
|---|---|
| 프론트엔드 | HTML5, CSS3, Vanilla JavaScript |
| 백엔드 | Vercel Serverless Functions (Python) |
| AI API | Anthropic Claude API (`claude-3-5-haiku-latest`) |
| 배포 | Vercel (GitHub 연동 자동 배포) |
| 폰트 | Google Fonts (Fraunces, IBM Plex Sans KR) |

## 3. 프로젝트 구조

```
routinemate/
├── index.html          # 전체 페이지 (홈/소개/AI추천/문의 4개 섹션)
├── css/
│   └── style.css
├── js/
│   └── main.js         # 폼 제출, fetch 호출, 실패 처리(빈 입력/API 오류/타임아웃)
├── api/
│   └── recommend.py    # Vercel Python 서버리스 함수, Claude API 호출
├── requirements.txt    # 백엔드 파이썬 의존성
├── .env.example         # 환경 변수 템플릿
├── .gitignore
└── README.md
```

## 4. 로컬에서 실행하기

```bash
# 1) 저장소 클론
git clone https://github.com/<your-id>/routinemate.git
cd routinemate

# 2) Vercel CLI 설치 (최초 1회)
npm install -g vercel

# 3) 환경 변수 파일 준비
cp .env.example .env
# .env 파일을 열어 실제 ANTHROPIC_API_KEY 값을 입력

# 4) 로컬 개발 서버 실행 (프론트 + api/ 함수 모두 동작)
vercel dev
```

브라우저에서 `http://localhost:3000` 접속 후 확인합니다.

## 5. 배포 방법 (Vercel)

1. GitHub에 이 저장소를 푸시합니다.
2. [vercel.com](https://vercel.com)에서 `New Project` → 방금 푸시한 GitHub 저장소를 선택합니다.
3. **Environment Variables**에 아래 값을 등록합니다.
   - `ANTHROPIC_API_KEY` = 발급받은 Anthropic API 키
4. `Deploy`를 누르면 자동으로 빌드/배포됩니다.
5. 이후 `main` 브랜치에 커밋을 푸시할 때마다 자동으로 재배포됩니다.

## 6. 환경 변수

| 변수명 | 설명 | 필수 여부 |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키. [console.anthropic.com](https://console.anthropic.com)에서 발급 | 필수 |

> API 키는 절대 코드나 README, 스크린샷에 노출하지 않고 Vercel의 환경 변수 설정으로만 관리합니다.
> 키 유출이 의심되면 즉시 Anthropic 콘솔에서 폐기/재발급하고, 노출된 커밋 이력을 정리하세요.

## 7. AI 기능 동작 확인

1. `AI 루틴 추천` 섹션으로 이동합니다.
2. 목표 / 시간 / 컨디션을 입력하고 `루틴 추천받기`를 클릭합니다.
3. 아래와 같은 상황을 각각 확인할 수 있습니다.
   - **정상 입력:** 추천 루틴 카드가 표시됨
   - **빈 입력:** "목표, 시간, 컨디션을 모두 입력해주세요." 안내 표시
   - **API 오류/타임아웃:** "잠시 후 다시 시도해주세요" 계열 안내 표시

## 8. 라이선스

이 프로젝트는 학습 미션 제출용 데모입니다.
