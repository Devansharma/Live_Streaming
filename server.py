import cv2
import socket
import pickle
import struct

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created successfully")

port = 1234
skt.bind(("", port))
skt.listen()
print("Socket started")
 
while True:
    session, address = skt.accept()
    print("Connected to: ", address)
    if session:
        cam = cv2.VideoCapture(0)
        while(cam.isOpened()):
            ret, img = cam.read()
            data = pickle.dumps(img)
            msg = struct.pack("Q", len(data))+ data
            session.sendall(msg)
            cv2.imshow("Streaming Live Video",img)
            if cv2.waitKey(1) == 13:
                cv2.destroyAllWindows()
                session.close()
                break

