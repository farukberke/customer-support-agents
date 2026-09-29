import asyncio

from agents import Runner, ToolCallItem, set_tracing_disabled

from support_agents import manager_agent

# Tracing uploads run data to OpenAI, which needs an OpenAI key. We only use Groq.
set_tracing_disabled(True)


async def main() -> None:
    """Send a single question to the manager agent."""
    result = await Runner.run(manager_agent, "Kartımdan iki kere ödeme alınmış.")

    for item in result.new_items:
        if isinstance(item, ToolCallItem):
            print(f"[manager called {item.raw_item.name}]")

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
