import grpc
import cv2
import numpy as np
from concurrent import futures
import video_streaming_pb2
import video_streaming_pb2_grpc
import face_recognition
import pickle
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
import ssl

# Email sending function
def sendemail(path):
    email_sender = ''
    email_password = ''
    email_receiver = ''

    subject = 'Stranger Alert!'
    body = "Alert! Unknown Body Detected!"

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.attach(MIMEText(body, 'plain'))

    with open(path, 'rb') as file:
        img_data = file.read()
    img_part = MIMEImage(img_data)
    img_part.add_header('Content-Disposition', 'attachment', filename='Stranger')
    em.attach(img_part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Load known faces and embeddings
print("[INFO] loading encodings + face detector...")
encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())

currentname = "unknown"
flag = False

class VideoStreamingServicer(video_streaming_pb2_grpc.VideoStreamingServiceServicer):
    def StreamVideo(self, request_iterator, context):
        global currentname, flag

        for video_frame in request_iterator:
            frame = np.frombuffer(video_frame.frame, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            boxes = face_recognition.face_locations(frame)
            encodings = face_recognition.face_encodings(frame, boxes)
            names = []

            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "Unknown"

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)

                    if currentname != name:
                        currentname = name
                        print(currentname)

                if name == "Unknown" and not flag:
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    image_path = f"unknown_{timestamp}.jpg"
                    cv2.imwrite(image_path, frame)
                    sendemail(image_path)
                    os.remove(image_path)
                    flag = True
                    break

                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

            cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or flag:
                break

        cv2.destroyAllWindows()
        return video_streaming_pb2.VideoResponse(message="Stream ended")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_streaming_pb2_grpc.add_VideoStreamingServiceServicer_to_server(VideoStreamingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


