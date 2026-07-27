from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.models.list()
    print("Conexión correcta")
    for model in response.data[:5]:
        print(model.id)
except Exception as e:
    print(e)