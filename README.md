# 🎮 Game Economy & Dev News Notifier

매일 아침 **09:50**에 최신 게임 개발 및 경제 관련 뉴스를 수집하고, **AI로 3줄 요약**하여 **디스코드**로 전송해주는 봇입니다.
GitHub Actions를 이용해 **무료로 24시간 자동화**할 수 있습니다.

![Discord Notification Example](https://img.shields.io/badge/Discord-Notification-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-8E75B2?style=for-the-badge)

## ✨ 주요 기능
- **자동 뉴스 수집**: Game Developer, GamesIndustry.biz 등 주요 매체의 최신 기사를 긁어옵니다.
- **AI 3줄 요약**:
    - **Google Gemini API (무료)** 또는 OpenAI GPT를 사용하여 핵심 내용을 한글로 요약합니다.
    - API Key가 없으면 자동으로 뉴스 앞부분을 요약 대신 보여줍니다.
- **디스코드 알림**: 깔끔한 Embed 형태로 뉴스 링크, 제목, 요약을 전송합니다.
- **서버리스 실행**: 컴퓨터를 켜두지 않아도 GitHub Actions에서 자동으로 돌아갑니다.

## 🚀 사용 방법 (GitHub Actions - 추천)
개인 컴퓨터를 켜두지 않고 **완전 자동화**하는 방법입니다.

### 1. Fork 및 설정
1. 이 저장소를 **Fork** 하거나 다운로드하여 자신의 GitHub 저장소에 올립니다.
2. 저장소의 **Settings** > **Secrets and variables** > **Actions** 메뉴로 이동합니다.
3. `New repository secret`을 눌러 다음 변수들을 등록합니다.

| Name | Description | 비고 |
|------|-------------|------|
| `DISCORD_WEBHOOK_URL` | 일반 게임 뉴스 웹훅 주소 (Game Developer) | **필수** |
| `DISCORD_ECONOMY_WEBHOOK_URL` | 경제 뉴스 웹훅 주소 (GamesIndustry.biz) | **필수** |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급받은 무료 API 키 | **추천 (무료)** |
| `OPENAI_API_KEY` | OpenAI API 키 | 선택 사항 (유료) |

이제 매일 한국 시간 **09:50**에 자동으로 뉴스가 배달됩니다! 🚚

---

## 💻 로컬 실행 방법 (내 컴퓨터에서 돌리기)
직접 컴퓨터에서 테스트하거나 실행하려면 다음 순서를 따르세요.

1. **설치**:
   ```bash
   git clone https://github.com/hyungjin-yu/Game_Economy_News.git
   cd Game_Economy_News
   
   # 실행 스크립트 (Windows)
   run.bat
   ```
   또는 수동으로:
   ```bash
   pip install -r requirements.txt
   python src/main.py --run-now
   ```

2. **설정 (`config.json`)**:
   파일을 열어 웹훅 주소와 API 키를 입력하세요.

## 🐳 Docker 실행 방법
Docker가 설치되어 있다면 간편하게 실행할 수 있습니다.

1. **이미지 빌드 및 실행**:
   ```bash
   docker-compose up -d --build
   ```
2. **환경 변수 설정**:
   `.env` 파일을 만들어서 키를 관리하거나 `docker-compose.yml`을 직접 수정하세요.

```bash
# .env 파일 예시
DISCORD_WEBHOOK_URL=your_webhook_url
GEMINI_API_KEY=your_gemini_key
```

## 🛠 기술 스택
- **Language**: Python 3.9
- **Libraries**: `feedparser` (RSS), `requests` (Webhook), `google-generativeai` (AI Summary), `schedule`
- **Infrastructure**: GitHub Actions (Cron Job)

## 📝 License
This project is open source. Feel free to use and modify!
