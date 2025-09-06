import requests
import tkinter as tk
from tkinter import * 
from tkinter import messagebox

session = requests.Session()
login_url_env = ""
login_secpath_env = ""
login_path = "login"

def build_api_url(base_url, secpath, subpath=""):
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "https://" + base_url
    base_url = base_url.rstrip("/")
    url = f"{base_url}/{secpath}"
    if subpath:
        url += f"/{subpath.lstrip('/')}"
    return url

def build_url(base_url, login_secpath_env, login_path, subpath=""):
    if not base_url.startswith("http://") and not base_url.startswith("https://"):
        base_url = "https://" + base_url
    base_url = base_url.rstrip("/")
    url = f"{base_url}/{login_secpath_env}/{login_path}"
    if subpath:
        url += f"/{subpath.lstrip('/')}"
    return url

def login_toplevel():
    global login_url_env, login_secpath_env
    def login():
        global login_url_env, login_secpath_env
        try:
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
            data = login_response.json()
            if data.get("success"):
                messagebox.showinfo("Успех", "Вы успешно вошли в систему!")
                login_window.destroy()  # закрыть только если успешно
            else:
                messagebox.showerror("Ошибка входа", data.get("msg", "Не удалось войти"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить вход:\n{e}")

    login_window = tk.Toplevel(window)  # создаём новое окно
    login_window.title("Новое окно")
    login_window.geometry("300x200")

    lbl = Label(login_window, text="Привет")
    lbl.grid(column=0, row=0)  

    login_url = Entry(login_window,width=10)  
    login_url.grid(column=1, row=0) 

    login_login = Entry(login_window,width=10)  
    login_login.grid(column=1, row=1) 

    login_pass = Entry(login_window,width=10)  
    login_pass.grid(column=1, row=2)

    login_secpath = Entry(login_window,width=10)  
    login_secpath.grid(column=1, row=3)

    login_button = Button(login_window, text="Login", command=login)  
    login_button.grid(column=2, row=0)

def get_inbounds():
    try:
        inbounds_url = build_api_url(login_url_env, login_secpath_env, "panel/api/inbounds/list")
        response = session.get(inbounds_url)
        data = response.json()

        if not data.get("success"):
            messagebox.showerror("Ошибка", "Не удалось получить список клиентов")
            return

        # собираем клиентов по email
        clients_by_email = {}
        for inbound in data.get("obj", []):
            for client in inbound.get("clientStats", []):
                email = client["email"]
                if email not in clients_by_email:
                    clients_by_email[email] = []
                clients_by_email[email].append({
                    "inboundId": inbound["id"],
                    "port": inbound["port"],
                    "protocol": inbound["protocol"],
                    **client
                })

        # создаём окно
        inbounds_window = tk.Toplevel(window)
        inbounds_window.title("Inbounds")
        inbounds_window.geometry("600x400")

        lb = tk.Listbox(inbounds_window, width=40, height=15)
        lb.pack(padx=10, pady=10)

        txt = tk.Text(inbounds_window, wrap=tk.WORD, width=60, height=10)
        txt.pack(padx=10, pady=10)

        for email in clients_by_email.keys():
            lb.insert(tk.END, email)

        def on_select(event):
            selection = lb.curselection()
            if selection:
                email = lb.get(selection[0])
                txt.delete("1.0", tk.END)
                for client in clients_by_email[email]:
                    txt.insert(tk.END, f"Email: {client['email']}\n")
                    txt.insert(tk.END, f"Inbound ID: {client['inboundId']}\n")
                    txt.insert(tk.END, f"Port: {client['port']} | Protocol: {client['protocol']}\n")
                    txt.insert(tk.END, f"Up: {client['up']} | Down: {client['down']} | AllTime: {client['allTime']}\n")
                    txt.insert(tk.END, "-"*40 + "\n")

        lb.bind("<<ListboxSelect>>", on_select)

    except Exception as e:
        print("Не удалось получить inbounds:", e)

# главное окно
window = Tk()
window.title("API System for 3X-UI")
window.geometry("500x250")

login_button_toplevel = Button(window, text="Login", command=login_toplevel)  
login_button_toplevel.grid(column=1, row=0) 

inbounds_button = Button(window, text="Get Inbounds", command=get_inbounds)  
inbounds_button.grid(column=1, row=1) 

window.mainloop()
