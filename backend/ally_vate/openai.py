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
            {"role": "user", "content": "Is this a good answer or postive response?"}
        ],
        
    )
    print(response)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
         messages=[
            {"role": "system", "content": f"{response}"},
            # {"role": "user", "content": f"Question: {question}"},
            # {"role": "assistant", "content": f"Answer: {answer}"},
            {"role": "user", "content": "Is this a postive response?"}
        ],
        
    )
    return response.choices[0].message['content'].strip()