from google import genai
from google.genai import types


class Agent:
    def __init__(self,
                 model,
                 api_key,
                 system_prompt,
                 role,
                 instructions):
        self.model = model
        self.client = genai.Client(api_key=api_key)
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
            context=""
            ):
        return self.client.models.generate_content(
            model=self.model,
            contents=self._format_prompt(prompt, context),
            config=types.GenerateContentConfig(
                system_instruction=self.config,
                temperature=0.7
            )
        ).text
