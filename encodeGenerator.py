import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://faceattendancesys-rtdb-default-rtdb.firebaseio.com/",  # Firebase Database Link
    "storageBucket": "faceattendancesys-rtdb.appspot.com"
})

# Importing Student Images
folderPath = "images"
imgPathList = os.listdir(folderPath)
print(imgPathList)
imgList = []
studentIDs = []
for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))  # Join the Image Directory & grab items (Student Images)
    studentIDs.append(os.path.splitext(path)[0])  # Splitting the Path & grab first Path Item (Student ID)
    # print(os.path.splitext(path)[0])

    # Adding Student Images to Database While Encode this file
    fileName = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIDs)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnown_IDs = [encodeListKnown, studentIDs]
# print(encodeListKnown)
print("Encoding Complete")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnown_IDs, file)
file.close()
print("File Saved")
