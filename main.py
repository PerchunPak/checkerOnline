from discord.ext import commands, tasks
import discord
import psutil
import asyncio

import datetime
import os

import mcstatus

TOKEN = ''

bot_intents = discord.Intents.default()
bot_intents.members = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="пингер онлайна",
    case_insensitive=True,
    help_command=None,
    status=discord.Status.invisible,
    intents=bot_intents,
    fetch_offline_members=True
)

bot.process = psutil.Process(os.getpid())
bot.ready_for_commands = False


@bot.event
async def on_connect():
    print("\nУстановлено соеденение с дискордом")


@bot.event
async def on_ready():

    print("\nЗашел как:")
    print(bot.user)
    print(bot.user.id)
    print("-----------------")
    print(datetime.datetime.now().strftime("%m/%d/%Y %X"))
    print("-----------------")
    print("Шардов: " + str(bot.shard_count))
    print("Серверов: " + str(len(bot.guilds)))
    print("Пользователей: " + str(len(bot.users)))
    print("-----------------\n")

    bot.ready_for_commands = True
    bot.started_at = datetime.datetime.utcnow()
    bot.app_info = await bot.application_info()

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        name='скоро пингану онлайн', type=discord.ActivityType.playing))

    while True:
        ping = mcstatus.MinecraftServer.lookup('localhost:25566')
        main = ping.status()
        ping = mcstatus.MinecraftServer.lookup('localhost:25567')
        rpg = ping.status()
        online = str(main.players.online + rpg.players.online)
        print('Онлайн: ' + online)
        
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
            name=f'онлайн {online}', type=discord.ActivityType.playing))

        if int(online) <= 5:
            owner = bot.get_user(379353300887273472)
            await owner.send(f'**Онлайн {online} так что поднимай свою жопу и иди готовится к переносу**')
        elif int(online) <= 3:
            owner = bot.get_user(379353300887273472)
            await owner.send(f'**Онлайн {online} так что поднимай свою жопу и иди переносить пландб**')
        await asyncio.sleep(300)





try:
    bot.loop.run_until_complete(bot.start(TOKEN))
except KeyboardInterrupt:
    print("\nЗакрытие")
    bot.loop.run_until_complete(bot.change_presence(status=discord.Status.invisible))
    for e in bot.extensions.copy():
        bot.unload_extension(e)
    print("Выходим")
    bot.loop.run_until_complete(discord.Client.close())
finally:
    print("Закрыто")
