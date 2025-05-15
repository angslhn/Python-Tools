import tkinter as tk
from tkinter import messagebox
import os
import ctypes
import tempfile
import shutil

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
DOMAINS = [
    "127.0.0.1 update.postman.com",
    "127.0.0.1 dl.pstmn.io",
    "127.0.0.1 api.postman.com"
]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_postman_update():
    with open(HOSTS_PATH, 'a+') as hosts:
        hosts.seek(0)
        content = hosts.read()
        for domain in DOMAINS:
            if domain not in content:
                hosts.write(domain + '\n')
    messagebox.showinfo("Blokir Update", "Auto update Postman DIBLOKIR.")

def allow_postman_update():
    with open(HOSTS_PATH, 'r') as hosts:
        lines = hosts.readlines()

    with open(HOSTS_PATH, 'w') as hosts:
        for line in lines:
            if not any(domain.split()[1] in line for domain in DOMAINS):
                hosts.write(line)

    messagebox.showinfo("Izinkan Update", "Auto update Postman DIIJINKAN kembali.")

def main():
    if not is_admin():
        messagebox.showerror("Permission Denied", "Harus dijalankan sebagai Administrator.")
        return

    root = tk.Tk()
    root.title("Postman Update Toggle")
    root.geometry("300x120")
    root.resizable(False, False)

    btn_off = tk.Button(root, text="BLOKIR UPDATE (OFF)", command=block_postman_update, width=25)
    btn_off.pack(pady=10)

    btn_on = tk.Button(root, text="IZINKAN UPDATE (ON)", command=allow_postman_update, width=25)
    btn_on.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
