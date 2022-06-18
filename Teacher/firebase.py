import threading
import pyrebase, sqlite3, os

config = {
    "apiKey": "AIzaSyB_LH8lyCg4bdgUHZhsmeyNmUtOjoB22mA",
    "authDomain": "qlsv-ea25d.firebaseapp.com",
    "databaseURL": "qlsv-ea25d.firebaseapp.com",
    "projectId": "qlsv-ea25d",
    "storageBucket": "qlsv-ea25d.appspot.com",
    "messagingSenderId": "911368744543",
    "appId": "1:911368744543:web:04dd657c6f99b2bf27f5ea",
    "measurementId": "G-1BKR6BV3NM",
}
config_a = {
    "apiKey": "AIzaSyCb_ge32xry68dj8yHLcVD8bvTSsBYJR3Q",
    "authDomain": "htnam-72b75.firebaseapp.com",
    "databaseURL": "htnam-72b75.firebaseapp.com",
    "projectId": "htnam-72b75",
    "storageBucket": "htnam-72b75.appspot.com",
    "messagingSenderId": "264425807306",
    "appId": "1:264425807306:web:e5a50cd02888d3e655c333",
}

configDtb = {
    "apiKey": "AIzaSyB_LH8lyCg4bdgUHZhsmeyNmUtOjoB22mA",
    "authDomain": "qlsv-ea25d.firebaseapp.com",
    "databaseURL": "https://qlsv-ea25d-default-rtdb.firebaseio.com/",
    "projectId": "qlsv-ea25d",
    "storageBucket": "qlsv-ea25d.appspot.com",
    "messagingSenderId": "911368744543",
    "appId": "1:911368744543:web:04dd657c6f99b2bf27f5ea",
    "measurementId": "G-1BKR6BV3NM",
}


try:
    firebase = pyrebase.initialize_app(config)
    firebase.storage().child("text.txt").put(os.path.join(os.getcwd(), "test.txt"))
except:
    firebase = pyrebase.initialize_app(config_a)
storage = firebase.storage()
database = pyrebase.initialize_app(configDtb).database()

local_path = "recognizer/trainingData.yml"
cloud_path = "recognizer/trainingData.yml"


def dowload():
    storage.child(cloud_path).download(local_path, cloud_path)


def dowloadDatabase():
    storage.child("../database/database.db").download(
        r"../database/database.db", "../database/database.db"
    )


def upload():
    storage.child(cloud_path).put(local_path)


def uploadDatabase():
    storage.child("../database/database.db").put("../database/database.db")


def delete():
    storage.delete(cloud_path)


def resetTime(id):
    database.child("ID").child(str(id)).update({"Time": 0})


def getTime(id):
    return database.child("ID").get().val().get(str(id))["Time"]


def updateTime(id, t):
    database.child("ID").child(str(id)).update({"Time": t})


def setClassStatus(st):
    database.child("ClassStatus").update({"Status": st})


def getClassStatus():
    return database.child("ClassStatus").get().val()["Status"]


def config():
    database.child("ID").remove()
    connect = sqlite3.connect(r"../database/database.db")
    cursor = connect.execute("SELECT * FROM people")
    lst = [i[0] for i in cursor]
    for i in lst:
        updateTime(str(i), 0)
    connect.commit()
    connect.close()
