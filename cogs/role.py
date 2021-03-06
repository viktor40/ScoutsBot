# HammerBotPython
# other module
# role.py

"""
role.py handles giving certain roles that members are allowed to give themselves.
These roles are used for notification and pinging purposes.
"""

import discord
from discord.ext import commands
import time

from utilities.data import role_list, role_ids, hammer_guild
from utilities.utils import get_server_roles
import cogs.help_command.help_data as hd
import utilities.data as data
from utilities.utils import disable_for_debug


class Role(commands.Cog):
    """
    This cog is used to implement the role command.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot
        print("> {} Cog Initialised. Took {} ss".format('Role', time.perf_counter() - bot.start_time))
        bot.start_time = time.perf_counter()

    async def valid_argument(self, ctx, action, args):
        """
        This will check if the arguments provided are valid

        :param ctx: The context variable of the command.
        :param action: The action to be performed (can be list, add or remove).
        :param args: A tuple containing *args
        :return: A boolean showing whether the test passed or not.
        """
        if action.lower() not in ['list', 'add', 'remove']:
            response = 'Invalid action.'
            await ctx.send(response)
            return False

        if not args:
            response = 'You have not specified a role'
            await ctx.send(response)
            return False

        return True

    async def user_has_role(self, ctx, action, role):
        """
        This method checks whether the user already has a role they're trying to add or doesn't have a role
        they're trying to remove.

        :param ctx: The context variable of the command.
        :param action: The action to be performed (can be list, add or remove).
        :param role: The role that the user is trying to add.
        :return: A boolean showing whether the test passed or not.
        """
        has_role = self.bot.get_guild(hammer_guild).get_role(role_ids[role]) in ctx.message.author.roles
        if has_role and action == 'add':
            response = 'I am sorry but you already have this role.'
            await ctx.send(response)
            return False

        elif not has_role and action == 'remove':
            response = 'I am sorry but you don\'t have this role.'
            await ctx.send(response)
            return False

        else:
            return True

    async def role_checker(self, ctx, action, args):
        """
        This method will check if the role removal is valid. This means checking if the role exists and checking
        if the user is allowed to add or remove that role.

        :param ctx: The context variable of the command.
        :param action: The action to be performed (can be list, add or remove).
        :param args: A tuple containing *args
        :return: A boolean showing whether the test passed or not.
        """
        if not await self.valid_argument(ctx, action, args):
            return False

        role = ' '.join(args)
        if role not in get_server_roles(ctx):
            a = get_server_roles(ctx)
            response = 'I am sorry but i am afraid that role does not exist.'
            await ctx.send(response)
            return False

        elif role not in role_list:
            response = 'I am sorry but i am afraid you cannot add/remove that role to yourself using the bot.'
            await ctx.send(response)
            return False

        elif not await self.user_has_role(ctx, action, role):
            return False

        else:
            return True

    async def give_role(self, ctx, args):
        """
        This async method will be used to assign a member a the new role, once all checks have passed.

        :param ctx: The context variable of the command.
        :param args: The context variable of the command.
        """
        role = ' '.join(args)
        member = ctx.message.author
        guild_role = self.bot.get_guild(hammer_guild).get_role(role_ids[role])
        await member.add_roles(guild_role)
        response = 'You have been successfully given the role `{}`! Congratulations!'.format(role)
        await ctx.send(response)

    async def remove_role(self, ctx, args):
        """
        This method will remove a role from the user once all checks have passed.

        :param ctx: The context variable of the command.
        :param args: The context variable of the command.
        """
        role = ' '.join(args)
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        guild_role = self.bot.get_guild(hammer_guild).get_role(role_ids[role])  # the role needed to add
        await member.remove_roles(guild_role)
        response = 'The role `{}` has successfully been removed! Congratulations!'.format(role)
        await ctx.send(response)

    @commands.command(name='role', help=hd.role_help, usage=hd.role_usage)
    @commands.has_role(data.member_role_id)
    async def role(self, ctx, action, *args):
        """
        This is the main method for the role command. In here we'll check if the request is valid.
        If so the method will perform the correct action depending on the action passed. It will either list
        the roles you can add, add a role, or remove a role.

        :param ctx: The context variable of the command.
        :param action: The action to be performed (can be list, add or remove).
        :param args: A tuple containing *args
        """
        if not await self.role_checker(ctx, action, args):
            return

        if action == 'list':
            await ctx.send(role_list)
            return

        try:
            await self.give_role(ctx, args) if action == 'add' else await self.remove_role(ctx, args)

        except discord.errors.Forbidden:
            response = 'Missing permissions'
            await ctx.send(response)
