import time
from google import genai
from google.genai import types

from AGI.utility import read_file

class Agent:
    def __init__(self,
                 model,
                 key_manager,
                 system_prompt,
                 role,
                 instructions):
        self.model = model
        self.key_manager = key_manager
        self.config = f'''
            <system_prompt>
            {system_prompt}
            </system_prompt>
            
            <role>
            {role}
            </role>
            
            <instructions>
            {instructions}
            </instructions>
            '''

    def _format_prompt(self,
                       prompt,
                       context=""
                       ):
        return f'''
            <context>
            {context}
            </context>
            
            <user_prompt>
            {prompt}
            </user_prompt>
            '''

    def run(self,
            prompt,
            context="",
            media=None,
            retries=3
            ):
        if retries <= 0:
            print("Max retries reached. Failing gracefully.")
            return None
        cur_key = self.key_manager.get_key()
        client = genai.Client(api_key=cur_key.key)
        contents = [self._format_prompt(prompt, context)]
        if media:
            uploads = read_file.get_uploads(media, client)
            contents.extend(uploads)
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.config,
                    temperature=0.7
                )
            )
            tokens_used = 0
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                tokens_used = getattr(response.usage_metadata, 'total_token_count', 0)

            self.key_manager.report_usage(cur_key, tokens_used=tokens_used)

            return response.text

        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "quota" in error_msg:
                print(f"Key limit hit! Penalizing key and retrying...")
                self.key_manager.report_usage(cur_key, rate_limited=True, reset_in_seconds=60)
                return self.run(prompt, context, media, retries - 1)

            elif "quota" in error_msg:
                print(f"Daily quota exhausted! Shelving key for 24 hours...")
                self.key_manager.report_usage(cur_key, rate_limited=True, reset_in_seconds=86400)
                return self.run(prompt, context, media, retries - 1)

            else:
                print(f"Unexpected API error: {e}")
                self.key_manager.report_usage(cur_key, tokens_used=0)
                time.sleep(15)
                return self.run(prompt, context, media, retries - 1)

