import openai
import time
from datetime import datetime
import os
import tiktoken
import json

class GPT4LLMHandler:
    def __init__(self, api_key=os.environ['OPENAI_API_KEY'], model="gpt-4o-2024-08-06", temperature=1, max_tokens=5000):
        openai.api_key = api_key
        self.client = openai.OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.price_per_1k_tokens = 0.0025

    def _count_tokens(self, text):
        encoding = tiktoken.get_encoding('o200k_base')
        num_tokens = len(encoding.encode(text))
        return num_tokens

    def generate_response(self, system_message, user_message):
        try:
            start_time = time.time()
            input_tokens = self._count_tokens(system_message) + self._count_tokens(user_message)

            response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                            "role": "system",
                            "content": [
                                {
                                "type": "text",
                                "text": system_message
                                }
                            ]
                            },
                            {
                            "role": "user",
                            "content": [
                                {
                                "type": "text",
                                "text": user_message
                                }
                            ]
                            }
                        ],
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        response_format={
                            "type": "json_object"
                        }
                        )

            end_time = time.time()
            output = response.choices[0].message.content
            output_tokens = self._count_tokens(json.dumps(json.loads(output)['tools'], sort_keys=False))
            total_tokens = input_tokens + output_tokens
            total_cost = (total_tokens / 1000) * self.price_per_1k_tokens

            return {
                "full": response,
                "response": output,
                "latency": end_time - start_time,
                "cost": total_cost
            }
        
        except:
            return {
                "full": response,
                "response": output,
                "latency": end_time - start_time,
                "cost": total_cost
            }