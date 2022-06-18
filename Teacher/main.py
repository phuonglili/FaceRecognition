import threading, cv2, os, sqlite3, shutil, firebase, ConnectionCheck, time, Addstudent, ViewMyClass
from tkinter import Entry, Frame, Tk, Button, Label, Toplevel, ttk, messagebox
from PIL import Image, ImageTk
import numpy as np


class MyGui:
    def __init__(self, master):
        self.__master = master
        self.__face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.__id = 0
        self.__temp = 0
        self.__Config()

    def __Config(self):
        self.__master.geometry("620x520")
        self.__master.title("ThuyLoi University  ")
        self.__master.resizable(False, False)

        self.__frame = Frame(self.__master, width=620, height=520)
        self.__frameConfig()
        self.__frame1 = Frame(self.__master, width=620, height=520)

    def __frameConfig(self):
        self.__frame.pack()
        Label(self.__frame, text="ID GV:", font=("Arial", 20, "bold")).place(
            x=165, y=150
        )
        etr1 = Entry(self.__frame, font=("Arial", 20), width=10, justify="left")
        etr1.place(x=275, y=150)

        Label(self.__frame, text="PW GV:", font=("Arial", 20, "bold")).place(
            x=165, y=230
        )
        etr2 = Entry(self.__frame, font=("Arial", 20), width=10, show="*",justify="left")
        etr2.place(x=275, y=230)

        self.__master.bind("<Return>", lambda e: self.__signIn(etr1, etr2))
        Button(
            self.__frame,
            text="Đăng nhập",
            font=("Arial", 20, "bold"),
            fg="green",
            command=lambda: self.__signIn(etr1, etr2),
        ).place(x=310, y=300)
        Button(
            self.__frame,
            text="Thoát",
            font=("Arial", 20, "bold"),
            width=6,
            fg="red",
            command=self.__master.destroy,
        ).place(x=170, y=300)

    def __signIn(self, etr1, etr2):
        connection = False
        try:
            if not ConnectionCheck.internet_on():
                raise Exception
            else:
                connection = True
        except Exception:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")
        if connection == True:
            id, pw = etr1.get(), etr2.get()

            if id == "" or pw == "":
                messagebox.showwarning(
                    "Can't Sign In", "Tài khoản hoặc mật khẩu không được để trống"
                )
            else:
                connect = sqlite3.connect("..\database\database.db")
                query = "SELECT * FROM teacher WHERE ID=" + str(id)
                cursor = connect.execute(query)

                isRecordExist = 0
                for row in cursor:
                    if int(id) == int(row[0]) and int(pw) == int(row[1]):
                        isRecordExist = 1

                if isRecordExist == 1:
                    self.__master.unbind("<Return>")
                    self.__frame.forget()
                    self.__frame1Config()
                else:
                    messagebox.showwarning("Can't Sign In", "Sai ID hoặc PW")
        else:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")

    def __frame1Config(self):
        self.__frame1.pack()
        frame = Frame(self.__frame1)
        Label(frame, text="Add face", font=("Arial", 20, "bold")).grid(
            row=0, column=0, columnspan=2
        )
        Label(frame, text="ID SV:", font=("Arial", 20, "bold")).grid(row=1, column=0)
        etr = Entry(frame, font=("Arial", 20), justify="right")
        etr.grid(row=1, column=1)
        frame.place(x=100, y=120)
        self.__master.bind("<Return>", lambda e: self.__getInfo(etr))
        Button(
            self.__frame1,
            text="Xóa nhận dạng",
            font=("Arial", 10, "bold"),
            fg="#009BFA",
            borderwidth=0,
            command=lambda: self.__deleteRecognizer(etr),
        ).place(x=390, y=195)
        Button(
            self.__frame1,
            text="Đăng kí ",
            fg="green",
            font=("Arial", 20, "bold"),
            command=lambda: self.__getInfo(etr),
        ).place(x=330, y=230)

        Button(
            self.__frame1,
            text="Đăng xuất",
            fg="red",
            font=("Arial", 20, "bold"),
            command=self.__Logout,
        ).place(x=145, y=230)

        Button(
            self.__frame1,
            text="Thêm sinh viên",
            fg="Orange",
            font=("Arial", 20, "bold"),
            command=self.__addStudent,
        ).place(x=145, y=290)

        Button(
            self.__frame1,
            text="My class",
            fg="Purple",
            font=("Arial", 20, "bold"),
            command=self.__MyClass,
        ).place(x=230, y=360)

    def __Logout(self):
        self.__frame1.forget()
        self.__frameConfig()

    def __getInfo(self, etr):
        connection = False
        try:
            if not ConnectionCheck.internet_on():
                raise Exception
            else:
                connection = True
        except Exception:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")
        if connection == True:
            self.__id = etr.get()

            if self.__id == "":
                messagebox.showwarning("Can't Sign In", "Tài khoản không được để trống")
            else:
                connect = sqlite3.connect("..\database\database.db")
                query = "SELECT * FROM people WHERE ID=" + str(self.__id)
                cursor = connect.execute(query)

                isRecordExist = 0
                for row in cursor:
                    if int(self.__id) == int(row[0]):
                        isRecordExist = 1

                if isRecordExist == 1:
                    path_yml = "..\\recognizer\\trainingData.yml"
                    with open(path_yml, "r+") as f:
                        s = ""
                        l = []
                        for i in f:
                            if "      - !!opencv-matrix" in i:
                                l.append(s)
                                s = i
                            elif "   labels: !!opencv-matrix" in i:
                                l.append(s)
                                s = i
                            else:
                                s += i
                        l.append(s)
                        try:
                            idpos = [
                                i.strip()
                                for i in l[len(l) - 1]
                                .split("]")[0]
                                .split("[")[1]
                                .split(",")
                            ].index(str(self.__id))
                            messagebox.showinfo(
                                "Can't process",
                                "Bạn đã có dữ liệu nhận dạng, hãy xóa dữ liệu cũ",
                            )
                        except:
                            idpos = -1
                    if idpos < 0:
                        self.__frame1.forget()
                        self.__frame2 = Frame(self.__master)
                        self.__label = Label(self.__frame2)
                        self.__label.pack()
                        self.__frame2.pack(fill="both", expand=1)
                        Button(
                            self.__frame2,
                            text="Next Step",
                            fg="Green",
                            font=("Arial", 15, "bold"),
                            command=self.__trainingData,
                        ).pack()
                        self.__master.unbind("<Return>")
                        self.__getData()
                else:
                    messagebox.showwarning(
                        "Can't Sign In", "Sai ID hoặc không có trong hệ thống"
                    )
        else:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")

    def __loading(self):
        ml = Tk()
        Label(
            ml, text="Signed in, loading", fg="Green", font=("Arial", 15, "bold")
        ).pack()
        ml.after(1300, ml.destroy)
        ml.mainloop()

    def __getData(self):
        th2 = threading.Thread(name="Thread-2", target=self.__loading)
        th2.start()
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.__getData1(cap)

    def __getData1(self, cap):
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = self.__face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if not os.path.exists("dataSet"):
                os.mkdir("dataSet")
            self.__temp += 1
            cv2.imwrite(
                r"dataSet\User." + str(self.__id) + "." + str(self.__temp) + ".jpg",
                gray[y : y + h, x : x + w],
            )
        if self.__temp >= 50:
            self.__temp = 0
            messagebox.showinfo("Get Info Done", "Lấy dữ liệu thành công")
        else:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(img)
            self.__label.config(image=imgtk)
            self.__label.image_names = imgtk
            self.__label.after(10, lambda: self.__getData1(cap))

    def __prgbar(self, mpgb, thr2):
        thr2.start()
        for i in range(5):
            mpgb["value"] += 20
            time.sleep(1)
            self.__frame3.update_idletasks()

    def __trainingData(self):
        thr2 = threading.Thread(name="Thread-2", target=self.__trainingData1)
        self.__frame2.forget()
        self.__frame3 = Frame(self.__master)
        mpgb = ttk.Progressbar(
            self.__frame3, orient="horizontal", length=200, mode="determinate"
        )
        mpgb.pack(pady=200)
        Button(
            self.__frame3,
            text="Start training data",
            fg="Green",
            font=("Arial", 15, "bold"),
            command=lambda: self.__prgbar(mpgb, thr2),
        ).place(x=215, y=300)
        self.__frame3.pack(fill="both", expand=1)

    def __trainingData1(self):
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            recognizer.read("..\\recognizer\\trainingData.yml")
            path = "dataSet"
            ImgPaths = [
                os.path.join(path, i)
                for i in os.listdir(path)
                if i.startswith("User." + str(self.__id) + ".")
            ]
            faces, id = [], []
            for ImgPath in ImgPaths:
                faceNp = np.array(Image.open(ImgPath).convert("L"), "uint8")
                faces.append(faceNp)
                id.append(int(ImgPath.split(".")[1]))

            recognizer.update(faces, np.array(id))
            recognizer.save("..\\recognizer\\trainingData.yml")
            messagebox.showinfo("Done", "Training data success")
            self.__frame3.forget()
            self.__frame1Config()
        except:
            if os.path.exists("recognizer"):
                shutil.rmtree("recognizer")
            if not os.path.exists(os.getcwd() + r"\recognizer\trainingData.yml"):
                if not os.path.exists("recognizer"):
                    os.mkdir("recognizer")
                    firebase.dowload()
            self.__trainingData1()

    def __addStudent(self):
        try:
            if not ConnectionCheck.internet_on():
                messagebox.showwarning("Lost Connection", "Không có kết nối mạng")
            else:
                self.__frame1.forget()
                self.__addFrame = Addstudent.MyFrame(self.__master)
                self.__addFrame.pack()
                self.__frame1Config()
        except:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")

    def __MyClass(self):
        self.__frame4 = ViewMyClass.MyFrame1(self.__frame1)
        # self.__frame4.pack()

    def __deleteRecognizer(self, etr):
        connection = False
        try:
            if not ConnectionCheck.internet_on():
                raise Exception
            else:
                connection = True
        except Exception:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")
        if connection == True:
            self.__id = etr.get()

            if self.__id == "":
                messagebox.showwarning("Can't Sign In", "Tài khoản không được để trống")
            else:
                connect = sqlite3.connect("..\database\database.db")
                query = "SELECT * FROM people WHERE ID=" + str(self.__id)
                cursor = connect.execute(query)

                isRecordExist = 0
                for row in cursor:
                    if int(self.__id) == int(row[0]):
                        isRecordExist = 1

                if isRecordExist == 1:

                    self.__master.unbind("<Return>")
                    self.__deleteFace(self.__id)
                else:
                    messagebox.showwarning(
                        "Can't Sign In", "Sai ID hoặc không có trong hệ thống"
                    )
        else:
            messagebox.showwarning("Lost Connection", "Không có kết nối mạng")

    def __deleteFace(self, n):
        path_yml = "..\\recognizer\\trainingData.yml"
        path_save = "..\\recognizer\\trainingData.yml"
        with open(path_yml, "r+") as f:
            s = ""
            l = []
            for i in f:
                if "      - !!opencv-matrix" in i:
                    l.append(s)
                    s = i
                elif "   labels: !!opencv-matrix" in i:
                    l.append(s)
                    s = i
                else:
                    s += i
            l.append(s)
            l1 = l[len(l) - 1].split("]")
            l2 = l1[0].split("[")
            l3 = l2[1].split(",")
            vt = []
            oldQ = len(l3)
            for i, j in enumerate(l3):
                if str(n) in j.split():
                    vt.append(i)
            svt = vt[0]
            for i in range(len(vt)):
                l.pop(svt + 1)
                l3.pop(svt)
            l3 = [i.strip() for i in l3]
            for i, j in enumerate(l3):
                if i != (len(l3) - 1):
                    l3[i] += ","
                if (i + 1) % 12 == 0 and i != 1:
                    l3[i] = j + ",\n         "
            l2[1] = "[ " + " ".join(l3) + " ]"
            oldPos = l2[0].find(str(oldQ))
            endPos = oldPos + l2[0][oldPos:].find(" ") - 1
            l2[0] = l2[0].replace(l2[0][oldPos:endPos], str(len(l3)))
            l1 = "".join(l2) + l1[1] + "]"
            s = ""
            for i in range(len(l) - 1):
                s += l[i]
            s = s + l1 + "\n"
        f2 = open(path_save, "w")
        f2.write(s)
        messagebox.showinfo("Done", "Xóa nhận dạng thành công")


root = Tk()
mg = MyGui(root)
root.mainloop()
cv2.destroyAllWindows()

