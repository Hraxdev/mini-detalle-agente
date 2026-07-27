from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Di únicamente Hola"
            }
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    print(e)