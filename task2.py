import time
import multiprocessing


# Функція для факторизації числа
def factorize_number(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


# Функція для паралельного обчислення факторизації
def factorize_parallel(*numbers):
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        results = pool.map(factorize_number, numbers)
    return results


# Основна функція
if __name__ == '__main__':
    # Тестування факторизації
    start_time = time.time()
    a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()

    print("Factors of 128:", a)
    print("Factors of 255:", b)
    print("Factors of 99999:", c)
    print("Factors of 10651060:", d)

    print(f"Час виконання паралельної версії: {end_time - start_time:.4f} секунд")

    # Синхронне виконання
    start_time_sync = time.time()
    a_sync = factorize_number(128)
    b_sync = factorize_number(255)
    c_sync = factorize_number(99999)
    d_sync = factorize_number(10651060)
    end_time_sync = time.time()

    print("Factors of 128 (sync):", a_sync)
    print("Factors of 255 (sync):", b_sync)
    print("Factors of 99999 (sync):", c_sync)
    print("Factors of 10651060 (sync):", d_sync)

    print(f"Час виконання синхронної версії: {end_time_sync - start_time_sync:.4f} секунд")

