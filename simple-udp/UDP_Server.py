import socket
import time
from tqdm import tqdm

# IP = socket.gethostbyname(socket.gethostname())


def main(chunk_size):
    IP = 'localhost'
    PORT = 8080
    SIZE = chunk_size
    ADDR = (IP, PORT)
    FORMAT = 'utf-8'
    BLOCKS = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    server.settimeout(15.0)
    print('[+] Waiting connection...')

    data, addr = server.recvfrom(SIZE)
    print(f"Recebi {data} de {addr}")
    prev = data.decode(FORMAT)
    item = prev.split("_")
    FILENAME = item[0]
    FILESIZE = int(item[1])
    server.sendto(b'Filename received', addr)

    bar = tqdm(range(
        FILESIZE), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=1000)

    with open(f'recv_{FILENAME}', 'w') as f:
        while True:
            data, addr = server.recvfrom(SIZE)

            if not data or data.decode(FORMAT) == 'F':
                server.sendto(b"Finish", addr)
                break

            f.write(data.decode(FORMAT))
            server.sendto(b"Data received", addr)
            BLOCKS = BLOCKS + 1
            bar.update(len(data))

    server.close()
    return BLOCKS


if __name__ == '__main__':
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
