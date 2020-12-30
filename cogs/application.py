from discord.ext import commands
import time

import utilities.data as data
from utilities.utils import disable_for_debug


class Application(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('> {} Cog Initialised. Took {} s'.format('Application', time.perf_counter() - bot.start_time))
        bot.start_time = time.perf_counter()

    @commands.Cog.listener()
    async def on_message(self, message):
        # Make sure the bot doesn't respond to itself.
        if message.author == self.bot.user:
            return

        if self.bot.enabled and not self.bot.debug:
            # Ff a new message is sent in the application forms channel, the bot will automatically add reactions.
            if message.channel.id == data.application_channel:
                for e in data.vote_emotes:
                    await message.add_reaction(self.bot.get_emoji(e))

            await self.bot.process_commands(message)
