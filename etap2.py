import time
import random
import matplotlib.pyplot as plt

def compute_pi(terms=10_000_000):
    pi = 0.0
    for k in range(terms):
        pi += (-1)**k / (2*k + 1)
    pi *= 4
    return pi

def random_key(n):
    return [str(i) for i in range(n)]

def benchmark_uniform(n):
    table = dict()
    keys = random_key(n)
    values = [random.randint(0, 1000000) for _ in range(n)]

    start = time.perf_counter()
    for k, v in zip(keys, values):
        table[k] = v
    t_insert = time.perf_counter() - start

    search_keys = keys[:n//2] + [str(n+i) for i in range(n//2)]
    random.shuffle(search_keys)
    start = time.perf_counter()
    for k in search_keys:
        _ = table.get(k, None)
    t_search = time.perf_counter() - start

    delete_keys = keys[:n//2]
    start = time.perf_counter()
    for k in delete_keys:
        table.pop(k, None)
    t_delete = time.perf_counter() - start

    return t_insert, t_search, t_delete

start_ref = time.perf_counter()
compute_pi(terms=5_000_000)
ref_time = time.perf_counter() - start_ref
print(f"Jednostka referencyjna: {ref_time:.6f} s")

sizes = [100, 1000, 10000, 100000, 1000000, 10000000]
insert_times, search_times, delete_times = [], [], []

for n in sizes:
    t_insert, t_search, t_delete = benchmark_uniform(n)
    insert_times.append(t_insert / ref_time)
    search_times.append(t_search / ref_time)
    delete_times.append(t_delete / ref_time)
    print(f"N={n}, INSERT={insert_times[-1]:.2f} π, SEARCH={search_times[-1]:.2f} π, DELETE={delete_times[-1]:.2f} π")

plt.figure(figsize=(10,6))
plt.plot(sizes, insert_times, marker='o', label='INSERT')
plt.plot(sizes, search_times, marker='s', label='SEARCH')
plt.plot(sizes, delete_times, marker='^', label='DELETE')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Liczba elementów (N)')
plt.ylabel('Czas / jednostka referencyjna (π)')
plt.title('Czas wykonania obliczeń')
plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend()
plt.tight_layout()
plt.show()
