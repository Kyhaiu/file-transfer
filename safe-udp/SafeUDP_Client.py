import socket
import os
import time
from tqdm import tqdm


def main(file_size):
    IP = '186.224.72.34'
    PORT = 8080
    ADDR = (IP, PORT)
    SIZE = file_size
    FORMAT = 'utf-8'
    FILENAME = 'data.txt'
    FILESIZE = os.path.getsize(FILENAME)
    ACK = 'ack'
    NACK = 'nack'
    BLOCKS = 0

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(ADDR)
    client.settimeout(15.0)

    PACK_NUM = int(FILESIZE / SIZE) + 1
    print(f"{PACK_NUM} Packages for this file")
    data = f"{FILENAME}_{FILESIZE}"
    client.send(data.encode(FORMAT))
    msg, addr = client.recvfrom(SIZE)
    print(f"SERVER: {msg.decode(FORMAT)}")

    bar = tqdm(range(FILESIZE), f"Sending {FILENAME}",
               unit="B", unit_scale=True, unit_divisor=SIZE)

    with open(FILENAME, 'r') as f:
        client.send(ACK.encode(FORMAT))
        msg, addr = client.recvfrom(SIZE)

        while True:
            data = f.read(SIZE)

            if not data:
                client.send('Finish'.encode(FORMAT))
                msg = client.recvfrom(SIZE)
                break

            client.send(data.encode(FORMAT))
            BLOCKS = BLOCKS + 1
            msg, addr = client.recvfrom(SIZE)
            while msg == NACK:
                client.send(data.encode(FORMAT))
                msg = client.recvfrom(SIZE)

            bar.update(len(data))

    client.close()


if __name__ == '__main__':
    file_sizes = [100, 500, 1000]

    for size in file_sizes:
        for i in range(10):
            print(f"Processing file of size: {size}")
            time.sleep(1)
            main(size)
