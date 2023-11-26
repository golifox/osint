# import requests
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import END
import httpx


def osint():
    file = open("list.txt")
    nick = vvod.get()
    label = tk.Label(
        win, text="Запущен поиск по нику '" + nick + "' ,пожалуйста, ожидайте"
    )
    label.grid(row=1, column=0, columnspan=5, stick="we")
    console.configure(state="normal")
    console.delete("1.0", "end")
    console.configure(state="disabled")

    for line in file:
        name = line.split(" ")[0]
        site = line.split(" ")[1]

        site = site.rstrip("\n")
        url = site + nick

        try:
            r = httpx.get(url)

            if r.status_code == 200:
                console.configure(state="normal")  # enable insert
                y = ("найдено " + name + ": " + url) + "\n"
                console.insert(END, y)
                # console.yview(END)  # autoscroll
                console.configure(state="disabled")  # disable editing
            else:
                console.configure(state="normal")  # enable insert
                e = (name + " не найдено") + "\n"
                console.insert(END, e)
                # console.yview(END)  # autoscroll
                console.configure(state="disabled")  # disable editing
        except:
            console.configure(state="normal")  # enable insert
            s = "ошибка запроса для " + name + "\n"
            console.insert(END, s)
            # console.yview(END)  # autoscroll
            console.configure(state="disabled")  # disable editing
    file.close()


win = tk.Tk()
photo = tk.PhotoImage(file="icon.png")
win.iconphoto(True, photo)
win.title("Nickname Finder")
win.geometry("660x550+500+300")
# win.maxsize(1000, 900)
# win.minsize(500, 600)
win.resizable(False, False)
win.grid_rowconfigure(2, minsize=500)

btn = tk.Button(win, text="Запуск поиска", command=osint)
btn.grid(row=0, column=2)
tx = tk.Label(win, text="Введите никнейм")
tx.grid(row=0, column=0)

vvod = tk.Entry(win)
vvod.grid(row=0, column=1)

console = tkst.ScrolledText(win, state="disabled")
console.grid(row=2, column=0, columnspan=3, stick="sn")

win.mainloop()
