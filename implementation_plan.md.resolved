# Game Dev News Notifier 구현 계획

매일 아침 9시 50분에 게임 개발 관련 뉴스를 수집, 요약하여 디스코드 Webhook으로 전송하는 파이썬 프로그램입니다.

## User Review Required

> [!IMPORTANT]
> **OpenAI API Key**: 고품질의 "3줄 요약"과 "한국어 번역"을 위해서는 OpenAI GPT 같은 LLM 사용이 권장됩니다. 무료 NLP 라이브러리(`sumy` 등)는 한국어 요약 품질이 낮거나 영어 원문을 그대로 요약할 수 있습니다. 사용자가 API Key를 입력할 수 있는 구조로 만들겠습니다.
> **Discord Webhook URL**: 사용자가 자신의 디스코드 서버 웹훅 URL을 설정해야 합니다.

## Proposed Changes

### Core Logic (`src/`)
#### [NEW] [main.py](file:///C:/Users/USER/.gemini/antigravity/brain/79655815-51cc-45f9-a4e5-d0c2b9fc08d5/src/main.py)
- 프로그램의 진입점.
- 스케줄러 설정 (매일 09:50).
- 설정 파일(`config.json`) 로드.

#### [NEW] [news_scraper.py](file:///C:/Users/USER/.gemini/antigravity/brain/79655815-51cc-45f9-a4e5-d0c2b9fc08d5/src/news_scraper.py)
- `feedparser`를 사용하여 주요 게임 개발 관련 RSS 피드 수집.
- 대상 사이트: Game Developer (Gamasutra), GamesIndustry.biz.
- 최신 10개 기사 필터링.

#### [NEW] [summarizer.py](file:///C:/Users/USER/.gemini/antigravity/brain/79655815-51cc-45f9-a4e5-d0c2b9fc08d5/src/summarizer.py)
- OpenAI API 연동 (Key가 있을 경우).
- 3줄 요약 및 한국어 번역 수행.
- Fallback: 제목 번역만 제공하거나 원문 앞부분 발췌.

#### [NEW] [discord_sender.py](file:///C:/Users/USER/.gemini/antigravity/brain/79655815-51cc-45f9-a4e5-d0c2b9fc08d5/src/discord_sender.py)
- `requests`를 이용해 Discord Webhook으로 메시지 발송.
- Embed 형식으로 깔끔하게 정리.

#### [NEW] [config_manager.py](file:///C:/Users/USER/.gemini/antigravity/brain/79655815-51cc-45f9-a4e5-d0c2b9fc08d5/src/config_manager.py)
- `config.json` 관리 (Webhook URL, API Key 등).

### Configuration
#### [NEW] [config.json](file:///C:/Users/USER/.gemini/antigravity/brain/79655815-51cc-45f9-a4e5-d0c2b9fc08d5/config.json)
- 사용자 설정 파일 템플릿.

## 기술 스택
- Python 3.x
- Libraries: `feedparser`, `requests`, `schedule`, `openai` (optional), `python-dotenv`

## Verification Plan

### Automated Tests
- 유닛 테스트: RSS 파싱 기능 테스트.
- 유닛 테스트: 요약 모듈 Mock 테스트.

### Manual Verification
- `main.py` 실행 후 즉시 뉴스 수집 및 디스코드 전송 테스트 (테스트 모드).
- 스케줄러가 9시 50분에 동작하는지 로컬 시간 변경하여 확인.
