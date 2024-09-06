import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import os


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "abis-345004")
LOCATION = os.getenv("REGION", "us-central1")
MODEL = "gemini-1.5-flash-001" # this is selectable 

vertexai.init(project=PROJECT_ID, location=LOCATION)

prompt_template = """
    {prompt}
    <Code>
    {code}
    """

def count_tokens(prompt: str, code: str) -> int:
    model = GenerativeModel(MODEL)
    response = model.count_tokens(prompt_template.format(prompt=prompt, code=code))

    return response.total_tokens

def evaluate_code(prompt: str, code: str) -> dict:
    model = GenerativeModel(MODEL)
    generation_config = GenerationConfig() #add in placeholders here, seed value and low temp

    response = model.generate_content(
        prompt_template.format(prompt=prompt, code=code),
        generation_config=generation_config,
    )

    return response.text


