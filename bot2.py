import discord
from discord.ext import commands
import aiosqlite
from config.data import token
bot = commands.Bot(command_prefix='!')

async def create_db():
    async with aiosqlite.connect('levels.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS levels (
                user_id INTEGER PRIMARY KEY,
                level INTEGER,
                xp INTEGER
            )
        ''')

@bot.event
async def on_ready():
    print('Bot is ready!')
    await create_db()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    async with aiosqlite.connect('levels.db') as db:
        user_id = message.author.id
        row = await db.execute('SELECT level FROM levels WHERE user_id = ?', (user_id,))
        data = await row.fetchone()

        if data is None:
            await db.execute('INSERT INTO levels (user_id, level) VALUES (?, ?)', (user_id, 1))
            await db.commit()
        else:
            level = data[0] + 1
            await db.execute('UPDATE levels SET level = ? WHERE user_id = ?', (level, user_id))
            await db.commit()

    await bot.process_commands(message)

@bot.slash_command()
async def level(ctx):
    async with aiosqlite.connect('levels.db') as db:
        user_id = ctx.author.id
        row = await db.execute('SELECT level FROM levels WHERE user_id = ?', (user_id,))
        data = await row.fetchone()

        if data is None:
            await ctx.respond(f'{ctx.author.mention}, you do not have a level yet.')
        else:
            level = data[0]
            await ctx.respond(f'{ctx.author.mention}, your level is {level}.')

bot.run(token)
