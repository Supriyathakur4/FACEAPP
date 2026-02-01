import pyrebase

firebase_config = {
    "apiKey": "AIzaSyDgpCUGHw3jjzOCzCxw2CZlCbMUgk855ic",
    "authDomain": "faceapp-874e7.firebaseapp.com",
    "projectId": "faceapp-874e7",
    "storageBucket": "faceapp-874e7.firebasestorage.app",
    "messagingSenderId": "792623592191",
    "appId": "1:792623592191:web:9c0f2c0f7b60e49ad512ca",
    "databaseURL": "https://faceapp-874e7-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()
db = firebase.database()

