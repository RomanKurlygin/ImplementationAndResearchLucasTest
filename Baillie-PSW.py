
import random

# Реализация теста Лукаса
def is_prime_lucas(n):
    # Если число меньше 2, оно не является простым
    if n < 2:
        return False
    # Число 2 является простым
    if n == 2:
        return True
    # Четные числа, кроме 2, не являются простыми
    if n % 2 == 0:
        return False

    # Вложенная функция для выполнения теста Лукаса-Лемера
    def lucas_lehmer_test(p):
        s = 4
        M = 2** p - 1  # Число Мерсенна
        for _ in range(p - 2):
            s = (s * s - 2) % M
        return s == 0

    # Применение теста Лукаса-Лемера для числа n
    return lucas_lehmer_test(n.bit_length() - 1)


# Реализация теста Ферма
def is_prime_fermat(n, k=5):
    # Если число меньше или равно 1, оно не является простым
    if n <= 1:
        return False
    # Числа 2 и 3 являются простыми
    if n <= 3:
        return True
    # Четные числа не являются простыми
    if n % 2 == 0:
        return False

    # Повторяем тест k раз для повышения точности
    for _ in range(k):
        a = random.randint(2, n - 2)  # Выбираем случайное число в диапазоне [2, n-2]
        # Проверяем малую теорему Ферма
        if pow(a, n - 1, n) != 1:
            return False
    return True


# Комбинированный тест Лукаса и Ферма
def is_prime_combined(n):
    # Если n mod 5 равно 2 или 3, применяем оба теста
    if n % 5 in (2, 3):
        return is_prime_lucas(n) and is_prime_fermat(n)
    # Если n mod 5 равно 1 или 4, применяем один из тестов
    elif n % 5 in (1, 4):
        return is_prime_lucas(n) or is_prime_fermat(n)
    # В остальных случаях число не проходит тест
    else:
        return False


# Поиск контрпримеров
def find_counterexamples(range_start, range_end):
    counterexamples = []
    for n in range(range_start, range_end):
        # Ищем контрпримеры для n mod 5 = 1 или 4
        if (n % 5 == 1 or n % 5 == 4) and is_prime_combined(n) and not is_prime_lucas(n) and not is_prime_fermat(n):
            counterexamples.append(n)
    return counterexamples


# Проверка чисел в заданном диапазоне
range_start = 1
range_end = 100000

# Фиксируем генератор случайных чисел для повторяемости
random.seed(45)

counterexamples = find_counterexamples(range_start, range_end)
print(f"Counterexamples found: {counterexamples}")

# Код с общим тестом Лукаса, есои будет необходим

# import random
# import time

# # Простая реализация общего теста Лукаса
# def is_prime_lucas(n):
#     if n < 2:
#         return False
#     if n == 2 or n == 3:
#         return True
#     if n % 2 == 0:
#         return False

#     # Простой тест, основанный на последовательностях Лукаса
#     def lucas_sequence(n):
#         if n < 2:
#             return False
#         if n % 2 == 0:
#             return False
#         if n == 2:
#             return True
#         u, v = 1, 1
#         for i in range(1, n):
#             u, v = v, (u + v) % n
#         return u == 0

#     return lucas_sequence(n)

# # Реализация теста Ферма
# def is_prime_fermat(n, k=5):
#     if n <= 1:
#         return False
#     if n <= 3:
#         return True
#     if n % 2 == 0:
#         return False

#     for _ in range(k):
#         a = random.randint(2, n - 2)
#         if pow(a, n - 1, n) != 1:
#             return False
#     return True

# # Комбинированный тест Лукаса и Ферма
# def is_prime_combined(n):
#     return is_prime_fermat(n) and is_prime_lucas(n)

# # Поиск контрпримеров
# def find_counterexamples(range_start, range_end):
#     counterexamples = []
#     for n in range(range_start, range_end):
#         if n % 5 in (1, 4) and is_prime_combined(n):
#             # Если число проходит тесты Ферма и Лукаса, но оно составное
#             if not (is_prime_fermat(n) and is_prime_lucas(n)):
#                 counterexamples.append(n)
#     return counterexamples

# # Проверка чисел в заданном диапазоне
# range_start = 1
# range_end = 100000

# # Фиксируем генератор случайных чисел для повторяемости
# # random.seed(45)

# start_time = time.time()
# counterexamples = find_counterexamples(range_start, range_end)
# end_time = time.time()

# print(f"Counterexamples found: {counterexamples}")
# print(f"Time taken: {end_time - start_time:.2f} seconds")