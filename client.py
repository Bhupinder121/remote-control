# Import socket module 
import socket	
import pickle	
import cv2
import struct
import pyautogui
import threading
import sys
from msvcrt import getch


def map(num, oldMin, oldMax, newMin, newMax): 
    return (num-oldMin)/(oldMax-oldMin)*(newMax-newMin)+newMin


def mouse_click(event, x, y,  flags, param): 
    global client_socket
    client_socket.send(struct.pack("QQ", x, y))

def connect():    
    global client_socket
    global keysThread
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8888))
    threading.Thread(target=getVideo).start()
    keysThread = threading.Thread(target=getKey)
    keysThread.start()



def getKey():
    global client_socket
    global key
    global stop
    lock = threading.Lock()
    while True:
        with lock:
            key = getch()
            if stop:
                break
            print(key)

def getVideo():
    global client_socket
    global keysThread
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        if not data:
            break
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)  # 4K buffer size
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        cv2.imshow('Client', frame)
        cv2.setMouseCallback("Client", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            stop = True
            keysThread.join()
            break
    cv2.destroyAllWindows()
    

if __name__=="__main__":
    client_socket = None
    key = "test"
    keysThread = None
    stop = False
    connect()
    