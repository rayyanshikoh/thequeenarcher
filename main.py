import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")


def prep_mention(id):
    return f"<@{id}>"

description = """A bot created by DeadlyRayyan to improve the user experience of the PurpleValkyries server."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="to $help")
    )
    await bot.load_extension('cogs.timecogs')


@bot.command(name="test", help="Check if the bot is added properly")
async def test(ctx):
    userid = ctx.author.id
    user = prep_mention(userid)
    await ctx.send(f"{user} hello")


bot.run(bot_token)
