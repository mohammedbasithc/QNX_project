import socket
import threading

LISTEN_IP = "192.168.254.35"
LISTEN_PORT = 5000

QNX_IP = "10.0.0.1"
QNX_PORT = 5000


def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except:
        pass
    finally:
        try:
            src.close()
        except:
            pass
        try:
            dst.close()
        except:
            pass


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LISTEN_IP, LISTEN_PORT))
server.listen(5)

print("====================================")
print("       ESP32 -> QNX TCP RELAY")
print("====================================")
print("Listening:", LISTEN_IP, LISTEN_PORT)
print("Forwarding to:", QNX_IP, QNX_PORT)
print("Waiting for ESP32...")
print()

while True:
    esp, addr = server.accept()
    print("ESP32 connected:", addr)

    try:
        qnx = socket.create_connection((QNX_IP, QNX_PORT), timeout=10)
        print("Connected to QNX")
        
        threading.Thread(target=forward, args=(esp, qnx), daemon=True).start()
        threading.Thread(target=forward, args=(qnx, esp), daemon=True).start()

    except Exception as e:
        print("QNX connection failed:", e)
        esp.close()
