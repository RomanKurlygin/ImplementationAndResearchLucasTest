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

# Счетчики правильных и ошибочных результатов
correct_counts = []
error_counts = []

# Подсчет правильных и ошибочных результатов для каждого числа Кармайкла
for n in carmichael_numbers:
    if is_prime_lucas(n):
        correct_counts.append(1)
        error_counts.append(0)
    else:
        correct_counts.append(0)
        error_counts.append(1)

# Строим график
plt.figure(figsize=(10, 6))
plt.plot(carmichael_numbers, correct_counts, label='Правильные')
plt.plot(carmichael_numbers, error_counts, label='Ошибки')
plt.xlabel('Числа Кармайкла')
plt.ylabel('Число')
plt.title('Зависимость правильных и ошибок от числа Кармайкла')
plt.legend()
plt.grid(True)
plt.show()

# Списки для хранения результатов теста Лукаса
results = []
for n in carmichael_numbers:
    result = is_prime_lucas(n)
    results.append(result)

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(carmichael_numbers, results, marker='o', linestyle='-', color='b', label='Результаты теста Лукаса')
plt.axhline(y=0.5, color='r', linestyle='--', label='Граница между ошибкой и правильным результатом')
plt.yticks([0, 1], ['Composite', 'Prime'])
plt.xlabel('Carmichael Numbers')
plt.ylabel('Lucas Test Result')
plt.title('Lucas Primality Test Results on Carmichael Numbers')
plt.legend()
plt.grid(True)
plt.show()


# Функция для получения результатов теста Лукаса на числах Кармайкла
def lucas_test_results(carmichael_numbers):
    results = []
    for n in carmichael_numbers:
        if is_prime_lucas(n):
            results.append(0)  # Ошибка: число Кармайкла прошло тест как простое
        else:
            results.append(1)  # Правильно определено как составное
    return results


# Получаем результаты теста
results = lucas_test_results(carmichael_numbers)

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(carmichael_numbers, results, 'bo-', label='Lucas Test Results')
plt.axhline(y=1, color='g', linestyle='--', label='Correct Classification')
plt.axhline(y=0, color='r', linestyle='--', label='Incorrect Classification')
plt.xlabel('Carmichael Numbers')
plt.ylabel('Test Result (1=Correct, 0=Incorrect)')
plt.title('Lucas Primality Test Results on Carmichael Numbers')
plt.legend()
plt.grid(True)
plt.show()


# Функция для получения результатов теста Лукаса на числах Кармайкла
def lucas_test_results(carmichael_numbers):
    results = []
    for n in carmichael_numbers:
        if is_prime_lucas(n):
            results.append(0)  # Ошибка: число Кармайкла прошло тест как простое
        else:
            results.append(1)  # Правильно определено как составное
    return results


# Получаем результаты теста
results = lucas_test_results(carmichael_numbers)

# Вычисляем вероятность ошибок на каждом этапе
error_probabilities = []
cumulative_errors = 0
for i, result in enumerate(results):
    if result == 0:  # Ошибка
        cumulative_errors += 1
    error_probabilities.append(cumulative_errors / (i + 1))

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(carmichael_numbers) + 1), error_probabilities, 'r-', marker='o')
plt.xlabel('Number of Carmichael Numbers Tested')
plt.ylabel('Probability of Error')
plt.title('Probability of Error in Lucas Primality Test on Carmichael Numbers')
plt.grid(True)
plt.show()


