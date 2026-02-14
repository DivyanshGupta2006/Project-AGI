from google import genai


class Agent:
    def __init__(self,
                 model,
                 api_key,
                 system_prompt,
                 role,
                 instructions):
        self.model = model
        self.client = genai.Client(api_key=api_key)
        self.system_prompt = system_prompt
        self.role = role
        self.instructions = instructions

    def _format_prompt(self,
                       prompt,
                       context=""
                       ):
        return f'''
            <system_prompt>
            {self.system_prompt}
            </system_prompt>
            
            <role>
            {self.role}
            </role>
            
            <context>
            {context}
            </context>
            
            <user_prompt>
            {prompt}
            </user_prompt>
            
            <instructions>
            {self.instructions}
            </instructions>
            '''

    def run(self,
                prompt,
                context=""
                ):
            return self.client.models.generate_content(
                model=self.model,
                contents=self._format_prompt(prompt, context)
            ).text
