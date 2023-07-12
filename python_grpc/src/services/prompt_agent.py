import os
import openai

class PromptAgent:
    def __init__(self) -> None:
        self.key = os.environ.get('OPENAI_API_KEY')
        openai.api_key = self.key

        self.model = 'gpt-3.5-turbo-0613'

    def convert_to_statements(self, text: str) -> list[str]:

        self.messages = [
            {
                "role": "user", 
                "content": "Task:\n" + 
                           "Break the following question into short, concise statements.\n\n" + 
                           "Requirements:\n" +
                           "1. No added text or context.\n2. Strictly one noun and one pronoun per statement.\n\n" +
                           "Question:\n" + 
                           f"{text}\n\n" +
                           "Statements:\n"  
            }
        ]

        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )

        
        result = completion.choices[0]["message"]["content"]

        result = result.split('\n')
        result = [result[3:] for result in result]

        return result

