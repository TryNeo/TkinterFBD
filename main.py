# !/usr/bin/env python
# -*- coding: utf-8 -*-

from fbdown import *
from requests import *
from tkinter import ttk, messagebox

import tkinter as tk
import requests
import time

class MainWindow:
    def __init__(self, root):
        root.title('')
        root.geometry("450x320")
        root.resizable(0, 0)

        root.update_idletasks()
        width = root.winfo_width()
        frm_width = root.winfo_rootx() - root.winfo_x()
        win_width = width + 2 * frm_width
        height = root.winfo_height()
        titlebar_height = root.winfo_rooty() - root.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = root.winfo_screenwidth() // 2 - win_width // 2
        y = root.winfo_screenheight() // 2 - win_height // 2
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        root.deiconify()

        self.root = root

        self.principal(root)

    def principal(self,root):
        self.url = tk.StringVar()
        self.name_format = tk.StringVar()

        self.progressbar = ttk.Progressbar(root)
        self.progressbar.place(x=100, y=190, width=330)

        label_title = tk.Label(root, text="FB TK-VIDEOS", font=("Arial", 15)).place(x=150, y=20)

        label_url = tk.Label(root, text="url:", font=("Arial", 12)).place(x=35, y=70)
        entry_url = tk.Entry(root, width=40, textvariable=self.url).place(x=100, y=70)

        label_name_format = tk.Label(root, text="name:", font=("Arial", 12)).place(x=35, y=120)
        entry_name_format = tk.Entry(root, width=40, textvariable=self.name_format).place(x=100, y=120)

        button_download = tk.Button(root, text="Descargar", font=("Arial", 12), command=self.dowloand_fb).place(x=170, y=240)
    def dowloand_fb(self):
        try:
            url = self.url.get()
            path_name = self.name_format.get()
            if url == "":
                messagebox.showerror(title="Error Data", message="Url requerido")
            else:
                if path_name == "":
                    path_name+="default_name.mp4"
                else:
                    path_name+=".mp4"
                path = path_name.replace(" ","_")
                link = getdownlink(url)
                self.download(link, path)
        except requests.exceptions.RequestException as a:
            messagebox.showerror(title="Error Dowloand", message="Url desconocida - inserte uno existente")
        except requests.exceptions.ConnectionError as b:
            messagebox.showerror(title="Error Dowloand", message=b)
        except requests.exceptions.Timeout as c:
            messagebox.showerror(title="Error Dowloand", message=c)
        except requests.exceptions.HTTPError as d:
            messagebox.showerror(title="Error Dowloand", message=d)

    def download(self,url=None, path=None,root=None):
        """
        credits to fbdown - overwriting its dowloand function 
        repo git : https://github.com/tbhaxor/fbdown 
        """
        chunk = 1024
        r = get(url, stream=True)
        total = int(r.headers.get("content-length"))
        self.progressbar.configure(maximum=int(round(total/chunk,2)))
        with open(path, "wb") as file:
            for i in range(int(round(total/chunk,2)+1)):
                self.progressbar['value'] = i
                self.root.update_idletasks()
            
            for data in tqdm(iterable=r.iter_content(chunk_size=chunk)):
                file.write(data)
            file.close()
        messagebox.showinfo(title="Completed", message=f'Descargada completada.\nnombre:{path}\npeso:{self.convertbytes(total)}')

    def convertbytes(self,B):
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)
        GB = float(KB ** 3)
        TB = float(KB ** 4)
        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B/KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B/MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B/GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B/TB)

if __name__ == '__main__':
    main = tk.Tk()
    window = MainWindow(main)
    main.mainloop()
