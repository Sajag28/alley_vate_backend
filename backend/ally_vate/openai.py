import openai
import os
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
def call_openai_api(question, answer):
    openai.api_key = "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"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
         messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Question: {question}"},
            {"role": "assistant", "content": f"Answer: {answer}"},
            {"role": "user", "content": "Is this a good answer?"}
        ],
        
    )
    return response.choices[0].message['content'].strip()