from tkinter import Tk, Frame, Label, Button, Entry, messagebox, ttk
import sqlite3, os, MyException, firebase

from pyrebase.pyrebase import Firebase


class MyFrame:
    def __init__(self, master):
        self.__master = master
        self.__mainframe = Frame(self.__master)
        self.__connect = sqlite3.connect(
            os.path.join(os.getcwd(), r"../database/database.db")
        )
        self.__lst = []
        self.__master.bind("<Return>", lambda e: self.__submit())
        Button(
            self.__mainframe,
            text="Thêm",
            fg="Green",
            font=("Arial", 20, "bold"),
            command=self.__submit,
        ).place(x=50, y=400)
        Button(
            self.__mainframe,
            text="Thoát",
            fg="Red",
            font=("Arial", 20, "bold"),
            command=self.forget,
        ).place(x=340, y=400)
        self.__FrConfig()

    def __FrConfig(self):
        frame = Frame(self.__mainframe)
        frame.pack(pady=180)

        Label(
            self.__mainframe,
            text="ID:",
            anchor="e",
            width=15,
            font=("Arial", 15, "bold"),
        ).place(x=95, y=10)
        etr1 = Entry(self.__mainframe, font=("Arial", 15), justify="center")
        etr1.place(x=150, y=40)

        Label(
            self.__mainframe,
            text="Mật Khẩu:",
            anchor="e",
            width=15,
            font=("Arial", 15, "bold"),
        ).place(x=-10, y=80)
        etr2 = Entry(self.__mainframe, font=("Arial", 15), justify="center")
        etr2.place(x=10, y=110)

        Label(
            self.__mainframe,
            text="Nhập Lại Mật Khẩu:",
            anchor="e",
            width=16,
            font=("Arial", 15, "bold"),
        ).place(x=285, y=80)
        etr3 = Entry(self.__mainframe, font=("Arial", 15), justify="center")
        etr3.place(x=285, y=110)

        Label(
            frame,
            text="Họ Tên:",
            anchor="e",
            width=8,
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, pady=10)
        etr4 = Entry(frame, font=("Arial", 10))
        etr4.grid(row=0, column=1, pady=10)

        Label(
            frame,
            text="Lớp:",
            anchor="e",
            width=15,
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=2, pady=10)
        etr5 = Entry(frame, font=("Arial", 10))
        etr5.grid(row=0, column=3, pady=10)

        Label(
            frame,
            text="Khoa:",
            anchor="e",
            width=8,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=0, pady=10)
        ots = ["Công Nghệ Thông Tin", "Kinh Tế", "Cơ Khí"]
        etr6 = ttk.Combobox(frame, font=("Arial", 8), values=ots)
        etr6.current(0)
        etr6.grid(row=1, column=1, pady=10)

        Label(
            frame,
            text="Giới Tính:",
            anchor="e",
            width=15,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=2, pady=10)
        options = ["", "Nam", "Nữ", "Khác"]
        etr7 = ttk.Combobox(frame, font=("Arial", 10), width=17, values=options)
        etr7.current(0)
        etr7.grid(row=1, column=3, pady=10)

        Label(
            frame,
            text="MSV:",
            anchor="e",
            width=8,
            font=("Arial", 10, "bold"),
        ).grid(row=2, column=0, pady=10)
        etr8 = Entry(frame, font=("Arial", 10))
        etr8.grid(row=2, column=1, pady=10)

        Label(
            frame,
            text="SĐT:",
            anchor="e",
            width=15,
            font=("Arial", 10, "bold"),
        ).grid(row=2, column=2, pady=10)
        etr9 = Entry(frame, font=("Arial", 10))
        etr9.grid(row=2, column=3, pady=10)

        Label(
            frame,
            text="Dân Tộc:",
            anchor="e",
            width=8,
            font=("Arial", 10, "bold"),
        ).grid(row=3, column=0, pady=10)
        etr10 = Entry(frame, font=("Arial", 10))
        etr10.grid(row=3, column=1, pady=10)

        Label(
            frame,
            text="Địa Chỉ:",
            anchor="e",
            width=15,
            font=("Arial", 10, "bold"),
        ).grid(row=3, column=2, pady=10)
        etr11 = Entry(frame, font=("Arial", 10))
        etr11.grid(row=3, column=3, pady=10)
        self.__lst = [
            etr1,
            etr2,
            etr3,
            etr4,
            etr5,
            etr6,
            etr7,
            etr8,
            etr9,
            etr10,
            etr11,
        ]

    def __submit(self):
        try:
            lstInfo = [" ".join(i.get().split()) for i in self.__lst]
            MyException.checkInfo(lstInfo)
            cursor = self.__connect.execute(
                "SELECT * FROM people WHERE ID=" + str(lstInfo[0])
            )
            isRecordExists = 0
            for row in cursor:
                isRecordExists = 1
            if isRecordExists == 0 and lstInfo[1] == lstInfo[2]:
                self.__connect.execute(
                    "INSERT INTO people(ID,PW,NAME,MSV,CLASS,GENDER,SDT,MAJOR,FOLK,ADDRESS) VALUES("
                    + str(lstInfo[0])
                    + ","
                    + str(lstInfo[1])
                    + ",'"
                    + str(lstInfo[3])
                    + "',"
                    + str(lstInfo[7])
                    + ",'"
                    + str(lstInfo[4])
                    + "','"
                    + str(lstInfo[6])
                    + "','"
                    + str(lstInfo[8])
                    + "','"
                    + str(lstInfo[5])
                    + "','"
                    + str(lstInfo[9])
                    + "','"
                    + str(lstInfo[10])
                    + "')"
                )
                firebase.uploadDatabase()
                messagebox.showinfo("OK", "Thêm thành công")
            elif isRecordExists == 1:
                messagebox.showwarning("Warning", "ID đã có người sử dụng")
            self.__connect.commit()
            self.__connect.close()
            self.__master.unbind("<Return>")
            #self.__mainframe.forget()
        except (
            MyException.IDException,
            MyException.PWException,
            MyException.MSVException,
            MyException.SDTException,
            MyException.NameException,
            MyException.ClassException,
            MyException.FolkException,
            MyException.AddressException,
            MyException.MajorException,
            MyException.ReEnterPWException,
            MyException.GenderException,
        ) as e:
            e.warning()

    def forget(self):
        self.__master.unbind("<Return>")
        self.__mainframe.forget()

    def pack(self):
        self.__mainframe.pack()


"""root = Tk()
frame = MyFrame(root)
frame.pack()
root.mainloop()"""
