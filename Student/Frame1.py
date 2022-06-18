from tkinter import Entry, Frame, Tk, Label, Button, Checkbutton, Toplevel, messagebox
import cv2
import os
import Frame2
import urllib
import sqlite3
import urllib.request
import urllib.error
import time
import MyMainException
from PIL import Image, ImageTk

MyID = MyMajor = None


class Frame1:
    def __init__(self, master):
        self.__master = master
        self.__frame1 = Frame(master)
        self.__GUIconfig()
        self.__frame1.pack(fill="both", expand=1)

    def __GUIconfig(self):
        img = ImageTk.PhotoImage(file="..\\resource\logo1.png")
        self.__master.title("Thuy Loi University")
        self.__master.geometry("1000x600")
        self.__master.resizable(False, False)
        self.__frame1.config(width=1000, height=600)
        label = Label(self.__frame1, image=img)
        label.image_names = img
        label.place(x=-2, y=0)
        etr1, etr2 = self.__setEntry()
        self.__master.bind("<Return>", lambda e: self.__SignIn(etr1, etr2))
        Button(
            self.__frame1,
            text="Đăng nhập",
            font=("Arial", 15, "bold"),
            fg="green",
            command=lambda: self.__SignIn(etr1, etr2),
        ).place(x=750, y=330)

    

        Button(
            self.__frame1,
            text="Quên mật khẩu",
            font=("Arial", 10, "bold"),
            fg="#009BFA",
            command=self.__forgetPW,
            borderwidth=0,
        ).place(x=600, y=290)

    def __setEntry(self):
        Label(self.__frame1, text="Tên đăng nhập:", font=("Arial", 15, "bold")).place(
            x=600, y=120
        )
        entry1 = Entry(self.__frame1, width=20,
                       font=("Arial", 20), justify="left")
        entry1.place(x=600, y=150)

        Label(
            self.__frame1,
            text="Mật Khẩu:",
            font=("Arial", 15, "bold"),
        ).place(x=600, y=220)
        entry2 = Entry(
            self.__frame1, width=20, font=("Arial", 20), show="*", justify="left"
        )
        entry2.place(x=600, y=250)
        return entry1, entry2

    def forget(self):
        self.__frame1.forget()

    def pack(self):
        self.__frame1.pack(fill="both", expand=1)

    def __SignIn(self, etr1, etr2):
        if type(etr1) == type("a"):
            id, pw = etr1, etr2
            MyMainException.checkID(id)
        else:
            id, pw = etr1.get(), etr2.get()
            MyMainException.checkID(id)
            MyMainException.checkPW(pw)

        global MyID, MyMajor
        MyID = id
        connect = sqlite3.connect("..\database\database.db")
        cursor = connect.execute(
            "SELECT * FROM people WHERE ID=" + str(id))
        isRecordExist = 0
        if pw != "PASS":
            for row in cursor:
                if str(id) == str(row[0]) and str(pw) == str(row[1]):
                    isRecordExist = 1
                    MyMajor = row[7]
        else:
            isRecordExist = 1
        if isRecordExist == 1:
            self.__master.unbind("<Return>")
            self.__frame1.forget()
            self.__frame2 = Frame2.Frame2(self.__master)
            self.__frame2.pack()
        else:
            messagebox.showwarning(
                "Error", "Tên đăng nhập hoặc mật khẩu không đúng"
            )
        connect.commit()
        connect.close()

    def __forgetPW(self):
        messagebox.showinfo(
            "Forgot Password",
            "Bạn hãy liên hệ với giáo viên để được cấp lại mật khẩu",
        )

  

    def __Reset(self):
        self.__frame1.destroy()


"""root = Tk()
mg = Frame1(root)
root.mainloop()"""
