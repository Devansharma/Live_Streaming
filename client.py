import cv2
import socket
import pickle
import struct

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created ...")

port = 1234
server_ip = "192.168.43.93"
skt.connect((server_ip,port))
data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = skt.recv(4*1024)
        if not packet: 
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size =  struct.unpack("Q",packed_msg_size)[0]

    while len(data) < msg_size:
        data+= skt.recv(4*1024)
    img_data = data[:msg_size]
    data = data[msg_size:]
    img = pickle.loads(img_data)
    cv2.imshow("Recieving Live video", img)
    if cv2.waitKey(10) == 13:
        cv2.destroyAllWindows()
        break
skt.close()
