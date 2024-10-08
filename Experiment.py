# 1.1. Тест простоты Лукаса

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


# 1.2. Тест Миллера-Рабина

import random


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


# 1.3. Тест Соловея-Штрассена

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


# 1.4. Решето Эратосфена

def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
    return primes


# 1.5. Тест малой теоремы Ферма

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


import time
import matplotlib.pyplot as plt
import random
import numpy as np


# Генерация случайных чисел
def generate_random_numbers(count, lower, upper):
    return [random.randint(lower, upper) for _ in range(count)]


# Измерение времени выполнения функции
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result


# Словарь тестов простоты чисел
test_functions = {
    'Lucas': is_prime_lucas,  # Тест Лукаса
    'Miller-Rabin': is_prime_miller_rabin,  # Тест Миллера-Рабина
    'Solovay-Strassen': is_prime_solovay_strassen,  # Тест Соловея-Штрассена
    'Eratosthenes': sieve_of_eratosthenes,  # Решето Эратосфена
    'Fermat': is_prime_fermat  # Тест малой теоремы Ферма
}

# Диапазоны чисел для тестирования
number_ranges = [(1000, 10000), (10000, 100000), (100000, 1000000)]

# Результаты выполнения тестов
results = {name: [] for name in test_functions}

# Запуск тестов на каждом диапазоне чисел
for lower, upper in number_ranges:
    random_numbers = generate_random_numbers(100, lower, upper)  # Генерация 100 случайных чисел в заданном диапазоне
    for name, func in test_functions.items():
        times = []
        for num in random_numbers:
            if name == 'Eratosthenes':
                time_taken, _ = measure_time(func, upper)  # Для решета Эратосфена передаем верхнюю границу
            else:
                time_taken, _ = measure_time(func, num)  # Для остальных тестов передаем число
            times.append(time_taken)
        results[name].append(sum(times) / len(times))  # Среднее время выполнения для текущего диапазона

# Построение столбчатой диаграммы
labels = [f'{lower}-{upper}' for lower, upper in number_ranges]
x = np.arange(len(labels))  # метки местоположения на оси X
width = 0.15  # ширина столбцов

fig, ax = plt.subplots(figsize=(12, 8))

# Построение столбцов для каждого теста
for i, (name, times) in enumerate(results.items()):
    ax.bar(x + i * width, times, width, label=name)

# Настройка осей и меток
ax.set_xlabel('Number Range')
ax.set_ylabel('Average Time (s)')
ax.set_title('Comparison of Primality Tests')
ax.set_yscale('log')  # Установка логарифмической шкалы на оси Y
ax.set_xticks(x + width * (len(results) - 1) / 2)
ax.set_xticklabels(labels)
ax.legend()

plt.show()

#Код для построения графиков


import matplotlib.pyplot as plt

def plot_test(name, times, number_ranges):
    plt.plot([r[1] for r in number_ranges], times, label=name)
    plt.xlabel('Number Range')
    plt.ylabel('Average Time (s)')
    plt.title(f'Comparison of {name} Primality Test')
    plt.legend()
    plt.show()

for name, times in results.items():
    plot_test(name, times, number_ranges)

# Общий график
for name, times in results.items():
    plt.plot([r[1] for r in number_ranges], times, label=name)

plt.xlabel('Number Range')
plt.ylabel('Average Time (s)')
plt.title('Comparison of Primality Tests')
plt.legend()
plt.show()