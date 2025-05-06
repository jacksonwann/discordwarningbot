import discord
import asyncio
from bot.moderation_bot import ModerationBot

# Load the token from token.txt
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()
    
intents = discord.Intents.default()
intents.message_content = True

bot = ModerationBot(command_prefix="!", intents=intents)

async def main():
    # Start the bot in the background
    await bot.start(TOKEN)

# Start a separate coroutine that will shut down after 10 seconds
async def shutdown_after_delay():
    await asyncio.sleep(10)  # wait 10 seconds
    print("Shutting down bot after 10 seconds...")
    await bot.close()

# Combine both in the event loop
async def runner():
    asyncio.create_task(shutdown_after_delay())  # schedule shutdown
    await main()

if __name__ == "__main__":
    asyncio.run(runner())
