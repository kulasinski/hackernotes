from typing import List

from ollama import chat

from hackernotes.utils.datetime import now

from ..core.types import Entity, EntityType, ExtractedEntities, ExtractedTimeIntelligence, TimeIntelligence, TimeScope

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
    
def extract_entities_from_text(text: str) -> List[Entity]:
    """Extracts entities from text."""
    
    sys_prompt = """
    You will be given a piece of text that is a note written by the user.
    Your task is to figure out which entities might be a good fit for the note.
    Warning: if the note contains any word preceded by either '#', '@', or '^', you should ignore it.

    Your task is to extract entities from the text, if any. 
    Each entity must be of the following types: {}

    Structure your response as a JSON object.
    """\
    .format(EntityType.to_str)

    response = ollama_generate(
        sys_prompt=sys_prompt,
        user_prompt=text,
        format=ExtractedEntities.model_json_schema()
    )

    resp_eval = ExtractedEntities.model_validate_json(response)

    if resp_eval:
        try:
            entities = resp_eval.entities
            return entities
        except AttributeError:
            raise ValueError("Invalid response format from Ollama API: {}".format(response))
    else:
        raise ValueError("Invalid response format from Ollama API: {}".format(response))

def extract_time_intelligence_from_text(text: str) -> List[TimeIntelligence]:
    """Extracts time intelligence from text."""
    
    sys_prompt = """
    You will be given a piece of text that is a note written by the user.
    Your task is to figure out which time intelligence might be a good fit for the note.
    Warning: if the note contains any word preceded by either '#', '@', or '^', you should ignore it.

    Your task is to extract time intelligence from the text, if any. 
    Time intelligence tuple constists the following fields:
    - literal: The literal representation of the time intelligence in the note, e.g. "next week".
    - value: The actual value of the time intelligence, e.g. "2023-10-15". Provide it as a string with the format "YYYY-MM-DD HH:mm:SS".
    - scope: The time scope of the intelligence, e.g. "WEEK", "DAY", etc.
    Each time intelligence scope must be of the following types: {}

    Structure your response as a JSON object.

    Note: When figuring out the dattime that is in the future, you MUST take into consideration current date and time.
    ATTENTION: Today is {}.
    """\
    .format(
        TimeScope.to_str(), 
        now(descriptive=True)
    )

    response = ollama_generate(
        sys_prompt=sys_prompt,
        user_prompt=text,
        format=ExtractedTimeIntelligence.model_json_schema()
    )

    resp_eval = ExtractedTimeIntelligence.model_validate_json(response)

    if resp_eval:
        try:
            time_intelligence = resp_eval.time_intelligence
            return time_intelligence
        except AttributeError:
            raise ValueError("Invalid response format from Ollama API: {}".format(response))
    else:
        raise ValueError("Invalid response format from Ollama API: {}".format(response))

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