# packages that need to be installed to run the code
import socket
import cv2
import pickle
import struct
import zlib

# Setting the host and the port
HOST = ''
PORT = 8099

# The following two files need to be imported
# Each file contains the data regarding detection of the face and eyes
# Ensure that both the below files are in the same folder as the server file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


s = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

# Making the socket start accepting data from the client
conn, addr = s.accept()

# converting string type data to byte type data
data = b""

payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        # As long as length of received frame is less that considered size, we accept data
        # printing the packet size of each frame sent from client
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    # DeCompressing each frame of data received from the client
    frame = pickle.loads(zlib.decompress(frame_data), fix_imports=True, encoding="bytes")
    # DeCoding each frame of data after decompression
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # code for face and eye detection
    img = frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # complexion
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # Drawing the rectangle shape around the face once they are detected
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + h]
        roi_color = img[y:y + h, x:x + h]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        # Drawing the rectangle shape around the eyes once they are detected
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    # To display the image after the detection process
    cv2.imshow('haar', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # cv2.waitKey(1)