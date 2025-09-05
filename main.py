import requests
import tkinter as tk
from tkinter import * 
from tkinter import messagebox

session = requests.Session()

def build_url(base_url, login_secpath_env, login_path):
    # если нет http/https → добавляем https://
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "https://" + base_url

    # убираем возможный / на конце
    base_url = base_url.rstrip("/")

    # собираем полный путь
    return f"{base_url}/{login_secpath_env}/{login_path}"

def login():
    login_login_env = login_login.get()
    login_pass_env = login_pass.get()
    login_url_env = login_url.get()
    login_secpath_env = login_secpath.get()
    login_data = {
        "username": login_login_env,
        "password": login_pass_env
    }
    login_path_modern = build_url(login_url_env, login_secpath_env, login_path)
    login_response = session.post(login_path_modern, data=login_data)
    print("Login:", login_response.json())

login_path = "login"

window = Tk()
window.title("API System for 3X-UI")
window.geometry("500x250")

lbl = Label(window, text="Привет")
lbl.grid(column=0, row=0)  

login_url = Entry(window,width=10)  
login_url.grid(column=1, row=0) 

login_login = Entry(window,width=10)  
login_login.grid(column=1, row=1) 

login_pass = Entry(window,width=10)  
login_pass.grid(column=1, row=2)

login_secpath = Entry(window,width=10)  
login_secpath.grid(column=1, row=3)

login_button = Button(window, text="Login", command=login)  
login_button.grid(column=2, row=0) 


window.mainloop()
#session = requests.Session()

#login_url = "https://riga.xui.qpda.ru/adnokinu/login"
#login_data = {
#    "username": "admin",
#    "password": "Artka565!"
#}
#login_response = session.post(login_url, data=login_data)
#print("Login:", login_response.json())

#inbounds_url = "https://riga.xui.qpda.ru/adnokinu/panel/api/inbounds/list"
#inbounds_response = session.get(inbounds_url)
