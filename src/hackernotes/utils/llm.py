import logging

from ollama import chat

logging.getLogger("httpx").setLevel(logging.WARNING)

def ollama_generate(sys_prompt: str, user_prompt: str, model_name: str = "llama3.2:latest", format: dict = None) -> str:
    """Generates a response using the Ollama API."""
    response = chat(
        messages=[
            {
                'role': 'system',
                'content': sys_prompt,
            },
            {
                'role': 'user',
                'content': user_prompt,
            }
        ],
        model=model_name,
        format=format,
    )
    return response.message.content