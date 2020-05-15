import hashlib
import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.environ.get('MYSQL_PASSWORD'),
    database="log_in")

my_cursor = mydb.cursor()

def log_in():
    email = str(input('Email: '))
    passw = str(input('Password: '))
    read = str(input('Do you want to read or change your text?(r/c)'))
    md5passw = hashlib.md5(passw.encode())
    passwdb = md5passw.hexdigest()

    my_cursor.execute(f'SELECT info FROM login_data WHERE email = "{email}" AND pass = "{passwdb}";')
    p = my_cursor.fetchone()
    if read.lower() == 'r':
        for i in p:
            print(i)
    elif read.lower() == 'c':
        print('\nThis is the last thing that you typed:')
        for i in p:
            print(i)
        info = str(input('\nWhat do you want to type now?\n'))
        my_cursor.execute(f"UPDATE `log_in`.`login_data` SET `info` = '{info}' WHERE (`email` = '{email}');")
        mydb.commit()
        print('Your text has been changed.')
    quit()

def sing_up():
    user = str(input('Username: '))
    name = str(input('Name: '))
    last = str(input('Last: '))
    email = str(input('Email: '))
    passw = str(input('Password: '))

    info = f'Type something, {name}'

    print('loading... ')

    try:
        sqlformula = "INSERT INTO login_data (nom, cognom, email, pass, username, info) VALUES (%s, %s, %s, md5(%s), " \
                     "%s, %s) "
        dades = (name, last, email, passw, user, info)
        my_cursor.execute(sqlformula, dades)
        mydb.commit()
    except:
        print('Email or username already in use')

log_sing = input('Log in or sing up? (log/sing)')

if log_sing.lower() == 'log':
    log_in()
elif log_sing.lower() == 'sing':
    sing_up()