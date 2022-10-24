import os
import logging
import sqlite3
import random

import discord
from discord.ext import commands

token = os.environ.get("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(
    case_insensitive=True,
    description="/help me",
)

cnx = sqlite3.connect("help.db")

class Connect:
    def __enter__(self):
        cnx = sqlite3.connect("help.db")
        self.cnx = cnx
        return cnx

    def __exit__(self, type, value, traceback):
        self.cnx.close()

@bot.event
async def on_ready():
    await bot.user.edit(username="/help")
    print("/help is ready.")


@bot.check
async def globally_block_guild(ctx):
    return ctx.guild is None


@bot.slash_command(description="Help me")
async def help(ctx):
    help_message = \
"""
/help: doesn't give you the flag
For other commands, please refer to the autocomplete.
"""
    embed = discord.Embed(
        title="/help",
        description=help_message,
        color=discord.Colour.blurple(),
    )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Register for an account or change your username")
async def register(ctx, username:str):
    with Connect() as cnx:
        cursor = cnx.cursor()
        cursor.execute('select 1 from users where id = ?', (ctx.author.id,))
        if len(cursor.fetchall()) == 0:
            welcome = True
            cursor.execute(f"insert into users values (?, '{username}', ?)", (ctx.author.id, 0))
        else:
            welcome = False
            cursor.execute(f"update users set username = '{username}'")
        cnx.commit()
    embed = discord.Embed(
        title="Welcome!" if welcome else "Welcome back!",
        description=f'Hello {username}!',
        colour=discord.Colour.blurple(),
    )
    await ctx.respond(embed=embed)

@bot.slash_command(description="whoami")
async def whoami(ctx):
    with Connect() as cnx:
        cursor = cnx.cursor()
        cursor.execute('select username, money from users where id = ?', (ctx.author.id,))
        if (username := cursor.fetchone()):
            embed = discord.Embed(
                title="whoami",
                description=f"You are {username[0]} the beggar with ${username[1]}",
                colour=discord.Colour.blurple(),
            )
        else:
            embed = discord.Embed(
                title="Error",
                description="Sorry, you haven't registered yourself yet",
                colour=discord.Colour.red(),
            )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Beg for money")
async def beg(ctx):
    with Connect() as cnx:
        cursor = cnx.cursor()
        cursor.execute('select 1 from users where id = ?', (ctx.author.id,))
        if len(cursor.fetchall()) == 0:
            embed = discord.Embed(
                title="Error",
                description="Sorry, you haven't registered yourself yet",
                colour=discord.Colour.red(),
            )
        else:
            money = random.randint(-100, 100)
            cursor.execute('update users set money = money + ? where id = ?', (money, ctx.author.id))
            if money < 0:
                embed = discord.Embed(
                    title="Boo",
                    description=f"Someone didn't like your face and took away ${-money}",
                    colour=discord.Colour.red(),
                )
            elif money == 0:
                embed = discord.Embed(
                    title="Eee",
                    description="Sorry, no spare change",
                    colour=discord.Colour.blurple(),
                )
            else:
                embed = discord.Embed(
                    title="Poor beggar, here's some cash!",
                    description=f"Ok, here's ${money} for you!",
                    colour=discord.Colour.green(),
                )
        cnx.commit()
    await ctx.respond(embed=embed)

@bot.slash_command(description="Window shopping")
async def shop(ctx):
    with Connect() as cnx:
        cursor = cnx.cursor()
        cursor.execute('select name, price from items');
        items = '\n'.join([f'{row[0]} -- ${row[1]}' for row in cursor.fetchall()])
        embed = discord.Embed(
            title="Shop Items",
            description=items,
            colour=discord.Colour.blurple(),
        )
    await ctx.respond(embed=embed)

@bot.slash_command(description="Buy an item")
async def buy(ctx, name:str):
    with Connect() as cnx:
        cursor = cnx.cursor()
        cursor.execute('select money from users where id = ?', (ctx.author.id,))
        if len(balance :=cursor.fetchone()) == 0:
            embed = discord.Embed(
                title="Error",
                description="Sorry, you haven't registered yourself yet",
                colour=discord.Colour.red()
            )
        else:
            cursor.execute(
                "select price from items where name = ?",
                (name,),
            )
            if (price := cursor.fetchone()):
                if (diff := balance[0] - price[0]) >= 0:
                    cursor.execute(
                        'insert into purchases (item_id, user_id) values ((select id from items where name = ?), ?)',
                       (name, ctx.author.id),
                    )
                    cursor.execute(
                        "update users set money = ? where id = ?",
                        (diff, ctx.author.id),
                    )
                    cnx.commit()
                    embed = discord.Embed(
                        title="Bought item",
                        description=f"You bought a {name} for ${price[0]}!",
                        colour=discord.Colour.blurple(),
                    )
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="You're too poor to buy anything",
                        colour=discord.Colour.blurple(),
                    )
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Sorry, this item doesn't exist",
                    colour=discord.Colour.blurple(),
                )
    await ctx.respond(embed=embed)

@bot.slash_command(description="See your inventory")
async def inv(ctx):
    with Connect() as cnx:
        cursor = cnx.cursor()
        cursor.execute("select money from users where id = ?", (ctx.author.id,))
        if (balance := cursor.fetchone()):
            balance = balance[0]
            cursor.execute(
                "select i.name from purchases as p inner join items as i on i.id = p.item_id \
                where p.user_id = ?",
                (ctx.author.id,),
            )
            items = '\n'.join([i[0] for i in cursor.fetchall()])
            embed = discord.Embed(
                title="Inventory",
                description=f"{items}\n Money: ${balance}",
                colour=discord.Colour.blurple(),
            )
    await ctx.respond(embed=embed)

if __name__ == "__main__":
    bot.run(token)
