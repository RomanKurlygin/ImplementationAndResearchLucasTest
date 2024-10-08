import matplotlib.pyplot as plt


# Функция проверки простоты Лукаса-Лемера (используем оригинальную, неоптимизированную версию для честного тестирования)
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


# Список чисел Кармайкла до определенного предела (используем заранее известный список чисел Кармайкла)
carmichael_numbers = [
    561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657,
    52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461,
    252601, 278545, 294409, 314821, 334153, 340561, 399001, 410041, 449065,
    488881, 512461
]


# Функция для подсчета ошибок теста простоты Лукаса на числах Кармайкла
def count_lucas_errors(carmichael_numbers):
    errors = 0
    for n in carmichael_numbers:
        if is_prime_lucas(n):
            errors += 1
    return errors


# Количество ошибок теста Лукаса
error_count = count_lucas_errors(carmichael_numbers)
total_count = len(carmichael_numbers)
correct_count = total_count - error_count

# Выводим количество ошибок
print(f"Количество ошибок теста простоты Лукаса: {error_count}")

# Данные для круговой диаграммы
labels = 'Correct', 'Errors'
sizes = [correct_count, error_count]
colors = ['lightgreen', 'lightcoral']
explode = (0, 0.1)  # выделение сектора с ошибками

# Строим круговую диаграмму
plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
plt.axis('equal')  # Сохраняем круглый вид диаграммы
plt.title('Errors in Lucas Primality Test on Carmichael Numbers')
plt.show()