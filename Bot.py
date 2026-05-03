import telebot
from telebot import types
import os
from dotenv import load_dotenv
load_dotenv()
from db import create_table, add_task, get_tasks, delete_task, mark_task_completed
bot = telebot.TeleBot(os.getenv("TOKEN"))

def create_replykeyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text = "Добавить задачу")
    btn2 = types.KeyboardButton(text = "Посмотреть список задач")
    btn3 = types.KeyboardButton(text = "Отметить задачу выполненной")
    btn4 = types.KeyboardButton(text = "Удалить задачу")
    kb.add(btn1,btn2,btn3,btn4)
    return kb


# Обработчик /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    create_table()
    bot.send_message(message.chat.id, "Привет, я <b>TO-DO бот</b>. Отправляй мне свои задачи и я помогу их орагнизовать :3", parse_mode="HTML", reply_markup=create_replykeyboard())

# Добавление задачи 
@bot.message_handler(func=lambda y: y.text == "Добавить задачу") 
def set_task(message):
    bot.send_message(message.chat.id, "Введите задачу:")
    bot.register_next_step_handler(message, addtask)

def addtask(message):
    user_id = message.chat.id
    task = message.text
    add_task(user_id, task)
    bot.send_message(message.chat.id, "Ваша задача успешно добавлена!")
 
# Просмотр задач
@bot.message_handler(func=lambda y: y.text == "Посмотреть список задач")
def view_tasks(message):
    user_id = message.chat.id
    tasks = get_tasks(user_id)
    if len(tasks) == 0:
        bot.send_message(message.chat.id, "У вас 0 задач")
        return 0
    
    send_task = "Текущие задачи: \n\n"
    for i, task in enumerate(tasks, start=1):
        send_task += f"{i}. {task[1]}\n"
        
    bot.send_message(message.chat.id, send_task)
       
# Отметка задач
@bot.message_handler(func=lambda y: y.text == "Отметить задачу выполненной") 
def complete_task(message):
    user_id = message.chat.id
    user_tasks = get_tasks(user_id)
    if len(user_tasks) > 0:
        bot.send_message(message.chat.id, "Выберите выполненную задачу:")
        bot.register_next_step_handler(message, choose_task)
    else:
        bot.send_message(message.chat.id, "У вас 0 задач")
 
def choose_task(message):
    user_id = message.chat.id
    user_tasks = get_tasks(user_id)
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Пожалуйста, введите номер задачи!")
        bot.register_next_step_handler(message, choose_task)
        return
    task_index = int(message.text)
    if task_index < 1 or task_index > len(user_tasks):
        bot.send_message(message.chat.id, "Такой задачи не существует")
        bot.register_next_step_handler(message, choose_task)
        return
    task_id = user_tasks[task_index - 1][0]
    mark_task_completed(task_id)
    bot.send_message(message.chat.id, "Задача отмечена как выполненная!")
                
# Удаление задач         
@bot.message_handler(func=lambda y: y.text == "Удалить задачу") 
def delete_task_handler(message):
    user_id = message.chat.id
    user_tasks = get_tasks(user_id)
    if len(user_tasks) == 0:
        bot.send_message(message.chat.id, "У вас 0 задач")
        return
    bot.send_message(message.chat.id, "Выберите задачу для удаления:")
    bot.register_next_step_handler (message, dele)

def dele(message):
    user_id = message.chat.id
    user_tasks = get_tasks(user_id)
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Пожалуйста, введите номер задачи!")
        bot.register_next_step_handler(message, dele)
        return
    task_index = int(message.text)
    if task_index < 1 or task_index > len(user_tasks):
        bot.send_message(message.chat.id, "Такой задачи не существует")
        bot.register_next_step_handler(message, dele)
        return
    task_id = user_tasks[task_index - 1][0]
    delete_task(task_id)
    bot.send_message(message.chat.id, "Задача удалена!")

# Любое сообщение
@bot.message_handler(func=lambda x:True)
def reply_to_all_message(message):
    bot.send_message(message.chat.id, "Выберите действие кнопками", reply_markup=create_replykeyboard())


if __name__ == "__main__":
    bot.polling() 





