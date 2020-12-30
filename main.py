import discord
from discord.ext import commands
import os
import time


from utilities.utils import NotConnectedToAnyServerWarning

from fun_zone.games.games import Games
from fun_zone.games.chess import ForbiddenChessMove

from cogs.status import Status
from cogs.miscellaneous_commands import MiscellaneousCommands
from cogs.admin_commands import AdminCommands
from cogs.voting import Voting
from cogs.help_command.help import Help
from cogs.calendar import Calendar


print('Initialisation started. All modules are loaded.')

start_time = time.perf_counter()
# Discord token is stored in a .env file in the same directory as the bot.
TOKEN = os.getenv('DISCORD_TOKEN')

# Debug mode will disable most functions and most operations in on_message for a smooth testing experience.
DEBUG = False
if not DEBUG:
    prefix = "/"
else:
    prefix = "="

COGS = [Status,  # Bot status, disable, enable, ping ...
        Games,  # Cog containing the different games implemented in the bot
        AdminCommands,  # Admin only or admin and dev only commands
        MiscellaneousCommands,  # Other commands not fit for a separate Cog
        Voting,  # Voting commands
        Help,  # The help command
        ]

# Setup the bot. Commands are case insensitive. The bot uses all intents.
# The standard implementation of a help command is disabled. A custom one is used.
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None, intents=discord.Intents.all())

# Add these variables to the global bot scope
bot.start_time = time.perf_counter()
bot.debug = DEBUG
bot.enabled = False


# Print a message if the bot is online and change it's status.
@bot.event
async def on_ready():
    bot.start_time = time.perf_counter()
    bot.enabled = True
    bot.debug = DEBUG
    await bot.change_presence(activity=discord.Game('Technical Minecraft on HammerSMP'))
    guilds = bot.guilds

    print('----------------------------------------------------------')
    print('Bot connected with prefix: "{}"'.format(bot.command_prefix))
    if bot.debug:
        print('    > Debug mode is enabled.\n')

    print('The bot has connected to the following servers:')
    if not guilds:
        print("    > !! The bot isn't connected to any server. !!")

    for server in guilds:
        print('    > {}'.format(server.name))

    print('\non_ready took {} s'.format(time.perf_counter() - bot.start_time))
    print('Complete initialisation took {} s'.format(time.perf_counter() - start_time))
    print('----------------------------------------------------------')

    if not guilds:
        raise NotConnectedToAnyServerWarning


# This will handle some errors and suppress raising them. It will also report to the user what the error was.
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("This command doesn't exist", delete_after=15)

    elif isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!", delete_after=15)

    elif isinstance(error, discord.ext.commands.MissingRole):
        await ctx.send("You don't have the correct role to use that command!", delete_after=15)

    elif isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("I'm afraid you aren't allowed to use that command.", delete_after=15)

    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        if isinstance(error.original, ForbiddenChessMove):
            await ctx.send("This is not a valid move!", delete_after=15)

        else:
            print('unknown error: {} of type {}'.format(error, type(error)))
            await ctx.channel.send(error)
            if bot.debug:
                raise error

    else:
        print('unknown error: {} of type {}'.format(error, type(error)))
        await ctx.channel.send(error)
        if bot.debug:
            raise error

try:
    for cog in COGS:
        bot.add_cog(cog(bot))
    print('All cogs are initialised.')
    print('Starting main loop ...')
    bot.loop.run_until_complete(bot.start(TOKEN))

except KeyboardInterrupt:
    print('KeyboardInterrupt: stopping main loop.')

finally:
    bot.loop.run_until_complete(bot.logout())
    print("done")
