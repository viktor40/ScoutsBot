import discord
from discord.ext import commands
import time


class Calendar(commands.Cog):
    """
    This cog is used to implement some miscellaneous commands.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot
        print('> {} Cog Initialised. Took {} s'.format('Calendar', time.perf_counter() - bot.start_time))
        bot.start_time = time.perf_counter()

