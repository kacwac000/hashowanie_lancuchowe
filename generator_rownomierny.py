import os
import random
import string

NUM_INSERTS = 100
KEY_LENGTH = 5
VALUE_LENGTH = 8
FILENAME = "test_rownomierny.txt"

filepath = os.path.join(r"TU SCIEZKA", FILENAME)

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

with open(filepath, "w", encoding="utf-8") as f:
    for i in range(NUM_INSERTS):
        key = f"key{i:03d}"
        value = random_string(VALUE_LENGTH)
        f.write(f"INSERT {key} {value}\n")

print(f"Plik '{filepath}' wygenerowany z {NUM_INSERTS} poleceniami INSERT.")
