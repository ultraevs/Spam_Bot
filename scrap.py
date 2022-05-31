import random
import time
import traceback

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, \
    ChatAdminRequiredError, FloodWaitError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# Взять api_id и api_hash можно на сайте my.telegram.org
api_id = # Введите ваш api_id
api_hash = # Введите ваш api_hash(нужно ввести его в кавычки)

client = TelegramClient('scraper', api_id, api_hash)

client.start()
f = open('id.txt', 'w', encoding='utf-8')  # создание файла с данными юезров(название id.txt)


# функция скраппинга группы
async def get_users(channel):  # chanel - ссылка на канал, которая передается из функции main в переменной url_in
    offset_user = 0
    limit_user = 100

    all_users = []
    filter_user = ChannelParticipantsSearch('')
    print('Сбор данных начат...')
    while True:
        participants = await client(GetParticipantsRequest(channel,
                                                           filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_users.extend(participants.users)
        offset_user += len(participants.users)

    for i in all_users:
        f.write(str(i.id))
        f.write(' ')
        f.write(str(i.access_hash))
        f.write(' ')
        f.write(str(i.first_name))
        f.write(' ')
        f.write(str(i.last_name))
        f.write(' ')
        f.write(str(i.username))
        f.write('\n')
    f.close()
    print('Сбор данных окончен.')


# функция рассылки
async def send(text):  # text - текст сообщения
    users = []
    with open(r"id.txt", encoding='UTF-8') as r:
        while True:
            user = {}
            u = r.readline().split()
            if not u:
                break
            user['id'] = int(u[0])
            user['access_hash'] = int(u[1])
            user['first'] = u[2]
            user['last'] = u[3]
            user['username'] = u[4]
            users.append(user)
        r.close()

    n = 0
    for user in users:
        n += 1
        if n % 80 == 0:
            time.sleep(60)
        try:
            print("Отправляем сообщение для {}".format(user['id']))
            await  client.send_message(user['id'], text)
            print("Ожидаем 30-60сек...")
            time.sleep(random.randrange(60, 90  )) # строка устанавливающая рандомное число задержки в указанном пределе(по умлочание это будет рандомное число от 60 до 90)
        except PeerFloodError:
            print(
                "Получаю сообщение об ошибке Flood от telegram. Crhgbn сейчас останавливается."
                " Пожалуйста, повторите попытку через некоторое время.")
            print("Ожидаем 100сек...")
            time.sleep(100)
        except UserPrivacyRestrictedError:
            print("Настройки конфиденциальности пользователя не позволяют вам этого делать. Пропускаю.")
            print("Ожидаем 5сек...")
            time.sleep(random.randrange(0, 5))
        except UserNotMutualContactError:
            print("Настройки конфиденциальности пользователя не позволяют вам этого делать. Пропускаю.")
            print("Ожидаем 5сек...")
            time.sleep(random.randrange(0, 5))
        except ChatAdminRequiredError:
            print("Для этого в указанном чате требуются права администратора чата")
            print("Ожидаем 5сек...")
            time.sleep(random.randrange(0, 5))
        except FloodWaitError as r:
            print("Flood error")
            print(r)
        except:
            traceback.print_exc()
            print("Неожиданная ошибка")
            print('Всего обработано {} человек'.format(n))
    print('Работа завершена\nВсего обработано {} человек'.format(n))

