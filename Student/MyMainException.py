from tkinter import messagebox


class IDException(Exception):
    def __init__(self, id) -> None:
        self.__id = id

    def warning(self):
        if len(self.__id) == 0:
            messagebox.showwarning("Error", "ID không được để trống")
        elif len(self.__id) > 10:
            messagebox.showwarning("Error", "ID không được dài hơn 10")
        elif not self.__id.isdigit():
            messagebox.showwarning("Error", "ID không được chứa kí tự")

    def __str__(self):
        return str(self.__id)


class PWException(Exception):
    def __init__(self, pw) -> None:
        self.__pw = pw

    def warning(self):
        if len(self.__pw) == 0:
            messagebox.showwarning("Error", "PW không được để trống")
        elif len(self.__pw) > 10:
            messagebox.showwarning("Error", "PW không được dài hơn 10")
        elif not self.__pw.isdigit():
            messagebox.showwarning("Error", "PW không được chứa kí tự")

    def __str__(self):
        return str(self.__pw)


class ReEnterPWException(Exception):
    def __init__(self, pw) -> None:
        self.__pw = pw

    def warning(self):
        if self.__pw.endswith("@notmatch@"):
            messagebox.showwarning("Error", "Nhập lại mật khẩu không khớp")
        else:
            messagebox.showwarning("Error", "Hãy nhập lại mật khẩu")

    def __str__(self):
        return str(self.__pw)


class MSVException(Exception):
    def __init__(self, msv) -> None:
        self.__msv = msv

    def warning(self):
        if len(self.__msv) == 0:
            messagebox.showwarning("Error", "MSV không được để trống")
        elif len(self.__msv) > 10:
            messagebox.showwarning("Error", "MSV không được dài hơn 10")
        elif not self.__msv.isdigit():
            messagebox.showwarning("Error", "MSV không được chứa kí tự")

    def __str__(self):
        return str(self.__msv)


class SDTException(Exception):
    def __init__(self, sdt) -> None:
        self.__sdt = sdt

    def warning(self):
        if len(self.__sdt) == 0:
            messagebox.showwarning("Error", "SDT không được để trống")
        elif len(self.__sdt) != 10:
            messagebox.showwarning("Error", "SDT phải có độ dài 10")
        elif not self.__sdt.isdigit():
            messagebox.showwarning("Error", "SDT không được chứa kí tự")
        elif self.__sdt[0] != "0":
            messagebox.showwarning("Error", "SDT phải chứa 0 ở trước")

    def __str__(self):
        return str(self.__sdt)


class NameException(Exception):
    def __init__(self, name):
        self.__name = name

    def warning(self):
        if len(self.__name) == 0:
            messagebox.showwarning("Error", "Tên không được để trống")
        elif len(self.__name) > 25:
            messagebox.showwarning("Error", "Tên không được dài quá 25 kí tự")
        elif not "".join(self.__name.split()).isalpha():
            messagebox.showwarning(
                "Error", "Tên không được chứa số hoặc kí tự đặc biệt"
            )


class ClassException(Exception):
    def __init__(self, mclass):
        self.__class = mclass

    def warning(self):
        if len(self.__class) == 0:
            messagebox.showwarning("Error", "Lớp không được để trống")
        elif len(self.__class) > 20:
            messagebox.showwarning("Error", "Lớp không được dài quá 20 kí tự")


class FolkException(Exception):
    def __init__(self, folk):
        self.__folk = folk

    def warning(self):
        if len(self.__folk) == 0:
            messagebox.showwarning("Error", "Dân tộc không được để trống")
        elif len(self.__folk) > 25:
            messagebox.showwarning("Error", "Dân tộc không được dài quá 25 kí tự")
        elif not "".join(self.__folk.split()).isalpha():
            messagebox.showwarning(
                "Error", "Dân tộc không được chứa số hoặc kí tự đặc biệt"
            )


class AddressException(Exception):
    def __init__(self, add):
        self.__add = add

    def warning(self):
        if len(self.__add) == 0:
            messagebox.showwarning("Error", "Địa chỉ không được để trống")
        elif len(self.__add) > 100:
            messagebox.showwarning("Error", "Địa chỉ không được dài quá 100 kí tự")
        elif not "".join(self.__add.split()).isalnum():
            messagebox.showwarning(
                "Error", "Địa chỉ không được chứa số hoặc kí tự đặc biệt"
            )


class MajorException(Exception):
    def __init__(self, major):
        self.__major = major

    def warning(self):
        if len(self.__major) == 0:
            messagebox.showwarning("Error", "Khoa không được để trống")
        elif len(self.__major) > 70:
            messagebox.showwarning("Error", "Khoa không được dài quá 70 kí tự")
        elif not "".join(self.__major.split()).isalpha():
            messagebox.showwarning(
                "Error", "Khoa không được chứa số hoặc kí tự đặc biệt"
            )


class GenderException(Exception):
    def __init__(self, gd):
        self.__gender = gd

    def warning(self):
        if self.__gender == "":
            messagebox.showwarning("Error", "Hãy thiết lập giới tính")


def checkID(id):
    if len(id) > 10 or len(id) == 0 or not id.isdigit():
        raise IDException(id)


def checkPW(pw):
    if len(pw) > 10 or len(pw) == 0 or not pw.isdigit():
        raise PWException(pw)


def checkMSV(msv):
    if len(msv) > 10 or len(msv) == 0 or not msv.isdigit():
        raise MSVException(msv)


def checkSDT(sdt):
    if len(sdt) == 0 or len(sdt) != 10 or sdt[0] != "0" or not sdt.isdigit():
        raise SDTException(sdt)


def checkName(name):
    if len(name) == 0 or len(name) > 25 or not "".join(name.split()).isalpha():
        raise NameException(name)


def checkClass(mclass):
    if len(mclass) == 0 or len(mclass) > 20:
        raise ClassException(mclass)


def checkMajor(major):
    if len(major) == 0 or len(major) > 70 or not "".join(major.split()).isalpha():
        raise MajorException(major)


def checkFolk(folk):
    if len(folk) == 0 or len(folk) > 25 or not "".join(folk.split()).isalpha():
        raise FolkException(folk)


def checkAddress(address):
    if (
        len(address) == 0
        or len(address) > 100
        or not "".join(address.split()).isalnum()
    ):
        raise AddressException(address)


def checkReEnterPass(p1, p2):
    if p2 == "":
        raise ReEnterPWException(p2)
    elif p1 != p2:
        raise ReEnterPWException(p2 + "@notmatch@")


def checkGender(gd):
    if gd == "":
        raise GenderException(gd)


def checkInfo(lst):
    checkName(lst[0])
    checkGender(lst[1])
    checkSDT(lst[2])
    checkFolk(lst[3])
    checkAddress(lst[4])
