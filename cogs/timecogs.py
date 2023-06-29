import discord
from discord.ext import commands
from datetime import datetime
import pytz


class Time(commands.Cog, name="Time", description="Commands related to time"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="time", help="Get the current time in EST")
    async def time(self, ctx):
        async with ctx.typing():
            # Get the current time in UTC
            utc_now = datetime.now(pytz.utc)

            # Convert the UTC time to Eastern Standard Time (EST)
            est_timezone = pytz.timezone("US/Eastern")
            est_time = utc_now.astimezone(est_timezone)

            # Format the time as a string
            time_string = est_time.strftime("%Y-%m-%d %H:%M:%S")
            embed = discord.embeds.Embed(
                colour=discord.Colour.purple(),
            )
            # embed.set_author(name="The Archer Queen")
            embed.add_field(name="Current Time (EST)", value=time_string, inline=True)
            embed.set_footer(text=f"Generated by The Archer Queen")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Time(bot))
