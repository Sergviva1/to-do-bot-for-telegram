import telebot
from telebot import types
import os
from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

def create_replykeyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text = "Добавить задачу")
    btn2 = types.KeyboardButton(text = "Посмотреть список задач")
    btn3 = types.KeyboardButton(text = "Отметить задачу выполненной")
    btn4 = types.KeyboardButton(text = "Удалить задачу")
    kb.add(btn1,btn2,btn3,btn4)
    return kb

tasks = {}

# Обработчик /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    if user_id not in tasks:
        tasks[user_id] = []
    bot.send_message(message.chat.id, "Привет, я <b>TO-DO бот</b>. Отправляй мне свои задачи и я помогу их орагнизовать :3", parse_mode="HTML", reply_markup=create_replykeyboard())

# Добавление задачи 
@bot.message_handler(func=lambda y: y.text == "Добавить задачу") 
def set_task(message):
    bot.send_message(message.chat.id, "Введите задачу:")
    bot.register_next_step_handler(message, addtask)

def addtask(message):
    user_id = message.chat.id
    if user_id not in tasks:
        tasks[user_id] = []
    tasks[user_id].append(message.text)
    bot.send_message(message.chat.id, "Ваша задача успешно добавлена!")
 
# Просмотр задач
@bot.message_handler(func=lambda y: y.text == "Посмотреть список задач")
def get_tasks(message):
    user_id = message.chat.id
    if user_id not in tasks:
        tasks[user_id] = []
    if len(tasks[user_id]) == 0:
        bot.send_message(message.chat.id, "У вас 0 задач")
        return 0
    
    send_task = "Текущие задачи: \n\n"
    for i, task in enumerate(tasks[user_id], start=1):
        send_task += f"{i}. {task}\n"
        
    bot.send_message(message.chat.id, send_task)
       
# Отметка задач
@bot.message_handler(func=lambda y: y.text == "Отметить задачу выполненной") 
def complete_task(message):
    user_id = message.chat.id
    get_tasks(message)
    if len(tasks[user_id]) > 0:
        bot.send_message(message.chat.id, "Выберите выполненную задачу:")
        bot.register_next_step_handler(message, choose_task)
 
def choose_task(message):
    user_id = message.chat.id
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Пожалуйста, введите номер задачи!")
        bot.register_next_step_handler(message, choose_task)
        return
    if int(message.text) < 1 or int(message.text) > len(tasks[user_id]):
        bot.send_message(message.chat.id, "Такой задачи не существует")
        bot.register_next_step_handler(message, choose_task)
        return
    for i, task in enumerate(tasks[user_id], start=1):
        if int(message.text) == i:
            task_index = i - 1
            if tasks[user_id][task_index][-1] != "☑":
                tasks[user_id][task_index] = tasks[user_id][task_index] + " ☑"
                bot.send_message(message.chat.id, f"Задача {i}. {task} выполнена ☑")
            else:
                bot.send_message(message.chat.id, "Задача уже выполнена")
                
# Удаление задач         
@bot.message_handler(func=lambda y: y.text == "Удалить задачу") 
def delete_task(message):
    get_tasks(message)
    bot.send_message(message.chat.id, "Выберите задачу для удаления:")
    bot.register_next_step_handler (message, dele)

def dele(message):
    user_id = message.chat.id
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Пожалуйста, введите номер задачи!")
        bot.register_next_step_handler(message, dele)
        return
    if int(message.text) < 1 or int(message.text) > len(tasks[user_id]):
        bot.send_message(message.chat.id, "Такой задачи не существует")
        bot.register_next_step_handler(message, choose_task)
        return
    for i, task in enumerate(tasks[user_id], start=1):
        if int(message.text) == i:
            task_index = i - 1
            tasks[user_id].pop(task_index)
            bot.send_message(message.chat.id, f"Задача {i}. {task} была удалена")

# Любое сообщение
@bot.message_handler(func=lambda x:True)
def reply_to_all_message(message):
    bot.send_message(message.chat.id, "Выберите действие кнопками", reply_markup=create_replykeyboard())
     
bot.polling() 


