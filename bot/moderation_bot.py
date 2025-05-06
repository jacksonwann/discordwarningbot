from bot.bot_base import BotBase
from bot.backend import Database
from bot.utils import is_valid_reason
import discord
from discord import app_commands


class ModerationBot(BotBase):
    """
    A Discord bot for basic moderation using slash commands.
    Includes features to warn users, list their warnings,
    and clear warnings with proper permission checks.
    """

    def __init__(self, command_prefix, intents):
        """
        Initialize the bot with command prefix, intents, and database.
        """
        super().__init__(command_prefix, intents)
        self.db = Database()
        self.add_commands()

    def add_commands(self):
        """
        Define all slash commands for the moderation bot.
        """

        @self.tree.command(name="ping", description="Check if the bot is alive.")
        async def ping(interaction: discord.Interaction):
            """Simple ping command to confirm bot responsiveness."""
            try:
                await interaction.response.send_message("\U0001F3D3 Pong!")
            except Exception as e:
                print(f"Error in /ping: {type(e).__name__} - {e}")

        @self.tree.command(name="warn", description="Warn a user with a reason.")
        async def warn(
            interaction: discord.Interaction,
            user: discord.Member,
            reason: str
        ):
            """Warn a user and save the reason in the database."""
            if not is_valid_reason(reason):
                await interaction.response.send_message(
                    "❌ Reason must be 5–100 characters and contain only allowed punctuation.",
                    ephemeral=True
                )
                return

            try:
                self.db.add_warning(user.id, reason)
                await interaction.response.send_message(
                    f"⚠️ Warned {user.name} for: {reason}"
                )
            except Exception as e:
                print(f"Error in /warn: {type(e).__name__} - {e}")
                await interaction.response.send_message("❌ Failed to warn user.")

        @self.tree.command(name="warnings", description="Show warnings for a user.")
        async def warnings(
            interaction: discord.Interaction,
            user: discord.Member
        ):
            """List all warnings recorded for a specific user."""
            try:
                warns = self.db.get_warnings(user.id)
                if warns:
                    formatted = "\n".join(f"- {w}" for w in warns)
                    await interaction.response.send_message(
                        f"📋 {user.name} has {len(warns)} warning(s):\n{formatted}"
                    )
                else:
                    await interaction.response.send_message(
                        f"✅ {user.name} has no warnings."
                    )
            except Exception as e:
                print(f"Error in /warnings: {type(e).__name__} - {e}")
                await interaction.response.send_message("❌ Failed to retrieve warnings.")

        @self.tree.command(
            name="clearwarnings",
            description="Clear all warnings for a user. (Mods/Admins Only)"
        )
        async def clear_warnings(
            interaction: discord.Interaction,
            user: discord.Member
        ):
            """Clear all warnings for a user (requires moderator permissions)."""
            if not interaction.user.guild_permissions.manage_messages and \
                    not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "🚫 You don't have permission to use this command.",
                    ephemeral=True
                )
                return

            try:
                self.db.clear_warnings(user.id)
                await interaction.response.send_message(
                    f"🧹 Cleared all warnings for {user.name}."
                )
            except Exception as e:
                print(f"Error in /clearwarnings: {type(e).__name__} - {e}")
                await interaction.response.send_message("❌ Failed to clear warnings.")

        @self.event
        async def on_ready():
            """
            Called when the bot is ready. Syncs all slash commands with Discord.
            """
            print(f"Logged in as {self.user} (ID: {self.user.id})")
            try:
                synced = await self.tree.sync()
                print(f"✅ Synced {len(synced)} slash command(s) globally.")
            except Exception as e:
                print(f"Error syncing commands: {type(e).__name__} - {e}")