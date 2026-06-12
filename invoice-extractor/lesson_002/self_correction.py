import json
import anthropic

from pydantic import BaseModel, ValidationError
from json_utils import strip_json_fence

def extract_with_correction(
    client: anthropic.Anthropic,
    model_class: type[BaseModel],
    messages: list,
    system: str,
    model: str = "claude-sonnet-4-6",
    max_corrections: int = 2
) -> BaseModel:
    """Call the LLM and retry with correction message if output is invalid"""
    conversation = list(messages)  # copy to avoid mutating input
    
    for attempt in range(max_corrections + 1):
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system,
            messages=conversation
        )
        raw = strip_json_fence(response.content[0].text)
        
        try:
            data = json.loads(raw)
            return model_class(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == max_corrections:
                raise ValueError(f"Model failed after {max_corrections} corrections: {e}")
            
            #Append bad response + correction request to conversation
            conversation.append({"role": "assistant", "content": response.content[0].text})
            conversation.append({
                "role": "user",
                "content": (
                    f"Your response was invalid. Error: {e}\n\n"
                    f"Return ONLY valid JSON with no prose or fences. try again."
                )
            })
            print(f"[correction] attempt {attempt+1}: {type(e).__name__}")