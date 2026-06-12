import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "What is a context window in LLMs?"
            }
    ]
)

print(response.content[0].text)

print(f"Tokens used: {response.usage.input_tokens} in / {response.usage.output_tokens} out")