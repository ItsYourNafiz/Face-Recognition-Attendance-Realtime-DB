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
    "212010032": {
        "name": "Tusher",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Good",
        "totalAttendance": 1,
        "year": 1,
        "lastAttendanceTime": "2021-10-15 10:02:20"
    },
    "212010057": {
        "name": "Chandra",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Excellent",
        "totalAttendance": 2,
        "year": 1,
        "lastAttendanceTime": "2021-10-15 10:02:20"
    },
    "212010091": {
        "name": "Nafiz",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Excellent",
        "totalAttendance": 5,
        "year": 1,
        "lastAttendanceTime": "2021-10-15 10:02:20"
    },
    "212010208": {
        "name": "Sohel",
        "department": "Computer Science & Engineering",
        "batch": "CSE-10th",
        "startingYear": 2021,
        "standings": "Average",
        "totalAttendance": 1,
        "year": 1,
        "lastAttendanceTime": "2021-10-15 10:02:20"
    }
}

for key, value in data.items():
    ref.child(key).set(value)


