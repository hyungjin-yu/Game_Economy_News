import openai
import os

class Summarizer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key:
            openai.api_key = self.api_key
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def summarize(self, text, title=""):
        if not self.client:
            return self._fallback_summary(text)
        
        try:
            prompt = f"다음 게임 개발 관련 뉴스 기사를 한국어로 3줄 요약해줘.\n제목: {title}\n내용: {text[:2000]}" # Limit content length
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes game development news for developers."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except openai.AuthenticationError:
            print("Warning: OpenAI API Key is invalid or expired. Skipping summary.")
            return self._fallback_summary(text)
        except Exception as e:
            # Print simplified error for common issues
            print(f"Warning: Failed to summarize (OpenAI Error). Details: {str(e)[:100]}...")
            return self._fallback_summary(text)

    def _fallback_summary(self, text):
        # Simple fallback: return first 200 chars or similar
        return "요약 기능 비활성화 (API Key 없음) - 원문 확인 필요"
