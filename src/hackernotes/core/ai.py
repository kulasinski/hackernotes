from ollama import chat

def extract_tags_from_text(text: str) -> set:
    """Extracts tags from text."""
    
    sys_prompt = """
    You will be given a piece of text that is a note written by the user.
    Your task is to figure out which tags might be a good fit for the note.
    Warning: if the note contains any word preceded by either '#', '@', or '^', you should ignore it.

    Form your response as a JSON array of strings.
    For example, if the note contains the text "I love Python coding", your response should be:
    {
        "tags": ["Python", "coding", #programming"]
    }
    """

    response = ollama_generate(
        sys_prompt=sys_prompt,
        user_prompt=text,
    )

    resp_eval = eval(response)

    if isinstance(resp_eval, dict) and "tags" in resp_eval:
        return set(resp_eval["tags"])
    else:
        raise ValueError("Invalid response format from Ollama API: {}".format(response))

def ollama_generate(sys_prompt: str, user_prompt: str, model_name: str = "llama3.2:latest") -> str:
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
        # format=Country.model_json_schema(),
    )
    return response.message.content