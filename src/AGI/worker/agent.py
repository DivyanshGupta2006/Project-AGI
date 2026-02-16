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
            retries=5
            ):
        client = genai.Client(api_key=self.key_manager.get_key())
        contents = [self._format_prompt(prompt, context)]
        if media:
            uploads = read_file.get_uploads(media, client)
            contents.extend(uploads)
        if retries > 0:
            try:
                return client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self.config,
                        temperature=0.7
                    )
                ).text
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    print(f"Key limit hit! Retrying with next key after 15s...")
                    return self.run(prompt, context, media, retries=retries-1)
                elif "503" in str(e):
                    print("Model Unavailable! Waiting 2 minutes...")
                    time.sleep(120)
                    return self.run(prompt, context, media, retries=retries-1)
                else:
                    print(e)
        else:
            print("Unable to use model! Aborting the generation...")