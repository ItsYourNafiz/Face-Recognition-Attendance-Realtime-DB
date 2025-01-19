import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import streamlit as st
import time

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://faceattendancesys-rtdb-default-rtdb.firebaseio.com/",  # Firebase Database Link
    "storageBucket": "faceattendancesys-rtdb.appspot.com"
})

bucket = storage.bucket()

# Initialize Webcam
cam = cv2.VideoCapture(0)  # Initialize WebCam
cam.set(3, 640)  # Set Webcam Resolution-Width
cam.set(4, 480)  # Set Webcam Resolution-Height

# Load Background Interface
imgBackground = cv2.imread("Resources/backgroundMe.png")

# Load The Mode Images into a List
modePath = "Resources/Modes"
modesPathList = os.listdir(modePath)
imgModeList = []
for path in modesPathList:
    imgModeList.append(cv2.imread(os.path.join(modePath, path)))
# print(imgModeList)

# Load Face Encodings
print("Loading Encode File ...")
file = open("EncodeFile.p", "rb")
encodeListKnown_IDs = pickle.load(file)
file.close()
encodeListKnown, studentIDs = encodeListKnown_IDs
# print(studentIDs)
print("Encode File Loaded ...")

# Initialize Variables
modeType = 0  # Set the Default Mode (Active)
counter = 0
iD = -1
studentImage = []

while True:
    success, frame = cam.read()

    # Resize and Convert Frame for Face Recognition
    # To do this, Make Images Squeezed/Scaled Down into One-Fourth of the Original Images to Reduce Computation Power.
    imgSmall = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Detect Faces and Compute Encodings
    faceCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurFrame = face_recognition.face_encodings(imgSmall, faceCurFrame)

    # Set Background Image Position to Frame (WEBCAM)
    imgBackground[165:165 + 480, 60:60 + 640] = frame
    # Set Background Image Position to Frame (Attendance Status)
    imgBackground[55:55 + 633, 820:820 + 414] = imgModeList[modeType]

    # Loop Through All Tee Encodings & Compare one-by-one Whether it's Match or not
    if faceCurFrame:
        for encodeFace, face_location in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("Matches", matches)
            # print("Face Distance", faceDistance)

            # Matching the Index Value of the Matches. Minimum Value Matches
            matchIndex = np.argmin(faceDistance)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print("Known Face Detected", studentIDs[matchIndex])  # Print Known Student ID's with Matched Faces.

                # Adjusting the Bounding Box Around Detected Faces
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 165 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                iD = studentIDs[matchIndex]
                # print(iD)
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (290, 401))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Retrieve student info
                studentsInfo = db.reference(f"Students/{iD}").get()
                print(studentsInfo)

                # Retrieve Student Image
                blob = bucket.get_blob(f"images/{iD}.jpg")
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                studentImage = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update Data of Attendance
                datetimeObject = datetime.strptime(studentsInfo['lastAttendanceTime'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f"Students/{iD}")
                    studentsInfo['totalAttendance'] += 1
                    ref.child('totalAttendance').set(studentsInfo['totalAttendance'])
                    ref.child('lastAttendanceTime').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[55:55 + 633, 820:820 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
                imgBackground[55:55 + 633, 820:820 + 414] = imgModeList[modeType]

                if counter <= 10:
                    # Display Student Info
                    cv2.putText(imgBackground, str(studentsInfo['totalAttendance']), (875, 160), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentsInfo['batch']), (1020, 586), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(iD), (990, 540), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentsInfo['standings']), (894, 662), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (50, 50, 50), 1)
                    cv2.putText(imgBackground, str(studentsInfo['year']), (1028, 662), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (50, 50, 50), 1)
                    cv2.putText(imgBackground, str(studentsInfo['startingYear']), (1160, 662), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (50, 50, 50), 1)

                    # Calculate Text Size and Position to Center the Name
                    (w, h), _ = cv2.getTextSize(studentsInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentsInfo['name']), (995 + offset, 498), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (50, 50, 50), 1)
                    imgBackground[210:210 + 256, 880:880 + 256] = studentImage

                counter += 1
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentsInfo = []
                    studentImage = []
                    imgBackground[55:55 + 633, 820:820 + 414] = imgModeList[modeType]
            #else:
                print("Unknown Face Detected")
    else:
        modeType = 0
        counter = 0

    # cv2.imshow("Webcam", frame)     # Launch Webcam
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
