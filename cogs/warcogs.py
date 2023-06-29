from datetime import datetime
import discord
from discord.ext import commands
import requests
import json
import aiohttp


from dotenv import load_dotenv
import os

load_dotenv()
coc_token = os.getenv("COC_API_KEY")

# main_channel_id = 1122515743657971758


def check_war_status():
    headers = {
        "Authorization": f"Bearer {coc_token}",
    }
    url = "https://api.clashofclans.com/v1/clans/%23292VVLJY0/currentwar"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        state = data["state"]

        # When War is Over
        if data["state"] == "warEnded":
            opponents = data["opponent"]["name"]
            our_stars = data["clan"]["stars"]
            opponent_stars = data["opponent"]["stars"]
            if our_stars > opponent_stars:
                result = f"We won! {our_stars} > {opponent_stars}"
            elif our_stars < opponent_stars:
                result = f"We lost! {our_stars} stars < {opponent_stars} stars"
            else:
                our_destruction = data["clan"]["destructionPercentage"]
                opponent_destruction = data["opponent"]["destructionPercentage"]
                if our_destruction > opponent_destruction:
                    result = f"We won! {our_destruction}% > {opponent_destruction}%"
                elif our_destruction < opponent_destruction:
                    result = f"We lost! {our_destruction}% < {opponent_destruction}%"
                else:
                    result = f"It's a tie!"
        
        # When searching for a war
        elif data["state"] == "notInWar":
            opponents = "N/A"
            result = f"Not currently in war"
        
        # When War Preparation is ongoing

        # When War Battle Day is ongoing
    else:
        result = f"Error: {response.status_code}"
        print(response.json())
    return result, state, opponents


def get_utc_time(timestamp):
    return datetime.strptime(timestamp, "%Y%m%dT%H%M%S.000Z")


class WarUtils(
    commands.Cog,
    name="War Utilities",
    description="Utilities for helping coordinate wars.",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="warstatus", help="Get the current war status")
    async def warstatus(self, ctx):
        result, state, opponents = check_war_status()
        if state == "warEnded":
            embed = discord.embeds.Embed(
                colour=discord.Colour.purple(),
                title="War has Ended!",
            )
            embed.add_field(
                name=f"PurpleValkyries vs {opponents}", value=result, inline=True
            )
            await ctx.send(embed=embed)
        elif state == "notInWar":
            embed = discord.embeds.Embed(
                colour=discord.Colour.purple(),
                title="War Status",
            )
            embed.set_image(
                url="https://api-assets.clashofclans.com/badges/200/iNp9fzLTN7FKaCUCc5UOjQhUvRUloa9J-bihgyWwMxQ.png"
            )
            embed.add_field(name=f"PurpleValkyries", value=result, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Something's wrong")

    async def send_all_player_embed(self, channel, players):
        available_players_full = players
        if len(available_players_full) > 26:
            available_players = available_players_full[:25]
            available_players2 = available_players_full[25:]
            embed1 = discord.Embed(
                colour=discord.Colour.purple(),
                title="Available for War - 1",
            )
            embed2 = discord.Embed(
                colour=discord.Colour.purple(),
                title="Available for War - 2",
            )
            for player in available_players:
                embed1.add_field(name=f"{player}", value="Available", inline=True)
            for player in available_players2:
                embed2.add_field(name=f"{player}", value="Available", inline=True)
            channel_obj = self.bot.get_channel(channel)
            if channel_obj:
                await channel_obj.send("Hello, channel!")
                await channel_obj.send(embed=embed1)
                await channel_obj.send(embed=embed2)
        else:
            embed = discord.Embed(
                colour=discord.Colour.purple(),
                title="Available for War",
            )
            for player in available_players_full:
                embed.add_field(name=f"{player}", value="Available", inline=True)
            await channel.send(embed=embed)

    @staticmethod
    async def get_available_war_players():
        headers = {
            "Authorization": f"Bearer {coc_token}",
        }
        url = "https://api.clashofclans.com/v1/clans/%23292VVLJY0/members?limit=50"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                available_players = []
                if response.status == 200:
                    print("Thinking...")
                    data = await response.json()
                    players = data["items"]
                    for player in players:
                        headers = {
                            "Authorization": f"Bearer {coc_token}",
                        }
                        playerdata = f"https://api.clashofclans.com/v1/players/%23{player['tag'][1:]}"
                        async with aiohttp.ClientSession() as session:
                            async with session.get(
                                playerdata, headers=headers
                            ) as player_response:
                                if player_response.status == 200:
                                    player_data = await player_response.json()
                                    if player_data["warPreference"] == "in":
                                        available_players.append(player_data["name"])
                                    else:
                                        pass
                                else:
                                    print(player_response.status_code)
                                    print(player_response.json())
                else:
                    result = f"Error: {response.status_code}"
                    print(response.json())
        return available_players

    @commands.command(name="availableforwar", help="Get the list of available players")
    async def availableforwar(self, ctx):
        await ctx.send("Thinking...")
        available_players = await self.get_available_war_players()
        await self.send_all_player_embed(
            ctx.channel, available_players
        )


async def setup(bot):
    await bot.add_cog(WarUtils(bot))
