# Download and import the below required packages
import cv2
import socket
import struct
import pickle
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Setting up the IP and port to connect to the server
# The port numbers for client and server must be same
client_socket.connect(('127.0.0.1', 8099))
connection = client_socket.makefile('wb')

# Setting the VideoCapture value as '0', meaning we are using the in-built webcam and not an external webcam
cam = cv2.VideoCapture(0)

# Setting the height and width of the display window
cam.set(18, 320);
cam.set(12, 240);

img_counter = 0

# Taking each frame as a JPEG image of particular quality(0 - 100). The higher the value.
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # Starting the reading of frames from the webcam
    ret, frame = cam.read()
    # Encoding each frame before sending it to the server
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    o_data = pickle.dumps(frame, 0)
    o_size = len(o_data)
    print("Size before compression", o_size)
    # Compressing each frame after encoding and sending it to the server
    data = zlib.compress(pickle.dumps(frame, 0))
    c_size = len(data)
    print("Size after compression", c_size)
    # Sending data to the server
    client_socket.sendall(struct.pack(">L", c_size) + data)
    img_counter += 1

