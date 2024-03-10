import numpy as np
import cv2
from PIL import ImageGrab
import socket
import pickle
import struct
import pyautogui
import threading
import keyboard



def map(num, oldMin, oldMax, newMin, newMax): 
    return (num-oldMin)/(oldMax-oldMin)*(newMax-newMin)+newMin

def listenting():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    server_socket.listen(5)
    print("Server is listening...")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=stream, args=(client_socket, client_address)).start()
        threading.Thread(target=getData, args=(client_socket,)).start()


def stream(client_socket, client_address):
    print(f"Connection from {client_address} accepted")
    while True:
        frame = np.array(ImageGrab.grab(bbox=(0, 0, width, height), all_screens=True))
        frame = cv2.resize(frame, (stream_width, stream_height))

        frame_data = pickle.dumps(frame)
        client_socket.sendall(struct.pack("Q", len(frame_data)))
        client_socket.sendall(frame_data)

        if cv2.waitKey(1) == 13:
            break
    cap.release()
    cv2.destroyAllWindows()

def getData(client_socket):
    while True:
        data = client_socket.recv(1024)
        if len(data) > 1:
            x = struct.unpack("QQ", data)[0]
            y = struct.unpack("QQ", data)[1]
            mouseX = round(map(x, 0, stream_width, 0, width))
            mouseY = round(map(y, 0, stream_height, 0, height))
            print(mouseX, mouseY)
        else:
            print(data)


if __name__=="__main__":
    width = pyautogui.size().width
    height = pyautogui.size().height
    stream_width = 1024
    stream_height = 768
    listenting()
