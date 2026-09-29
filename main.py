import asyncio

from agents import Runner, ToolCallItem, TResponseInputItem, set_tracing_disabled

from support_agents import manager_agent

# Tracing uploads run data to OpenAI, which needs an OpenAI key. We only use Groq.
set_tracing_disabled(True)


async def main() -> None:
    """Chat with the manager agent until the user types exit or quit."""
    print("Customer Support System (type 'exit' or 'quit' to leave)")
    history: list[TResponseInputItem] = []

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        result = await Runner.run(manager_agent, history)

        for item in result.new_items:
            if isinstance(item, ToolCallItem):
                print(f"  [manager called {item.raw_item.name}]")

        print(f"\nAssistant: {result.final_output}")

        # to_input_list() returns the old input plus everything from this run,
        # so the manager remembers earlier turns.
        history = result.to_input_list()


if __name__ == "__main__":
    asyncio.run(main())
