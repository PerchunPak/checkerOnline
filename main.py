"""
За основною часть кода спасибо https://github.com/PerchunPak/sunshinedsbot и конечно же https://github.com/NWordCounter/bot
"""
from discord.ext import commands
from discord import Intents, Status, Activity, ActivityType, Client
from psutil import Process
from asyncio import sleep as asynSleep

from datetime import datetime
from os import getpid

from mcstatus import MinecraftServer

TOKEN = ''

bot_intents = Intents.default()
bot_intents.members = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="пингер онлайна",
    case_insensitive=True,
    help_command=None,
    status=Status.invisible,
    intents=bot_intents,
    fetch_offline_members=True
)

bot.process = Process(getpid())
bot.ready_for_commands = False


@bot.event
async def on_connect():
    print('\nУстановлено соеденение с дискордом')


@bot.event
async def on_ready():

    print('\nЗашел как:\n'
         f'{bot.user}\n'
         f'{bot.user.id}\n'
          '-----------------\n'
         f'{datetime.now().strftime("%m/%d/%Y %X")}\n'
          '-----------------\n'
         f'Шардов: {str(bot.shard_count)}\n'
         f'Серверов: {str(len(bot.guilds))}\n'
         f'Пользователей: {str(len(bot.users))}\n'
          '-----------------\n')

    bot.ready_for_commands = True
    bot.started_at = datetime.utcnow()
    bot.app_info = await bot.application_info()

    await bot.change_presence(status=Status.online, activity=Activity(
        name='скоро пингану онлайн', type=ActivityType.playing))

    while True: # собственно код программы
        ping = MinecraftServer.lookup('localhost:25566') # айпи сервера1, тут это main сервер
        main = ping.status()
        ping = MinecraftServer.lookup('localhost:25567') # айпи сервера2, тут это rpg сервер
        rpg = ping.status()
        online = str(main.players.online + rpg.players.online)
        print('Онлайн: ' + online)
        
        await bot.change_presence(status=Status.online, activity=Activity(
            name=f'онлайн {online}', type=ActivityType.playing))

        if int(online) <= 3:
            owner = bot.get_user(bot.app_info.owner)
            await owner.send(f'**Онлайн {online} так что готовься**')
        elif int(online) <= 5:
            owner = bot.get_user(bot.app_info.owner)
            await owner.send(f'**Онлайн {online} так что делай что хотел**')
        await asynSleep(300) # time.sleep не подходит тк останавливает все процессы





try:
    bot.loop.run_until_complete(bot.start(TOKEN))
except KeyboardInterrupt:
    print("\nЗакрытие")
    bot.loop.run_until_complete(bot.change_presence(status=Status.invisible))
    for e in bot.extensions.copy():
        bot.unload_extension(e)
    print("Выходим")
    bot.loop.run_until_complete(Client.close())
finally:
    print("Закрыто")
