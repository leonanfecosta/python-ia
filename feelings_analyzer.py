import os
from typing import Any

import google.generativeai as genai
import gradio as gr
from google.api_core.exceptions import InvalidArgument

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
initial_prompt = (
    "Você é um assistente virtual que analisa sentimentos em textos."
    "Você é capaz de processar arquivos de texto e analisar o sentimento deles."
    "Sempre que alguem perguntar sobre um arquivo, verifique o histórico para encontrar o arquivo correspondente."
    "Não diga que não é capaz de processar arquivos, pois você é."
)

model = genai.GenerativeModel(
    "gemini-1.5-flash", system_instruction=initial_prompt
)

chat = model.start_chat()


def assemble_prompt(message: dict[str, Any]) -> str:
    user_text = message["text"]
    files = message.get("files", [])
    file_contents = []
    if files:
        for file_info in files:
            if file_info["mime_type"] == "text/plain":
                with open(file_info, "r", encoding="utf-8") as f:
                    content = f.read()
                file_contents.append(content)
            else:
                pass
    combined_text = user_text + "\n\n" + "\n\n".join(file_contents)
    prompt = f"Analise o sentimento do seguinte texto:\n{combined_text}"
    return prompt


def grab_sentiment(message: dict[str, Any], _history: dict[str, Any]) -> str:
    prompt = assemble_prompt(message)
    try:
        response = chat.send_message(prompt)
    except InvalidArgument as e:
        response = chat.send_message(
            f"O usuário te enviou um arquivo para você ler e obteve o erro: {e}. "
            "Pode explicar o que houve e dizer quais tipos de arquivos você "
            "dá suporte? Assuma que a pessoa não sabe programação e "
            "não quer ver o erro original. Explique de forma simples e concisa."
        )
    return response.text


def main() -> None:
    chat_interface = gr.ChatInterface(
        fn=grab_sentiment,
        title="Analisador de Sentimentos 🎭",
        multimodal=True,
    )
    chat_interface.launch()


if __name__ == "__main__":
    main()
