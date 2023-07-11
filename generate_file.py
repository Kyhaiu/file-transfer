import random
import string

# Size of the file in megabytes
file_size_mb = 100

# Convert megabytes to bytes
file_size_bytes = file_size_mb * 1024 * 1024

# Generate random string of given length


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# Open file for writing
with open('data.txt', 'w') as file:
    bytes_written = 0
    while bytes_written < file_size_bytes:
        # Generate random string of length between 100 and 1000 characters
        random_string = generate_random_string(random.randint(100, 1000))

        # Write the string to the file
        file.write(random_string)

        # Get the size of the written string in bytes
        bytes_written += len(random_string.encode('utf-8'))

print(f"File 'output.txt' with size {file_size_mb}MB generated successfully.")
