import os

from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

from tools import (
    cancel_subscription,
    check_service_status,
    create_billing_ticket,
    create_technical_ticket,
    get_subscription_info,
    reset_password,
)

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

billing_agent = Agent(
    name="Billing Support Agent",
    instructions=(
        "You handle payments, subscriptions and invoices. "
        "Use get_subscription_info to look up the plan, payments and invoices. "
        "Use cancel_subscription only when the customer clearly asks to cancel. "
        "For duplicate charges or refunds, check the payments first, then open a ticket "
        "with create_billing_ticket. "
        "Reply with a short summary of what you found and did."
    ),
    tools=[get_subscription_info, cancel_subscription, create_billing_ticket],
    model=model,
)

# as_tool() wraps a whole agent as a tool. When the manager calls it, the SDK
# runs the specialist in its own agent loop and returns its final output
# to the manager as the tool result. The manager keeps control of the conversation.
manager_agent = Agent(
    name="Customer Support Manager",
    instructions=(
        "You are the customer support manager of Acme Cloud. "
        "Decide which specialist can help and call it with a clear description of the request:\n"
        "- technical_support: login problems, app errors, passwords, service status\n"
        "- billing_support: payments, subscriptions, invoices, refunds\n"
        "- general_support: company info, support hours, contact details\n"
        "Don't make up account details, always ask a specialist. "
        "You can answer greetings and small talk yourself. "
        "Write the final answer to the customer yourself, in the customer's language, "
        "short and friendly."
    ),
    tools=[
        technical_agent.as_tool(
            tool_name="technical_support",
            tool_description="Handles technical problems like login issues, app errors and password resets.",
        ),
        billing_agent.as_tool(
            tool_name="billing_support",
            tool_description="Handles payments, subscriptions, invoices and refunds.",
        ),
        general_agent.as_tool(
            tool_name="general_support",
            tool_description="Answers general questions about the company, support hours and contact info.",
        ),
    ],
    model=model,
)
