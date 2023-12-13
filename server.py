import cv2
import socket
import pickle
import struct

def send_image(conn, image):
    _, img_encoded = cv2.imencode('.jpg', image)
    data = pickle.dumps(img_encoded, protocol=3)
    size = struct.pack('>L', len(data))
    conn.sendall(size + data)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)

    print("Waiting for a connection...")
    connection, address = server_socket.accept()
    print(f"Connected to {address}")

    camera = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                continue

            send_image(connection, frame)

    finally:
        camera.release()
        connection.close()
        server_socket.close()

if __name__ == "__main__":
    server()
