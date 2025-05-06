import discord
from discord.ext import commands

class BotBase(commands.Bot):
    """Base class for the bot demonstrating OOP and Encapsulation."""

    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')