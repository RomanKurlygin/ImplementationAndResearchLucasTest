import time
import matplotlib.pyplot as plt


# Функция для измерения времени выполнения
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time


# Обычный тест простоты Лукаса-Лемера для чисел Мерсенна
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


# Простой тест на простоту, проверка делимости до квадратного корня из n
def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    # Более эффективная проверка на простоту
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# Оптимизированный тест Лукаса-Лемера с предварительной проверкой на простоту
def is_prime_lucas_optimized(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    def lucas_lehmer_test(p):
        s = 4
        M = (1 << p) - 1
        for _ in range(p - 2):
            s = (s * s - 2) % M
        return s == 0

    # Проверка на простоту через числа Мерсенна
    return is_prime(n) and lucas_lehmer_test(n.bit_length() - 1)


# Значения n для проверки (шаг 100 для уменьшения количества тестов и улучшения визуализации)
values = list(range(10000, 10000000, 100))

# Измеряем время выполнения для обычной и оптимизированной функций
total_time_normal = 0
total_time_optimized = 0

for n in values:
    _, time_normal = measure_time(is_prime_lucas, n)
    _, time_optimized = measure_time(is_prime_lucas_optimized, n)
    total_time_normal += time_normal
    total_time_optimized += time_optimized

# Данные для прямоугольной диаграммы
labels = ['Обычная версия', 'Оптимизированная версия']
times = [total_time_normal, total_time_optimized]

# Построение прямоугольной диаграммы
fig, ax = plt.subplots()
ax.bar(labels, times, color=['blue', 'green'])

ax.set_xlabel('Версии')
ax.set_ylabel('Общее время выполнения (сек)')
ax.set_title('Сравнение общего времени выполнения')

for i, v in enumerate(times):
    ax.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom')

plt.show()