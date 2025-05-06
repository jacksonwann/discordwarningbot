import tkinter as tk
import threading
import asyncio
import discord
from bot.moderation_bot import ModerationBot

# Load the token and channel ID from external files
try:
    with open("token.txt", "r") as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    TOKEN = ""

try:
    with open("channel.txt", "r") as f:
        CHANNEL_ID = int(f.read().strip())
except FileNotFoundError:
    CHANNEL_ID = None

class BotGUI:
    """Simple Tkinter GUI to start/stop/restart the bot and send messages."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Discord Moderation Bot")

        self.start_button = tk.Button(self.root, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=5)

        self.reconnect_button = tk.Button(self.root, text="Reconnect Bot", command=self.reconnect_bot)
        self.reconnect_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=5)

        self.message_label = tk.Label(self.root, text="Enter message to send:")
        self.message_label.pack(pady=5)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.stop_bot)
        self.bot = None
        self.loop = None

    def start_bot(self):
        if not TOKEN:
            self.status_label.config(text="Error: token.txt missing or empty.", fg="red")
            return

        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = ModerationBot(command_prefix='!', intents=intents)

        def run():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(self.bot.start(TOKEN))
            except Exception as e:
                print(f"Error starting bot: {e}")
                self.status_label.config(text=f"Error: {e}", fg="red")

        threading.Thread(target=run, daemon=True).start()
        self.status_label.config(text="Bot is starting...", fg="green")

    def reconnect_bot(self):
        """Stops the bot and restarts it."""
        self.status_label.config(text="Reconnecting bot...", fg="blue")
        self.stop_bot(only_stop=True)
        self.start_bot()

    def send_message(self):
        if not self.bot:
            self.status_label.config(text="Error: Bot not running!", fg="red")
            return

        if CHANNEL_ID is None:
            self.status_label.config(text="Error: channel.txt missing or invalid.", fg="red")
            return

        message = self.message_entry.get()
        if not message:
            self.status_label.config(text="Error: Enter a message first.", fg="red")
            return

        async def send():
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(message)
                self.status_label.config(text="Message sent successfully!", fg="green")
            else:
                self.status_label.config(text="Error: Channel not found.", fg="red")

        asyncio.run_coroutine_threadsafe(send(), self.loop)

    def stop_bot(self, only_stop=False):
        if self.bot and self.loop:
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)
            self.bot = None
            self.loop = None
        if not only_stop:
            self.root.destroy()

    def run(self):
        self.root.mainloop()