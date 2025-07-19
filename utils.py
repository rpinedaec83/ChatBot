import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente útil y amable."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("OpenAI Error:", e)
        return "Lo siento, ocurrió un error al procesar tu mensaje."
