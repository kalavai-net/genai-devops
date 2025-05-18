import asyncio

from llama_index.llms.openai_like import OpenAILike
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.core.agent.workflow import AgentStream, ToolCallResult


def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


llm = OpenAILike(model="qwen-qwen2-5-7b-instruct-awq", api_key="sk--BnVfdA8bKzGPjr-JWYlzw", api_base="https://api.cogenai.kalavai.net/v1")
agent = ReActAgent(
    tools=[multiply, add],
    llm=llm,
    system_prompt="You are a helpful assistant that can help with mathematical operations.",
)
ctx = Context(agent)


async def main():

    handler = agent.run("What is 20+(2*4)?", ctx=ctx)

    async for ev in handler.stream_events():
    # if isinstance(ev, ToolCallResult):
    #     print(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
        if isinstance(ev, AgentStream):
            print(f"{ev.delta}", end="", flush=True)

    response = await handler
    print(response)
    print(response.tool_calls)

if __name__ == "__main__":
    asyncio.run(main())
