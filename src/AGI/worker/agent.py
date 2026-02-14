from google import genai


class Agent:
    def __init__(self,
                 model,
                 api_key):
        self.model = model
        self.client = genai.Client(api_key=api_key)
    def run(self,
            prompt,
            system_prompt=""):
        return self.client.models.generate_content(
            model=self.model,
            contents=f'System Prompt: {system_prompt} \n User Prompt: {prompt}'
        ).text