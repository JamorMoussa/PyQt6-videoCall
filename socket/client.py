import socket
import pickle
import struct
import cv2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345
client_socket.connect((host, port))


camera = cv2.VideoCapture(0)

try:
    while True:
        # Capture a frame
        _, frame = camera.read()

        # Serialize the frame
        data = pickle.dumps(frame)
        size = struct.pack('!I', len(data))

        # Send the size of the data
        client_socket.sendall(size)

        # Send the serialized frame
        client_socket.sendall(data)

finally:
    camera.release()
    client_socket.close()
