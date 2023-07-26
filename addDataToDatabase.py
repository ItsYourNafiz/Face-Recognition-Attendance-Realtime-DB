from _weakref import ref

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://faceattendancesys-rtdb-default-rtdb.firebaseio.com/"  # Firebase Database Link
})

# Reference Path of Our Database
ref = db.reference("Students")

# Write Data Format
data = {
    "212010091": {
        "name": "Nafiz",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Good",
        "totalAttendance": 15,
        "year": 2,
        "lastAttendanceTime": "2022-05-20 10:05:35"
    },
    "212010023": {
        "name": "Chandra Saha Esha",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Excellent",
        "totalAttendance": 18,
        "year": 2,
        "lastAttendanceTime": "2022-05-20 10:05:35"
    },
    "212010080": {
        "name": "Rajesh Barua",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Fair",
        "totalAttendance": 8,
        "year": 2,
        "lastAttendanceTime": "2022-05-20 10:05:35"
    },
    "212010183": {
        "name": "Sojib Shimanto",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Good",
        "totalAttendance": 10,
        "year": 2,
        "lastAttendanceTime": "2022-05-20 10:05:35"
    },
    "212010208": {
        "name": "Anamul Haque Shohel",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Good",
        "totalAttendance": 11,
        "year": 2,
        "lastAttendanceTime": "2022-05-20 10:05:35"
    }
}

for key, value in data.items():
    ref.child(key).set(value)


