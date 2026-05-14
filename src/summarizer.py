import openai
import os
import google.generativeai as genai

class Summarizer:
    def __init__(self, openai_api_key=None, gemini_api_key=None):
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key
        
        self.mode = "fallback"
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.mode = "gemini"
        elif self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.client = openai.OpenAI(api_key=self.openai_api_key)
            self.mode = "openai"

    def summarize(self, text, title=""):
        if self.mode == "fallback":
            return self._fallback_summary(text)
        
        prompt = f"다음 게임 개발 관련 뉴스 기사를 한국어로 3줄 요약해줘.\n제목: {title}\n내용: {text[:4000]}" # Gemini can handle more context

        try:
            if self.mode == "gemini":
                response = self.model.generate_content(prompt)
                return response.text.strip()
            
            elif self.mode == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that summarizes game development news for developers."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Warning: Failed to summarize ({self.mode} Error). Details: {str(e)[:100]}...")
            return self._fallback_summary(text)

    def _fallback_summary(self, text):
        # Fallback: Return the first 300 characters
        if not text:
            return "내용 없음"
        
        # Simple cleanup
        clean_text = text.replace('\n', ' ').strip()
        if len(clean_text) > 300:
            return clean_text[:300] + "..."
        return clean_text
