import os

from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Groq exposes an OpenAI-compatible Chat Completions API,
# so the SDK's regular OpenAI client can talk to it.
groq_client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
model = OpenAIChatCompletionsModel(model="openai/gpt-oss-20b", openai_client=groq_client)

general_agent = Agent(
    name="General Support Agent",
    instructions=(
        "You answer general questions about Acme Cloud, a company that sells "
        "cloud storage and file sharing subscriptions. "
        "Support hours are Monday to Friday, 09:00-18:00 (UTC+3). "
        "Customers can reach support at support@acmecloud.example or +90 212 555 00 00. "
        "Keep answers short."
    ),
    model=model,
)
