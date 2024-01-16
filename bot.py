from interactions import Client, Intents, slash_command, SlashContext, listen,slash_option,OptionType
from dotenv import load_dotenv
import os

from querying import data_querying

load_dotenv()


bot = Client(intents=Intents.ALL)


@listen() 
async def on_ready():
    print("Ready")
    # print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    # This event is called when a message is sent in a channel the bot can see
    print(f"message received: {event.message.content}")


@slash_command(name="query", description="Enter your query :)")
@slash_option(
    name="input_text",
    description="input text",
    required=True,
    opt_type=OptionType.STRING,
)
async def get_response(ctx: SlashContext, input_text: str):
    await ctx.defer()
    response = await data_querying(input_text)
    await ctx.send(response)


bot.start(os.getenv("DISCORD_BOT_TOKEN"))