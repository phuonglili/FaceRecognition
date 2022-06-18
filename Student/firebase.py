import pyrebase, os

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

configDatabase = {
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
database = pyrebase.initialize_app(configDatabase).database()

dtbLocalPath = dtbCloudPath = "../database/database.db"
tnLocalPath = tnCloudPath = "recognizer/trainingData.yml"


def dowloadDtb():
    if not os.path.exists("database"):
        os.mkdir("database")
    storage.child(dtbCloudPath).download(dtbLocalPath, dtbCloudPath)


def dowloadTrainingData():
    if not os.path.exists("recognizer"):
        os.mkdir("recognizer")
    storage.child(tnCloudPath).download(tnLocalPath, tnCloudPath)


def uploadDtb():
    storage.child(dtbCloudPath).put(dtbLocalPath)


def uploadTrainingData():
    storage.child(tnCloudPath).put(tnLocalPath)


def setClassStatus(st):
    database.child("ClassStatus").update({"Status": st})


def getClassStatus():
    try:
        return database.child("ClassStatus").get().val()["Status"]
    except:
        return 0


# setNewRecord
# database.child("1111").set({"Time": 5})

# getRecord
# e = database.child("1111").get()
# print(dict(e.val())["Time"])


def updateTime(id, t):
    database.child("ID").child(str(id)).update({"Time": int(t)})


def getTime(id):
    return database.child("ID").get().val().get(str(id))["Time"]


# delete "1111"
# database.child("1111").remove()
