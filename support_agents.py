import os

from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

from tools import check_service_status, create_technical_ticket, reset_password

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

technical_agent = Agent(
    name="Technical Support Agent",
    instructions=(
        "You solve technical problems such as login issues, app crashes and forgotten passwords. "
        "Use check_service_status when the customer can't log in or the app doesn't work. "
        "Use reset_password only if the customer forgot their password and gave an email. "
        "If you can't solve the problem, open a ticket with create_technical_ticket. "
        "Reply with a short summary of what you found and did."
    ),
    tools=[check_service_status, reset_password, create_technical_ticket],
    model=model,
)
