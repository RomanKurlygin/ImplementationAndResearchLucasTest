import matplotlib.pyplot as plt
import random


# 1.1. Тест Миллера-Рабина
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


# 1.2. Тест Соловея-Штрассена
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


# 1.3. Решето Эратосфена
def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[0], is_prime[1] = False, False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    return is_prime


def is_prime_sieve(n):
    if n <= 1:
        return False
    primes = sieve_of_eratosthenes(n)
    return primes[n]


# 1.4. Тест малой теоремы Ферма
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


# 1.5. Тест Лукаса
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


# Список чисел Кармайкла
carmichael_numbers = [
    561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657,
    52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461,
    252601, 278545, 294409, 314821, 334153, 340561, 399001, 410041, 449065,
    488881, 512461
]


# Функция для проверки чисел Кармайкла на каждом из тестов
def test_primality_algorithms(carmichael_numbers):
    results = {
        'Miller-Rabin': [],
        'Solovay-Strassen': [],
        'Eratosthenes': [],
        'Fermat': [],
        'Lucas': []
    }

    for n in carmichael_numbers:
        results['Miller-Rabin'].append(is_prime_miller_rabin(n))
        results['Solovay-Strassen'].append(is_prime_solovay_strassen(n))
        results['Eratosthenes'].append(is_prime_sieve(n))
        results['Fermat'].append(is_prime_fermat(n))
        results['Lucas'].append(is_prime_lucas(n))

    return results


# Получаем результаты тестирования
results = test_primality_algorithms(carmichael_numbers)

# Подсчитываем количество ошибок для каждого теста
error_counts = {test: sum(results[test]) for test in results}
total_count = len(carmichael_numbers)
correct_counts = {test: total_count - error_counts[test] for test in results}


# Функция для отображения числовых значений на круговой диаграмме
def absolute_value(val, sizes):
    a = int(val / 100. * sum(sizes))
    return f'{a}' if a != 0 else ''


# Строим круговую диаграмму для каждого теста
for test in results:
    if test != 'Lucas':
        sizes = [correct_counts[test], error_counts[test]]
        labels = ['Correct', 'Errors']
        colors = ['lightgreen', 'lightcoral']
        explode = (0, 0.1)  # выделение сектора с ошибками

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda val: absolute_value(val, sizes),
                shadow=True, startangle=140)

        plt.axis('equal')  # Сохраняем круглый вид диаграммы
        plt.title(f'Errors in {test} Primality Test on Carmichael Numbers')
        plt.show()

# Данные для общей круговой диаграммы
labels = list(results.keys())
sizes = [correct_counts[test] for test in labels]
errors = [error_counts[test] for test in labels]
colors = ['lightgreen', 'lightblue', 'lightcoral', 'lightyellow', 'lightpink']
explode = (0, 0.1, 0.1, 0.1, 0.1)  # выделение секторов с ошибками

sizes = [correct_counts[test] for test in labels]
# Строим общую круговую диаграмму
plt.figure(figsize=(12, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda val: absolute_value(val, sizes),
        shadow=True, startangle=140)

plt.axis('equal')  # Сохраняем круглый вид диаграммы
plt.title('Correct Results in Primality Tests on Carmichael Numbers')
plt.show()