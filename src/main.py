import gspread
import schedule
import asyncio
import time
import os
from datetime import datetime
from threading import Thread
from telethon.sync import TelegramClient, events
from telethon import errors

GSPREAD_CREDENTIALS_JSON_FILE = os.getenv('GSPREAD_CREDENTIALS_JSON_FILE', 'credentials.json')
GSPREAD_NAME = os.getenv('GSPREAD_NAME', 'TREND_SECURITY')

TG_API_ID = os.getenv('TG_API_ID', '1114086')
TG_API_HASH = os.getenv('TG_API_HASH', '4960eb9dcee82fca3178a37dc8e360ed')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', '6968043363:AAGPkLQ7Ncc1MMCh7u3HY8xn_ndzXm9C3k8')
TG_ADMIN_CHANNEL_ID = os.getenv('TG_ADMIN_CHANNEL_ID', -4063207053)
FIND_TIME = os.getenv('FIND_TIME', '21:00')

# Functions
def findUserByLogin(employees, login_to_find):
  for employee in employees:
    if employee['Логин TG'] == login_to_find:
      # Пользователь найден
      return True

def telegramClientReconnect(client):
  try:
    client.start(bot_token=TG_BOT_TOKEN)
    return client
  except ConnectionError:
    # Обрыв соединения, переподключаемся
    telegramClientReconnect(client)

def checkUsers(client):
  connected = telegramClientReconnect(client)

  # Креды к Google Excel в формате JSON
  gc = gspread.service_account(filename=GSPREAD_CREDENTIALS_JSON_FILE)
  # Открываем таблицу
  sh = gc.open(GSPREAD_NAME)

  # Получаем значения листов Employees и Chats
  worksheetEmployees = sh.worksheet("Employees")
  worksheetEmployeesVars = worksheetEmployees.get_all_records()

  # Получаем список ID всех чатов
  worksheetChats = sh.worksheet("Chats")
  worksheetChatsVars = worksheetChats.get_all_records()

  for chat_id in worksheetChatsVars:
    chatId = chat_id['ID']

    participants = connected.get_participants(chatId)
    for participant in participants:
      user = participant.username

      if participant.bot:
        continue

      result = findUserByLogin(worksheetEmployeesVars, user)
      if (not result):
        # Удаляем пользователя из группы
        try:
          channel_entity = connected.get_entity(chatId)
          connected.kick_participant(chatId, participant.id)
          print(
            f"User {user} removed from the group {chatId}: {channel_entity.title}")
          connected.send_message(
            TG_ADMIN_CHANNEL_ID, f"Пользователь @{participant.username} удалён из канала: **{channel_entity.title}**")
        except errors.rpcerrorlist.ChatAdminRequiredError as e:
          # ОШИБКА: У бота отсутствуют права администратора
          connected.send_message(
            TG_ADMIN_CHANNEL_ID, f"Отсутствуют права администратора в канале: **{channel_entity.title}**")
          print(
            f"Error: {e}: Insufficient admin privileges in the group: **{channel_entity.title}**.")
        except Exception as e:
          print(f"Error: {e}")

  connected.disconnect()

def run():
  # Создаём новый цикл событий
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  # Объявление клиента Telegram
  client = TelegramClient('./sessions/check_session', TG_API_ID, TG_API_HASH, loop=loop)

  # Ставим на рассписание выполнение функции проверки пользователей
  schedule.every().day.at(FIND_TIME, "Europe/Moscow").do(checkUsers, client)

  # Цикл запуска расписаний
  while True:
    print('Проверяем, есть ли отложенные задачи, которые нужно выполнить')
    schedule.run_pending()
    time_of_next_run = schedule.next_run()
    time_now = datetime.now()
    time_remaining = time_of_next_run - time_now
    print(f"Next run in {time_of_next_run}. {time_remaining.seconds} remaining seconds")
    time.sleep(60)

def main():
  # Telegram client initialization
  client = TelegramClient('./sessions/bot_session', TG_API_ID, TG_API_HASH)

  # Команда получения ID чата
  @client.on(events.NewMessage(pattern='/get_id'))
  async def getChannelId(event):
    try:
      # Получаем id чата, и обрабатываем так, чтобы id был с - в начале
      result_string = '-' + str(event.message.peer_id.chat_id)
      # Преобразуем в число
      result_number = int(result_string)

      # Отправляем сообщение с ID канала
      await event.respond(f"Channel ID: {result_number}")

    except Exception as e:
      # Эксепшен при возникновении любых ошибок
      # TODO: Вывести в консоль + отправить сообщение в админ чат
      print(f'Error: {e}')

  # Запускаем отдельный поток в котором будем производить проверки
  thread = Thread(target=run)
  thread.start()

  # Основной поток, который не будет завершаться и будет переподключаться при потере соединения
  connected = telegramClientReconnect(client)
  connected.run_until_disconnected()

if __name__ == "__main__":
  main()
