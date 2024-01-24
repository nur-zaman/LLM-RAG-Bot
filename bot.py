from interactions import Client, Intents, slash_command, SlashContext, listen,slash_option,OptionType
from dotenv import load_dotenv
import os

from querying import data_querying
from manage_embedding import update_index

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
    response = f'**Input Query**: {input_text}\n\n{response}'
    await ctx.send(response)

@slash_command(name="updatedb", description="Update your information database :)")
async def updated_database(ctx: SlashContext):
    await ctx.defer()
    update = await update_index()
    if update:
        response = f'Updated {sum(update)} document chunks'
    else:
        response = f'Error updating index'
    await ctx.send(response)



bot.start(os.getenv("DISCORD_BOT_TOKEN"))