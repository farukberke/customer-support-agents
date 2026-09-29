import gradio as gr
from agents import Runner, ToolCallItem, TResponseInputItem, set_tracing_disabled

from support_agents import manager_agent

# Tracing uploads run data to OpenAI, which needs an OpenAI key. We only use Groq.
set_tracing_disabled(True)


async def respond(
    message: str, chat: list[dict], history: list[TResponseInputItem]
) -> tuple[str, list[dict], list[TResponseInputItem]]:
    """Run the manager agent and update the chat window and agent history."""
    history = history + [{"role": "user", "content": message}]
    result = await Runner.run(manager_agent, history)

    answer = result.final_output
    called = [
        item.tool_name
        for item in result.new_items
        if isinstance(item, ToolCallItem) and item.tool_name
    ]
    if called:
        names = ", ".join(f"`{name}`" for name in dict.fromkeys(called))
        answer += f"\n\n---\n**Specialists used:** {names}"

    chat = chat + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ]
    return "", chat, result.to_input_list()


with gr.Blocks(title="Customer Support Agents") as demo:
    gr.Markdown("# Customer Support Agents")
    chatbot = gr.Chatbot(height="80vh")
    # The agent history also keeps tool calls, so it is stored separately from the chat window.
    history = gr.State([])
    textbox = gr.Textbox(placeholder="Type your message...", show_label=False)
    gr.Examples(
        [
            "Kartımdan iki kere ödeme alınmış.",
            "Uygulamaya giriş yapamıyorum.",
            "Şifremi unuttum, mailim ali@example.com",
            "Destek saatleriniz nedir?",
        ],
        inputs=textbox,
    )
    gr.ClearButton([chatbot, textbox, history])

    textbox.submit(respond, [textbox, chatbot, history], [textbox, chatbot, history])


if __name__ == "__main__":
    demo.launch()
