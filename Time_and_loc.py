import time
import random
import matplotlib.pyplot as plt
import tracemalloc


# Реализация тестов простоты

def is_prime_lucas(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    def lucas_lehmer_test(p):
        s = 4
        M = 2 ** p - 1
        for _ in range(p - 2):
            s = (s * s - 2) % M
        return s == 0

    return lucas_lehmer_test(n.bit_length() - 1)


def is_prime_miller_rabin(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(r):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True


def is_prime_solovay_strassen(n, k=5):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    def jacobi(a, n):
        if a == 0:
            return 0
        if a == 1:
            return 1
        if a % 2 == 0:
            if n % 8 == 1 or n % 8 == 7:
                return jacobi(a // 2, n)
            elif n % 8 == 3 or n % 8 == 5:
                return -jacobi(a // 2, n)
        if a % 4 == 3 and n % 4 == 3:
            return -jacobi(n % a, a)
        else:
            return jacobi(n % a, a)

    def trial_composite(a):
        jacobian = (n + jacobi(a, n)) % n
        mod = pow(a, (n - 1) // 2, n)
        return jacobian == 0 or mod != jacobian

    for _ in range(k):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True


def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
    return primes


def is_prime_fermat(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True


# Функция для генерации случайных чисел
def generate_random_numbers(count, lower, upper):
    return [random.randint(lower, upper) for _ in range(count)]


# Функция для измерения времени выполнения и использования памяти
def measure_time_and_memory(func, args):
    tracemalloc.start()
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, peak, result


# Диапазоны чисел для экспериментов
number_ranges = [(10, 100), (100, 1000), (1000, 10000)]

# Словарь для хранения результатов
results_time = {name: [] for name in
                ['Лукас', 'Миллера-Рабина', 'Соловея Штрассена', 'Решето Эратосфена', 'теорема Ферма']}
results_memory = {name: [] for name in
                  ['Лукас', 'Миллера-Рабина', 'Соловея Штрассена', 'Решето Эратосфена', 'теорема Ферма']}

# Запуск тестов и сбор данных
for lower, upper in number_ranges:
    random_numbers = generate_random_numbers(100, lower, upper)
    for name, func in [('Лукас', is_prime_lucas),
                       ('Миллера-Рабина', is_prime_miller_rabin),
                       ('Соловея Штрассена', is_prime_solovay_strassen),
                       ('Решето Эратосфена', sieve_of_eratosthenes),
                       ('теорема Ферма', is_prime_fermat)]:
        times = []
        memories = []
        for num in random_numbers:
            if name == 'Решето Эратосфена':
                time_taken, memory_used, _ = measure_time_and_memory(func, (upper,))
            else:
                time_taken, memory_used, _ = measure_time_and_memory(func, (num,))
            times.append(time_taken)
            memories.append(memory_used)
        results_time[name].append(sum(times) / len(times))
        results_memory[name].append(sum(memories) / len(memories))
        print(f'{name} test, range {lower}-{upper}: {times}, {memories}')

# Построение графиков времени выполнения
for name, times in results_time.items():
    plt.plot([r[1] for r in number_ranges], times, label=name)

plt.xlabel('Upper Bound of Number Range')
plt.ylabel('Average Time (s)')
plt.title('Comparison of Primality Tests - Time Complexity')
plt.legend()
plt.show()

# Построение графиков использования памяти
for name, memories in results_memory.items():
    plt.plot([r[1] for r in number_ranges], memories, label=name)

plt.xlabel('Upper Bound of Number Range')
plt.ylabel('Average Memory Usage (bytes)')
plt.title('Comparison of Primality Tests - Space Complexity')
plt.legend()
plt.show()

# Построение графиков времени выполнения для каждого теста
for name, times in results_time.items():
    plt.plot([r[1] for r in number_ranges], times, label=name)
    plt.xlabel('Upper Bound of Number Range')
    plt.ylabel('Average Time (s)')
    plt.title('Comparison of Primality Tests - Time Complexity')
    plt.legend()
    plt.show()

# Построение графиков использования памяти для каждого теста
for name, memories in results_memory.items():
    plt.plot([r[1] for r in number_ranges], memories, label=name)
    plt.xlabel('Upper Bound of Number Range')
    plt.ylabel('Average Memory Usage (bytes)')
    plt.title('Comparison of Primality Tests - Space Complexity')
    plt.legend()
    plt.show()

# Общий график времени выполнения
for name, times in results_time.items():
    plt.plot([r[1] for r in number_ranges], times, label=name)

plt.xlabel('Upper Bound of Number Range')
plt.ylabel('Average Time (s)')
plt.title('Comparison of Primality Tests - Time Complexity')
plt.legend()
plt.show()

# Общий график использования памяти
for name, memories in results_memory.items():
    plt.plot([r[1] for r in number_ranges], memories, label=name)

plt.xlabel('Upper Bound of Number Range')
plt.ylabel('Average Memory Usage (bytes)')
plt.title('Comparison of Primality Tests - Space Complexity')
plt.legend()
plt.show()

# С диаграммой:
import time
import random
import matplotlib.pyplot as plt
import tracemalloc

# Реализация тестов простоты

def is_prime_lucas(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    def lucas_lehmer_test(p):
        s = 4
        M = 2**p - 1
        for _ in range(p - 2):
            s = (s * s - 2) % M
        return s == 0

    return lucas_lehmer_test(n.bit_length() - 1)

def is_prime_miller_rabin(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(r):
            if pow(a, 2**i * d, n) == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True

def is_prime_solovay_strassen(n, k=5):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    def jacobi(a, n):
        if a == 0:
            return 0
        if a == 1:
            return 1
        if a % 2 == 0:
            if n % 8 == 1 or n % 8 == 7:
                return jacobi(a // 2, n)
            elif n % 8 == 3 or n % 8 == 5:
                return -jacobi(a // 2, n)
        if a % 4 == 3 and n % 4 == 3:
            return -jacobi(n % a, a)
        else:
            return jacobi(n % a, a)

    def trial_composite(a):
        jacobian = (n + jacobi(a, n)) % n
        mod = pow(a, (n - 1) // 2, n)
        return jacobian == 0 or mod != jacobian

    for _ in range(k):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True

def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
    return primes

def is_prime_fermat(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

# Функция для генерации случайных чисел
def generate_random_numbers(count, lower, upper):
    return [random.randint(lower, upper) for _ in range(count)]

# Функция для измерения времени выполнения и использования памяти
def measure_time_and_memory(func, args):
    tracemalloc.start()
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, peak, result

# Диапазоны чисел для экспериментов
number_ranges = [(10, 100), (100, 1000), (1000, 10000)]

# Словарь для хранения результатов
results_time = {name: [] for name in ['Лукас', 'Миллера-Рабина', 'Соловея Штрассена', 'Решето Эратосфена', 'теорема Ферма']}
results_memory = {name: [] for name in ['Лукас', 'Миллера-Рабина', 'Соловея Штрассена', 'Решето Эратосфена', 'теорема Ферма']}

# Запуск тестов и сбор данных
for lower, upper in number_ranges:
    random_numbers = generate_random_numbers(100, lower, upper)
    for name, func in [('Лукас', is_prime_lucas),
                       ('Миллера-Рабина', is_prime_miller_rabin),
                       ('Соловея Штрассена', is_prime_solovay_strassen),
                       ('Решето Эратосфена', sieve_of_eratosthenes),
                       ('теорема Ферма', is_prime_fermat)]:
        times = []
        memories = []
        for num in random_numbers:
            if name == 'Решето Эратосфена':
                time_taken, memory_used, _ = measure_time_and_memory(func, (upper,))
            else:
                time_taken, memory_used, _ = measure_time_and_memory(func, (num,))
            times.append(time_taken)
            memories.append(memory_used)
        results_time[name].append(sum(times) / len(times))
        results_memory[name].append(sum(memories) / len(memories))
        print(f'{name} test, range {lower}-{upper}: {times}, {memories}')

# Построение графиков времени выполнения
plt.figure(figsize=(14, 7))
for name, times in results_time.items():
    plt.plot([r[1] for r in number_ranges], times, label=name)

plt.xlabel('Upper Bound of Number Range')
plt.ylabel('Average Time (s)')
plt.title('Comparison of Primality Tests - Time Complexity')
plt.yscale('log')  # Установка логарифмической шкалы на оси Y
plt.legend()
plt.grid(True)
plt.show()

# Построение графиков использования памяти
plt.figure(figsize=(14, 7))
for name, memories in results_memory.items():
    plt.plot([r[1] for r in number_ranges], memories, label=name)

plt.xlabel('Upper Bound of Number Range')
plt.ylabel('Average Memory Usage (bytes)')
plt.title('Comparison of Primality Tests - Space Complexity')
plt.yscale('log')  # Установка логарифмической шкалы на оси Y
plt.legend()
plt.grid(True)
plt.show()
