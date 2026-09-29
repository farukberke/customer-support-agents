import asyncio

from agents import Runner, set_tracing_disabled

from support_agents import general_agent

# Tracing uploads run data to OpenAI, which needs an OpenAI key. We only use Groq.
set_tracing_disabled(True)


async def main() -> None:
    """Send a single question to the general support agent."""
    result = await Runner.run(general_agent, "Destek saatleriniz nedir?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
