import socket
import os
import time
from tqdm import tqdm

# IP = socket.gethostbyname(socket.gethostname())


def main(chunk_size):
    IP = 'localhost'
    PORT = 8080
    ADDR = (IP, PORT)
    SIZE = chunk_size
    FORMAT = 'utf-8'
    FILENAME = 'data.txt'
    FILESIZE = os.path.getsize(FILENAME)
    BLOCKS = 0

    # cria socket UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(ADDR)
    client.settimeout(15.0)

    data = f"{FILENAME}_{FILESIZE}"
    client.send(data.encode(FORMAT))
    msg, addr = client.recvfrom(SIZE)
    print(f"SERVER: {msg.decode(FORMAT)}")

    bar = tqdm(range(FILESIZE), f"Sending {FILENAME}",
               unit="B", unit_scale=True, unit_divisor=1000)

    with open(FILENAME, 'r') as f:
        while True:
            data = f.read(SIZE)

            if not data:
                client.send('F'.encode(FORMAT))
                msg = client.recvfrom(SIZE)
                break

            client.send(data.encode(FORMAT))
            BLOCKS = BLOCKS + 1
            msg = client.recvfrom(SIZE)

            bar.update(len(data))

    client.close()


if __name__ == '__main__':
    file_sizes = [100, 500, 1000]

    for size in file_sizes:
        for i in range(2):
            print(f"Processing file of size: {size}")
            time.sleep(1)
            main(size)
