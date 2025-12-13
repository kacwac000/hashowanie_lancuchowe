import random
import string
import math
import os
TABLE_SIZE = 10
N = 1000       # liczba elementów
mu = (TABLE_SIZE - 1) / 2  # środek bucketów
sigma = 2.0                 # odchylenie standardowe

FILENAME = "test_gauss.txt"
filepath = os.path.join(r"TU SCIEZKA", FILENAME)
# wyliczamy liczność elementów w każdym bucketu wg Gaussa
buckets_counts = []
for i in range(TABLE_SIZE):
    prob = math.exp(-(i - mu) ** 2 / (2 * sigma ** 2))
    buckets_counts.append(prob)
total_prob = sum(buckets_counts)
buckets_counts = [int(N * x / total_prob) for x in buckets_counts]

def random_key_for_bucket(bucket_index):
    while True:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        if sum(ord(c) for c in key) % TABLE_SIZE == bucket_index:
            return key

with open(filepath, "w", encoding="utf-8") as f:
    for bucket_index, count in enumerate(buckets_counts):
        for _ in range(count):
            key = random_key_for_bucket(bucket_index)
            value = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            f.write(f"INSERT {key} {value}\n")

print(f"Wygenerowano {sum(buckets_counts)} wpisów w pliku {FILENAME}")
