from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import chainlit as cl
import httpx, os
from dotenv import load_dotenv
#place secrets in a .env file

load_dotenv()

model = OpenAIModel(
    'google/gemini-2.5-flash-lite',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
        http_client=httpx.AsyncClient(verify=False)
    ),
)



simple_agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=(
        'Please answer everything in traditional chinese'
        'You are an expert in geography, history and culture.'
        'You are helpful and courteous.'
        'You are concise and to the point.'
        
    
    ),
)
@cl.on_chat_start
def on_start():
    cl.user_session.set("agent", simple_agent)

@cl.on_message #decorator
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.run_sync(message.content)
    await cl.Message(content=response.output).send()