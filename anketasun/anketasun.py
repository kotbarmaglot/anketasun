from .config import API_KEY
from .db import get_table, update_table_questions, create_table, delete_table, update_table_users, update_table_answers
import telebot
import json
from telebot import types
import pathlib
from pathlib import Path
import os
import sys
from pprint import pprint
import datetime


bot = telebot.TeleBot(API_KEY)


# admin = [257930228, 1820161475]
admin = []
adminoksa = [1820161475]
adminroman = [257930228]


def next_step_anketing(message):
    question = get_table(table='questions')
    answers = get_table('answers', user = message.from_user.id)

    print('вопросы', question)
    print('ответы', answers)

    ans = {}

    amount_question = len(question)

    # print(answers)

    if not answers:
        i = 1
        ans['user_id'] = message.from_user.id
        ans['question_id'] = i
        ans['answer'] = message.text
        print('1111', ans)
        update_table_answers(ans)
        anketing(message, i)
    else:
        i = len(answers)+1
        if i < amount_question:
            ans['user_id'] = message.from_user.id
            ans['question_id'] = i
            ans['answer'] = message.text

            update_table_answers(ans)

            anketing(message, i)
        
        elif i == amount_question:
            ans['user_id'] = message.from_user.id
            ans['question_id'] = i
            ans['answer'] = message.text

            update_table_answers(ans)

            finish_anketing(message)


def anketing(message, i):
    question = get_table(table='questions')
    amount_question = len(question)

    text = str(question[i][2]) + f'/{amount_question}. ' + question[i][1]
    msg = bot.send_message(message.from_user.id, text=text)
    bot.register_next_step_handler(msg, next_step_anketing)

    
def finish_anketing(message):
    bot.send_message(message.from_user.id, text='Вы ответили на все вопросы. Спасибо за уделенное время.')


def start_anketa(message):
    user = {}

    user['id'] = message.from_user.id
    user['name'] = message.from_user.first_name if message.from_user.first_name else 'none'
    user['surname'] = message.from_user.last_name if message.from_user.last_name else 'none'
    user['nickname'] = message.from_user.username if message.from_user.username else 'none'

    update_table_users(user)

    question = get_table(table='questions')
    answers = get_table('answers', user = message.from_user.id)

    if len(question) == len(answers):
        finish_anketing(message)
    else:
        if not answers:
            i = 0
        else:
            i = len(answers)
        
        anketing(message, i=i)

    
def show_users(message):
    users = get_table('users')

    for elem in users:
        id = elem[0]
        name = elem[1]
        surname = elem[2]
        nickname = '@' + elem[3]

        item = f'item_{id}'

        markup_inline = types.InlineKeyboardMarkup()

        item = types.InlineKeyboardButton(text='Показать ответы', callback_data=f'show_answers_{id}')

        markup_inline.add(item)

        bot.send_message(message.from_user.id, text = f'id - {id} \n\nИмя - {name} \n\nФамилия - {surname} \n\nNickname - {nickname}', reply_markup=markup_inline)


def show_answers(message, user):
    answers = get_table('answers', user=user)

    for elem in answers:
        answer = elem[3]
        quest = elem[2]
        text = f'Вопрос номер {quest} \n\nОтвет - {answer}'
        bot.send_message(message.from_user.id, text=text)

    print(answers)


def show_questions(message):

    quest = get_table(table='questions')

    for elem in quest:
        text = str(elem[2]) + '. ' + elem[1]
        bot.send_message(message.from_user.id, text=text)
    
    menu(message)


def next_step_add_questions(message):
    user = message.from_user.id
    stroka = message.text
    index_number = int(stroka.partition('. ')[0])

    question = stroka.partition('. ')[2]

    print(index_number, question)
    # bot.send_message(user, 'Добавить еще один вопрос')

    update_table_questions(question=question, index_number=index_number)

    markup_inline = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton(text='Добавить вопрос', callback_data='add_questions')
    item2 = types.InlineKeyboardButton(text='Завершить добавление вопросов', callback_data='finish_add_questions')

    markup_inline.add(item)
    markup_inline.add(item2)

    bot.send_message(user, 'Вопрос успешно добавлен', reply_markup=markup_inline)


def add_questions(message):
    user = message.from_user.id
    msg = bot.send_message(user, 'Напиши вопрос, который нужно добавить: (1. Вопрос?):')
    bot.register_next_step_handler(msg, next_step_add_questions)


@bot.message_handler(commands=['start'])
def menu(message):

    user = message.from_user.id

    if user in adminoksa:
        admin_menu = types.ReplyKeyboardMarkup(True, True)
        admin_menu.add('Показать пользователей')
        admin_menu.add('Показать вопросы')
        admin_menu.add('Добавить вопрос')
        admin_menu.add('Создать таблицы', 'Удалить таблицы')

        bot.send_message(user, 'Стартовое меню для админа:', reply_markup=admin_menu)

    else:
        markup_inline=types.ReplyKeyboardRemove()
        print('зашел обычный поьзователь')
        markup_inline = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton(text='Начать анкетирование', callback_data='start_anketa')

        markup_inline.add(item)

        bot.send_message(user, 'Прошу вас ответить на несколько вопросов:', reply_markup=markup_inline)



@bot.message_handler(content_types=['text'])
def handle_text_admin(message):

    user = message.from_user.id

    if user in adminoksa:

        if message.text == 'Показать пользователей':
            show_users(message)

            # menu(message)

        if message.text == 'Показать вопросы':
            # show_questions(message)
            try:
                show_questions(message)
            except:
                bot.send_message(user, 'Таблицы не созданы')
                menu(message)
            

        if message.text == 'Добавить вопрос':
            add_questions(message)

        if message.text == 'Создать таблицы':
            create_table()
            menu(message)

        if message.text == 'Удалить таблицы':
            delete_table()
            menu(message)

        
@bot.callback_query_handler(func=lambda m: True)
def callback_choice(message):
    t = message.data

    users = get_table('users')

    list_users = []

    for elem in users:
        id = elem[0]
        list_users.append(f'show_answers_{id}')

    if t in list_users:
        id = t.partition('show_answers_')[2]
        print(id)
        user = int(id)
        # bot.send_message(user, 'Стартовое меню для админа:', reply_markup=admin_menu)
        show_answers(message, user)
        

    if t == 'start_anketa':
        start_anketa(message)

    if t == 'add_questions':
        add_questions(message)

    if t == 'finish_add_questions':
        menu(message)
            

bot.infinity_polling()


def main():
    pass


if __name__ == '__main__':
    main()