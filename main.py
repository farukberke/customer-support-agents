import asyncio

from agents import Runner, set_tracing_disabled

from support_agents import technical_agent

# Tracing uploads run data to OpenAI, which needs an OpenAI key. We only use Groq.
set_tracing_disabled(True)


async def main() -> None:
    """Send a single question to the technical support agent."""
    result = await Runner.run(technical_agent, "Uygulama açılmıyor.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
