import os
import time
from typing import Any, LiteralString

import google.generativeai as genai
import gradio as gr
from google.api_core.exceptions import InvalidArgument

from home_assistant import (
    good_morning,
    intruder_alert,
    set_light_values,
    start_music,
)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
initial_prompt = (
    "Você é um assistente virtual capaz de processar arquivos como imagens, textos e outros tipos. "
    "Sempre que alguém perguntar sobre um arquivo, verifique o histórico para encontrar o arquivo correspondente. "
    "Não diga que não é capaz de processar arquivos, pois você é."
    "Você tem acesso a funções que controlam a casa da pessoa que está usando. "
    "Chame as funções quando achar que deve, mas nunca exponha o código delas. "
    "Assuma que a pessoa é amigável e ajude-a a entender o que aconteceu se algo der errado "
    "ou se você precisar de mais informações. Não esqueça de, de fato, chamar as funções."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=initial_prompt,
    tools=[good_morning, intruder_alert, set_light_values, start_music],
)
chat = model.start_chat(enable_automatic_function_calling=True)


def upload_files(message: Any) -> list[Any]:
    uploaded_files = []
    if message["files"]:
        for file_gradio_data in message["files"]:
            uploaded_file = genai.upload_file(file_gradio_data)
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(5)
                uploaded_file = genai.get_file(uploaded_file.name)
            uploaded_files.append(uploaded_file)
    return uploaded_files


def assemble_prompt(message: Any) -> list[Any]:
    prompt = [message["text"]]
    uploaded_files = upload_files(message)
    prompt.extend(uploaded_files)
    return prompt


def gradio_wrapper(message: Any, _history: Any) -> LiteralString:
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
        fn=gradio_wrapper,
        title="Chatbot com Suporte a Arquivos 🤖",
        multimodal=True,
    )
    chat_interface.launch()


if __name__ == "__main__":
    main()
