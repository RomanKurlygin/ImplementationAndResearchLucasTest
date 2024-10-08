# 1.1. Тест простоты Лукаса
def is_prime_lucas(n, k=5):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Вспомогательная функция для нахождения простых делителей числа
    def prime_factors(n):
        factors = set()
        for p in primerange(2, n + 1):
            if n % p == 0:
                factors.add(p)
                while n % p == 0:
                    n //= p
        return factors

    # Основной цикл теста
    for _ in range(k):
        # Выбираем случайное число в диапазоне от 2 до n-1
        a = random.randint(2, n - 1)
        # Проверяем условие pow(a, n-1, n) != 1
        if pow(a, n - 1, n) != 1:
            return False

        # Получаем простые делители числа n-1
        factors = prime_factors(n - 1)
        for q in factors:
            # Проверяем условие pow(a, (n - 1) // q, n) == 1
            if pow(a, (n - 1) // q, n) == 1:
                break
        else:
            return True

    return False


# 1.2. Тест Миллера-Рабина
# Статистический тест на простоту, использующий вероятность. k указывает количество раундов тестирования.
import random

def is_prime_miller_rabin(n, k=5):
    if n <= 1:
        return False  # Числа меньше или равные 1 не являются простыми
    if n <= 3:
        return True  # 2 и 3 - простые числа
    if n % 2 == 0:
        return False  # Четные числа, кроме 2, не являются простыми

    # Представляем n-1 как 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False  # a^d % n == 1
        for i in range(r):
            if pow(a, 2**i * d, n) == n - 1:
                return False  # a^(2^i * d) % n == n-1
        return True

    for _ in range(k):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False  # Составное число
    return True  # Число прошло все раунды тестирования

# 1.3. Тест Соловея-Штрассена
# Статистический тест на простоту, использующий символ Якоби и вероятностные проверки.
def is_prime_solovay_strassen(n, k=5):
    if n < 2:
        return False  # Числа меньше 2 не являются простыми
    if n == 2:
        return True  # 2 - простое число
    if n % 2 == 0:
        return False  # Четные числа, кроме 2, не являются простыми

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
            return False  # Составное число
    return True  # Число прошло все раунды тестирования

# 1.4. Решето Эратосфена
# Алгоритм нахождения всех простых чисел до заданного предела n.
def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)  # Создаем массив булевых значений, инициализированных True
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)  # p - простое число
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False  # Устанавливаем кратные p как составные
    return primes  # Возвращаем список простых чисел


# 1.5. Тест малой теоремы Ферма
# Статистический тест на простоту, использующий малую теорему Ферма.
def is_prime_fermat(n, k=5):
    if n <= 1:
        return False  # Числа меньше или равные 1 не являются простыми
    if n <= 3:
        return True  # 2 и 3 - простые числа
    if n % 2 == 0:
        return False  # Четные числа, кроме 2, не являются простыми

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False  # Составное число
    return True  # Число прошло все раунды тестирования