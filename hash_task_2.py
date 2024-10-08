import hashlib
from cryptography.fernet import Fernet
from tkinter import *
from tkinter.messagebox import showinfo, showerror
import uuid

pass_dict = {}
salt_dict = {}

key = Fernet.generate_key()
cipher = Fernet(key)


#   функция авторизации
def sign_up_func():
    if login_entry.get() in pass_dict.keys():
        showerror('Error', 'You\'ve already authorised')
    else:
        salt_dict.setdefault(login_entry.get(), encrypt(uuid.uuid4().hex))
        pass_dict.setdefault(login_entry.get(), hashlib.md5(bytes((pass_entry.get() + decrypt(salt_dict[login_entry.get()])).encode())))
        showinfo('Authorisation', 'Now you are authorised!')


#   функция входа
def sign_in_func():
    if login_entry.get() not in pass_dict.keys():
        showerror('Error', 'You\'ve not authorised')
    else:
        check_password()


#  функция проверки пароля
def check_password():
    pass_check = hashlib.md5(bytes((pass_entry.get() + decrypt(salt_dict[login_entry.get()])).encode()))
    if pass_check.digest() == pass_dict[login_entry.get()].digest():
        showinfo('Result', 'Password is correct, welcome!')
        login_entry.delete(0, END)
        pass_entry.delete(0, END)
        login_entry.focus()
    else:
        showerror('Result', 'Password is wrong, try again.')


#   функции шифровки и дешифровки соли
def encrypt(salt):
    return cipher.encrypt(salt.encode())


def decrypt(salt):
    return cipher.decrypt(salt).decode()


#   создаём окно для ввода пароля
root = Tk()
root.title('Authorization')
root.geometry('330x200')
root['bg'] = 'LightPink'
root.resizable(False, False)
Label(text='Login:', font='Sylfaen', background='PaleVioletRed').place(x=30, y=5)
Label(text='Password:', font='Sylfaen', background='PaleVioletRed').place(x=30, y=85)


#   поля ввода логина и пароля
login_entry = Entry(justify=LEFT, font='TimesNewRoman 11')
login_entry.place(height=40, width=150, x=30, y=40)
login_entry.focus()
pass_entry = Entry(justify=LEFT, font='TimesNewRoman 11')
pass_entry.place(height=40, width=150, x=30, y=120)


#   кнопки ввода пароля и проверки
sign_in_butt = Button(text='Sign in', font='Sylfaen', background='PaleVioletRed', command=sign_in_func)
sign_in_butt.place(height=30, width=90, x=210, y=60)
sign_un_butt = Button(text='Sign up', font='Sylfaen 12', background='PaleVioletRed', command=sign_up_func)
sign_un_butt.place(height=25, width=80, x=215, y=110)


root.mainloop()