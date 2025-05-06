import unittest
import asyncio
import discord
from bot.moderation_bot import ModerationBot

class BotCommandTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = ModerationBot(command_prefix='!', intents=intents)

        # Run the bot for just enough time to sync commands
        self.bot_task = asyncio.create_task(self.bot.start_bot_for_test())

    async def asyncTearDown(self):
        await self.bot.close()
        if not self.bot_task.done():
            self.bot_task.cancel()

    async def test_command_names(self):
        # Wait until bot is ready
        await self.bot.wait_until_ready()

        # Check that slash commands are registered
        commands = [cmd.name for cmd in self.bot.tree.get_commands()]
        expected = {"ping", "warn", "warnings", "clearwarnings"}
        self.assertTrue(expected.issubset(set(commands)), "Not all expected commands are registered!")

# Add test mode method to your bot
def patch_bot_start_method():
    async def start_bot_for_test(self):
        await self.login(open("token.txt").read().strip())
        await self.connect()
    setattr(ModerationBot, "start_bot_for_test", start_bot_for_test)

patch_bot_start_method()

if __name__ == '__main__':
    unittest.main()