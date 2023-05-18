import sqlite3
import datetime
import json


def create_table(table='all'):
    if table == 'all':
        create_table_questions()
        create_table_users()
        create_table_answers()
    elif table == 'questions':
        create_table_questions()
    elif table == 'users':
        create_table_users()
    elif table == 'answers':
        create_table_answers()


def delete_table(table='all'):

    con = sqlite3.connect("anketasun.db")
    con.execute('PRAGMA foreign_keys = 0')
    cur = con.cursor()

    if table == 'all':
        cur.execute('DROP TABLE IF EXISTS `questions`')
        cur.execute('DROP TABLE IF EXISTS `users`')
        cur.execute('DROP TABLE IF EXISTS `answers`')
    
    else:
        cur.execute(f'DROP TABLE IF EXISTS {table}')

    con.execute('PRAGMA foreign_keys = 1')

    con.commit()
    con.close()
    

def create_table_questions():
    con = sqlite3.connect("anketasun.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS `questions` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            index_number INTEGER NOT NULL
        )""")
    con.commit()
    con.close()


def create_table_users():
    con = sqlite3.connect("anketasun.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            nickname TEXT NOT NULL
        )""")
    con.commit()
    con.close()


def create_table_answers():
    con = sqlite3.connect("anketasun.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS `answers` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )""")
    con.commit()
    con.close()


def update_table_users(user):
    con = sqlite3.connect("anketasun.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    cur.execute("""INSERT OR REPLACE INTO `users` (id, name, surname, nickname) VALUES(:id, :name, :surname, :nickname)""", user)

    con.commit()
    con.close()


def update_table_answers(ans):
    con = sqlite3.connect("anketasun.db")
    con.execute('PRAGMA foreign_keys = 1')
    cur = con.cursor()

    print('answer', ans)

    cur.execute("""INSERT OR REPLACE INTO `answers` (user_id, question_id, answer) VALUES(:user_id, :question_id, :answer)""", ans)

    con.commit()
    con.close()


def update_table_questions(question, index_number):
    con = sqlite3.connect("anketasun.db")
    cur = con.cursor()

    print('dddd', question, index_number)

    cur.execute(f"INSERT INTO `questions`(question, index_number) values('{question}', {index_number})")

    con.commit()
    con.close()



def get_table(table, user=0):
    print(table)
    con = sqlite3.connect("anketasun.db")
    cur = con.cursor()

    if table == 'questions':
        res = cur.execute(f"SELECT * FROM {table} ORDER BY index_number").fetchall()
    
    elif table == 'users':
        res = cur.execute(f"SELECT * FROM {table}").fetchall()

    elif table == 'answers':
        res = cur.execute(f"SELECT * FROM {table} WHERE user_id={user}").fetchall()
    

    return res


def main():
    pass


if __name__ == '__main__':
    main()