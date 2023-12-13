import socket
import threading as th
import struct
import pickle
import cv2


class Server:
    _server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host = "127.0.0.1", port = 12345):
        self._server.bind((host, port))
        self._server.listen(5)

    
    def acceptClients(self):
        while True:
            client, addr = self._server.accept()

            th.Thread(target= lambda : self.receiveImage(client)).start()


    def receiveImage(self, client):
        try:
            while True:
                size = client.recv(4)
                size = struct.unpack('!I', size)[0]

                data = b""
                while len(data) < size:
                    packet = client.recv(size - len(data))
                    if not packet:
                        break
                    data += packet

                frame = pickle.loads(data)

                cv2.imshow('Received Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            client.close()
            cv2.destroyAllWindows()



if __name__ == "__main__":

    server = Server()
    server.acceptClients()
