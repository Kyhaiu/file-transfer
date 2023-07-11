import socket
import time
from tqdm import tqdm

# IP = socket.gethostbyname(socket.gethostname())


def main(chunk_size):
    IP = 'localhost'
    PORT = 8080
    ADDR = (IP, PORT)
    SIZE = chunk_size
    FORMAT = 'utf-8'
    BLOCKS = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[+] Listening...")

    conn, addr = server.accept()
    print(f"[+] Client connected from {addr[0]}:{addr[1]}")

    data = conn.recv(SIZE).decode(FORMAT)
    item = data.split("_")
    FILENAME = item[0]
    FILESIZE = int(item[1])

    print("[+] Filename and filesize received from the client.")
    conn.send("Filename and filesize received".encode(FORMAT))

    bar = tqdm(range(
        FILESIZE), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=1000)

    with open(f'recv_{FILENAME}', 'w') as f:
        while True:
            data = conn.recv(SIZE).decode(FORMAT)

            if not data:
                break

            f.write(data)
            conn.send("Data received".encode(FORMAT))
            BLOCKS = BLOCKS + 1
            bar.update(len(data))

    conn.close()
    server.close()

    return BLOCKS


if __name__ == "__main__":
    file_sizes = [100, 500, 1000]
    total_blocks = 0
    total_time = 0

    results = []

    for size in file_sizes:
        for i in range(2):
            print("Processing file with chunk size: {}".format(size))
            start_time = time.perf_counter_ns()
            blocks = main(size)
            end_time = time.perf_counter_ns()
            execution_time = (end_time - start_time) / 1000000
            print(f"No Blocks received: {blocks}")
            results.append([size, blocks, execution_time])
            total_blocks += blocks
            total_time += execution_time

    print(f"Total blocks received: {total_blocks} in {total_time} ms")

    for i, result in enumerate(results):
        print("Chunk size: {}".format(result[0]))
        print("Received Blocks: {}".format(result[1]))
        print("Execution time: {} ms\n".format(result[2]))
        print("-------------------------------------------------")
