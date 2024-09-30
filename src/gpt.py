import os
import openai

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = "sk-ouapzZyTJaNSUAO480744a8693F446B1B1A552Da73A05971"
openai.base_url = "https://free.gpt.ge/v1/"
openai.default_headers = {"x-foo": "true"}


def analyze_with_gpt(content, task_prompt):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        messages=[
            {"role": "system", "content": task_prompt},
            {"role": "user", "content": content}
        ]
    )
    
    return completion.choices[0].message.content



