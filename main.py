from datetime import datetime
import time

import pytz
import uvicorn
import models.employee as models
import schemas.employee as schemas
from config.db import engine
from fastapi import FastAPI, status
import routers.employee as employee
import routers.status as status
import routers.admin as admin
import routers.auth as auth
import routers.job as job
import routers.attendance as attendance
import routers.attendance_status as attendance_status
from fastapi.middleware.cors import CORSMiddleware
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import mysql.connector


app= FastAPI()

models.Base.metadata.create_all(engine)
now = datetime.now(pytz.timezone('Asia/Singapore'))
# Setup CORS middleware
origins = [
    "http://localhost",
    "https://admin-production-b634.up.railway.app/"
    "https://employee-production.up.railway.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)

app.include_router(employee.router)

app.include_router(status.router)

app.include_router(admin.router)

app.include_router(job.router)

app.include_router(attendance_status.router)

app.include_router(attendance.router)



# def detect_faces_in_dataset():
#     face_classifier = cv2.CascadeClassifier(
#         "C:/Users/rizal/PycharmProjects/FlaskOpenCV_FaceDetection/resources/haarcascade_frontalface_default.xml")

#     dataset_dir = "static/Images"  # Directory containing the images
#     face_dataset_dir = "static/face_dataset"  # Directory to save the detected face images

#     if not os.path.exists(face_dataset_dir):
#         os.makedirs(face_dataset_dir)

#     for filename in os.listdir(dataset_dir):
#         if filename.endswith(".jpg"):
#             img_path = os.path.join(dataset_dir, filename)
#             img = cv2.imread(img_path)

#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             faces = face_classifier.detectMultiScale(gray, 1.3, 5)

#             if len(faces) > 0:
#                 for (x, y, w, h) in faces:
#                     face_img = img[y:y+h, x:x+w]
#                     face_img = cv2.resize(face_img, (200, 200))
#                     face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    
#                     face_file_path = os.path.join(face_dataset_dir, filename)
#                     cv2.imwrite(face_file_path, face_img)

#                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     cv2.destroyAllWindows()

# def train_classifier():
#     dataset_dir = "static/face_dataset"

#     path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
#     faces = []
#     ids = []

#     for image in path:
#         img = Image.open(image).convert('L')
#         imageNp = np.array(img, 'uint8')
#         id = int(os.path.split(image)[1].split(".")[1])

#         faces.append(imageNp)
#         ids.append(id)
#     ids = np.array(ids)

#     # Train the classifier and save
#     clf = cv2.face.LBPHFaceRecognizer_create()
#     clf.train(faces, ids)
#     clf.write("classifier.xml")

#     return {'status': 'success'}

# Membuat koneksi ke database
mydb = mysql.connector.connect(
    host="containers-us-west-110.railway.app",
    user="root",
    password="5awcXt09ZHlr1xwxZLie",
    database="railway",
    port= 6395
)

# Mendapatkan cursor untuk menjalankan query
mycursor = mydb.cursor()

import datetime
import pytz

def create(request,id):
    # Mendapatkan waktu saat ini dengan timezone Asia/Singapore
    now = datetime.datetime.now(pytz.timezone('Asia/Singapore'))
    
     # Memeriksa apakah data dengan tanggal saat ini dan ID tersebut sudah ada di database
    check_query = """
    SELECT COUNT(*) FROM tabelattendance WHERE date = %s AND employee_id = %s
    """
    cursor = mydb.cursor()
    cursor.execute(check_query, (now.date(), id))
    result = cursor.fetchone()
    count = result[0]
    
    # Jika data dengan tanggal saat ini dan ID tersebut sudah ada di database
    if count > 0:
        # Memeriksa waktu saat ini dan memperbarui absen yang sesuai
        update_query = """
        UPDATE tabelattendance SET absen_1 = CASE
            WHEN HOUR(%s) >= 8 AND HOUR(%s) < 9 THEN %s
            ELSE absen_1
        END,
        absen_2 = CASE
            WHEN HOUR(%s) >= 11 AND HOUR(%s) < 12 THEN %s
            ELSE absen_2
        END,
        absen_3 = CASE
            WHEN HOUR(%s) >= 13 AND HOUR(%s) < 15 THEN %s
            ELSE absen_3
        END,
        absen_4 = CASE
            WHEN HOUR(%s) >= 16 AND HOUR(%s) < 23 THEN %s
            ELSE absen_4
        END
        WHERE date = %s AND employee_id = %s
        """
        update_data = (
            now, now, now,
            now, now, now,
            now, now, now,
            now, now, now,
            now.date(), id
        )
        cursor.execute(update_query, update_data)
        
        # Commit perubahan ke database
        mydb.commit()
        
        # Mengembalikan pesan sukses
        return {
            "message": "Data absensi telah diperbarui."
        }
    
    # Jika data dengan tanggal saat ini belum ada di database
    else:
        attendance1 = models.Attendance(
            date=request.date,
            absen_1=request.absen_1,
            absen_2=request.absen_2,
            absen_3=request.absen_3,
            absen_4=request.absen_4,
            employee_id=request.employee_id,
            attendance_status_id=1
        )
    
        # Menjalankan query INSERT untuk data absensi baru
        add_attendance_query = """
        INSERT INTO tabelattendance (date, absen_1, absen_2, absen_3, absen_4, employee_id, attendance_status_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        attendance_data = (
            attendance1.date, attendance1.absen_1, attendance1.absen_2, attendance1.absen_3,
            attendance1.absen_4, attendance1.employee_id, attendance1.attendance_status_id
        )
        cursor.execute(add_attendance_query, attendance_data)
        
        # Commit perubahan ke database
        mydb.commit()
        
        # Mendapatkan ID yang baru saja di-generate oleh database
        attendance_id = cursor.lastrowid
    
        # Mengembalikan data attendance yang telah disimpan
        return {
            "id": attendance_id,
            "absen_1": attendance1.absen_1,
            "absen_2": attendance1.absen_2,
            "absen_3": attendance1.absen_3,
            "absen_4": attendance1.absen_4,
            "employee_id": attendance1.employee_id,
            "attendance_status_id": attendance1.attendance_status_id
        }


cnt = 0
pause_cnt = 0
justscanned = False 
def face_recognition():  # generate frame by frame from camera
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        global justscanned
        global pause_cnt

        pause_cnt += 1

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 70 and not justscanned:
                global cnt
                cnt += 1

                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w

                cv2.putText(img, str(int(n)) + ' %', (x + 20, y + h + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (153, 255, 255), 2, cv2.LINE_AA)

                cv2.rectangle(img, (x, y + h + 40), (x + w, y + h + 50), color, 2)
                cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled), y + h + 50), (153, 255, 255), cv2.FILLED)

                mycursor.execute("select a.employee_id, b.name "
                                 "  from tabeldataset a "
                                 "  left join tabelpegawai b on a.employee_id = b.id "
                                 " where a.id = " + str(id))
                row = mycursor.fetchone()
                pnbr = row[0]
                pname = row[1]


                if int(cnt) == 30:

                    # mycursor.execute("insert into tabelattendance (absen_1, employee_id) values('" + str(
                    #     date.today())+""+""+"" + "', '" + pnbr + "')")
                    # mycursor.execute("INSERT INTO attendance (absen_1, employee_id, attendance_status_id) VALUES (%s, %s, %s)")
                    # mydb.commit()
                    cv2.putText(img, pname , (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (153, 255, 255), 2, cv2.LINE_AA)
                    time.sleep(1)
                    if now.hour >= 8 and now.hour < 9:
                        request= schemas.Attendance1(
                            employee_id=pnbr
                        )
                    if now.hour >= 11 and now.hour < 12:
                        request= schemas.Attendance2(
                            employee_id=pnbr
                        )
                    if now.hour >= 13 and now.hour < 15:
                        request= schemas.Attendance3(
                            employee_id=pnbr
                        )
                    if now.hour >= 16 and now.hour < 23:
                        request= schemas.Attendance4(
                            employee_id=pnbr
                        )
                    create(request,pnbr)
                    justscanned = True
                    pause_cnt = 0
                    cnt = 0


                    

            else:
                if not justscanned:
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                if pause_cnt > 80:
                    justscanned = False

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    wCam, hCam = 400, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while justscanned == False:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break
    

@app.get('/video_feed')
async def video_feed():
    global justscanned
    justscanned=False
    return StreamingResponse(face_recognition(), media_type='multipart/x-mixed-replace; boundary=frame')






