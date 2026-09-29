import asyncio

from agents import Runner, set_tracing_disabled

from support_agents import billing_agent

# Tracing uploads run data to OpenAI, which needs an OpenAI key. We only use Groq.
set_tracing_disabled(True)


async def main() -> None:
    """Send a single question to the billing support agent."""
    result = await Runner.run(billing_agent, "Kartımdan iki kere ödeme alınmış.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
