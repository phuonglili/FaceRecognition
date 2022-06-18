import time
from tkinter import Tk, Frame, Label, Button, Canvas, Toplevel, messagebox, ttk
import sqlite3, firebase, threading


class MyFrame1:
    def __init__(self, master):
        self.__master = Toplevel(master)
        self.__master.geometry("620x520")
        self.__master.resizable(False, False)
        self.__SvTime = tuple("0" for i in range(8))
        self.__SVOn = tuple()
        self.__SVOff = tuple()
        self.__status = "All"
        self.__frame = Frame(self.__master, width=620, height=220)
        self.__connect = sqlite3.connect("..\database\database.db")
        cursor = self.__connect.execute("SELECT * FROM people")
        self.__lstsv = [i for i in cursor]
        self.__frameConfig()
        self.__connect.commit()
        self.__connect.close()

    def __frameConfig(self):
        self.__frame.pack(fill="both", expand=1)

        self.__sta = Button(
            self.__frame,
            text="Start Lesson",
            font=("Arial", 20, "bold"),
            fg="green",
            command=self.__start,
        )
        self.__sta.place(x=200, y=0)
        self.__sto = Button(
            self.__frame,
            text="Stop Lesson",
            font=("Arial", 20, "bold"),
            fg="red",
            command=self.__stop,
        )
        Button(
            self.__frame,
            text="Back",
            font=("Arial", 20, "bold"),
            fg="orange",
            command=self.__master.destroy,
        ).place(x=250, y=465)

        thr1 = threading.Thread(name=("Thr1"), target=self.__getSvTime)
        thr1.start()

        options = ("All", "Online", "Offline")
        self.__cbb = ttk.Combobox(
            self.__frame, values=options, font=("Arial", 20), width=6, foreground="blue"
        )
        self.__cbb.current(0)
        self.__cbb.place(x=460, y=0)
        self.__getStatus()

        self.__scr = ttk.Scrollbar(self.__frame, orient="vertical")
        self.__scr.pack(side="right", fill="y")

    def __start(self):
        firebase.setClassStatus(1)
        self.__sta.place_forget()
        self.__sto = Button(
            self.__frame,
            text="Stop Lesson",
            font=("Arial", 20, "bold"),
            fg="red",
            command=self.__stop,
        )
        self.__sto.place(x=200, y=0)

        self.__canvasConfig()

    def __stop(self):
        firebase.setClassStatus(0)
        threading.Thread(target=firebase.config).start()
        self.__myCanvas.forget()
        self.__sto.place_forget()
        self.__sta = Button(
            self.__frame,
            text="Start Lesson",
            font=("Arial", 20, "bold"),
            fg="green",
            command=self.__start,
        )
        self.__sta.place(x=200, y=0)

    def __canvasConfig(self):
        self.__myCanvas = Canvas(self.__frame, width=600, height=420)
        self.__scr.config(command=self.__myCanvas.yview)
        self.__myCanvas.config(yscrollcommand=self.__scr.set)
        self.__myCanvas.bind(
            "<Configure>",
            lambda a: self.__myCanvas.config(scrollregion=self.__myCanvas.bbox("all")),
        )
        self.__myCanvas.pack(side="left", pady=70)
        self.__frame1 = Frame(self.__myCanvas)
        self.__myCanvas.create_window((0, 0), window=self.__frame1, anchor="nw")
        self.__frame1Config()

    def __frame1Config(self):
        Label(self.__frame1, text="Danh sách sinh viên", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=4)
        self.__table()
        cbb = self.__cbb.get()
        lst = self.__lstsv
        if self.__cbb.get() == "Online":
            lst = tuple(
                self.__lstsv[i]
                for i in range(len(self.__lstsv))
                if int(self.__SvTime[i]) > 0
            )
        elif self.__cbb.get() == "Offline":
            lst = tuple(
                self.__lstsv[i]
                for i in range(len(self.__lstsv))
                if int(self.__SvTime[i]) == 0
            )
        q=0
        while(q<len(lst)):
            Label(self.__frame1, text=str(q + 1), font=("Arial", 15)).grid(row=q + 2, column=0)
            Label(self.__frame1, text=lst[q][3], font=("Arial", 15)).grid(row=q + 2, column=1)
            Label(self.__frame1, text=lst[q][2], font=("Arial", 15)).grid(row=q + 2, column=2)
            Label(self.__frame1, text=str(0), font=("Arial", 15),).grid(row=q + 2, column=3)
            q = q+1
        self.__frame1.after(1000, lambda: self.__updateTime(cbb, len(lst)))

    def __updateTime(self, cbb, i):
        self.__thr1 = threading.Thread(name=("Thr1"), target=self.__getSvTime)
        self.__thr1.start()

        tp = self.__SvTime
        if self.__cbb.get() == "Online":
            tp = self.__SVOn
        elif self.__cbb.get() == "Offline":
            tp = self.__SVOff
        for q in range(len(tp)):
            Label(
                self.__frame1,
                text="     ",
                font=("Arial", 15),
            ).grid(row=q + 2, column=3)
            Label(
                self.__frame1,
                text=str(tp[q]),
                font=("Arial", 15),
            ).grid(row=q + 2, column=3)
        a = (
            len(self.__SVOn)
            if self.__cbb.get() == "Online"
            else len(self.__SVOff)
            if self.__cbb.get() == "Offline"
            else len(self.__SvTime)
        )
        if cbb != self.__cbb.get() or i != a:
            # self.__frame1.pack_forget()
            self.__myCanvas.forget()
            # self.__frame1 = Frame(self.__frame, width=620, height=420)
            # self.__frame1.place(x=0, y=60)
            self.__canvasConfig()
            # self.__frame1Config()
            self.__myCanvas.update_idletasks()
        else:
            self.__frame1.after(3000, lambda: self.__updateTime(cbb, i))

    def __getSvTime(self):
        try:
            self.__SvTime = tuple(
                firebase.getTime(self.__lstsv[i][0]) for i in range(len(self.__lstsv))
            )
        except:
            firebase.config()
            self.__SvTime = tuple(
                firebase.getTime(self.__lstsv[i][0]) for i in range(len(self.__lstsv))
            )
        self.__SVOn = tuple(i for i in self.__SvTime if int(i) > 0)
        self.__SVOff = tuple(i for i in self.__SvTime if int(i) == 0)

    def __table(self):
        temp = len(self.__lstsv)
        if sum(set(map(int, self.__SvTime))) == 0 and self.__status != "All":
            time.sleep(2)
        if self.__status == "Online":
            temp = len([i for i in self.__SvTime if int(i) > 0])
        elif self.__status == "Offline":
            temp = len([i for i in self.__SvTime if int(i) == 0])

        for q in range(temp + 1):
            Label(
                self.__frame1,
                width=10,
                height=2,
                relief="solid",
                borderwidth=1,
            ).grid(row=q + 1, column=0)
            Label(
                self.__frame1,
                width=25,
                height=2,
                relief="solid",
                borderwidth=1,
            ).grid(row=q + 1, column=1)
            Label(
                self.__frame1,
                width=35,
                height=2,
                relief="solid",
                borderwidth=1,
            ).grid(row=q + 1, column=2)
            Label(
                self.__frame1,
                width=14,
                height=2,
                relief="solid",
                borderwidth=1,
            ).grid(row=q + 1, column=3)
        Label(self.__frame1, text="STT", font=("Arial", 15)).grid(row=1, column=0)
        Label(self.__frame1, text="Mã sinh viên", font=("Arial", 15)).grid(
            row=1, column=1
        )
        Label(self.__frame1, text="Họ tên", font=("Arial", 15)).grid(row=1, column=2)
        Label(self.__frame1, text="Thời gian", font=("Arial", 15)).grid(row=1, column=3)

    def __getStatus(self):
        self.__status = self.__cbb.get()
        self.__cbb.after(10, self.__getStatus)

    def forget(self):
        self.__frame.forget()

    def pack(self):
        self.__frame.pack()


"""root = Tk()
mf = MyFrame1(root)
root.mainloop()"""
