import random
import time
import json


def greedy_algorithm(m, n, u, p):
    """Жадібний алгоритм для мінімізації максимального часу закінчення робіт (makespan)
    та середнього зваженого часу проходження робіт в умовах паралельних ідентичних машин"""
    S = [[] for _ in range(m)]
    F = [0] * m

    jobs = [[p[i], u[i]] for i in range(n)]
    jobs.sort(key=lambda x: x[0] / x[1])

    for job in jobs:
        # Обрати машину j, яка має найменшу поточну тривалість проходження робіт F_j
        j = F.index(min(F))
        # Призначити роботу на машину
        S[j].append(job)
        # Перерахувати тривалість проходження роботи на машині
        F[j] += job[0]

    total_weighted_completion_time = 0
    for j in range(m):
        time_elapsed = 0
        for job in S[j]:
            time_elapsed += job[0]
            total_weighted_completion_time += job[1] * time_elapsed

    avg_weighted_completion_time = total_weighted_completion_time / sum(u)
    makespan = max(F)

    return S, avg_weighted_completion_time, makespan


def calculate_objective_local_search(S, m, u):
    """Обрахунок ЦФ (цільових функцій)"""
    total_weighted_completion_time = 0
    for j in range(m):
        time_elapsed = 0
        for job in S[j]:
            time_elapsed += job[0]
            total_weighted_completion_time += job[1] * time_elapsed
    avg_weighted_completion_time = total_weighted_completion_time / sum(u)
    makespan = max(sum(job[0] for job in S[j]) for j in range(m))
    return avg_weighted_completion_time, makespan


def fair_compromise_principle(new_avg_time, new_makespan, best_avg_time, best_makespan):
    """Принцип справедливого компромісу для порівняння розв’язків за двома критеріями"""
    return (((new_avg_time - best_avg_time) / min(best_avg_time, new_avg_time))
            + (new_makespan - best_makespan) / min(best_makespan, new_makespan))


def local_search_relocation(S_greedy, m, u):
    """Алгоритм локального пошуку з переміщенням роботи,
    базується на розв’язку, отриманому за допомогою жадібного алгоритму і покращує його"""
    best_S = [list(sublist) for sublist in S_greedy]
    best_avg_time, best_makespan = calculate_objective_local_search(best_S, m, u)

    for j in range(m):
        for k in range(m):
            if k == j:
                continue

            S_iter_best = [list(sublist) for sublist in best_S]

            for job in S_iter_best[j]:
                S_temp = [list(sublist) for sublist in S_iter_best]

                S_temp[j].remove(job)
                S_temp[k].append(job)

                S_temp[k].sort(key=lambda x: x[0] / x[1])

                avg_time, makespan = calculate_objective_local_search(S_temp, m, u)

                if fair_compromise_principle(avg_time, makespan, best_avg_time, best_makespan) < 0:
                    best_S = [list(sublist) for sublist in S_temp]
                    best_avg_time, best_makespan = avg_time, makespan
                    # print(f"{S_temp}\nchange, {job} {j=} {k=} {best_avg_time=}, {best_makespan=} \n")

    return best_S, best_avg_time, best_makespan


def local_search_exchange(S_greedy, m, u):
    """Алгоритм локального пошуку з обміном роботами,
    базується на розв’язку, отриманому за допомогою жадібного алгоритму і покращує його"""
    best_S = [list(sublist) for sublist in S_greedy]
    best_avg_time, best_makespan = calculate_objective_local_search(best_S, m, u)

    for i in range(m):
        for j in range(m):
            if i == j:
                continue

            S_iter_best = [list(sublist) for sublist in best_S]
            min_machine_jobs = min(len(S_iter_best[i]), len(S_iter_best[j]))

            for _ in range(min_machine_jobs):
                temp_S = [list(sublist) for sublist in S_iter_best]

                job_i = random.choice(temp_S[i])
                job_j = random.choice(temp_S[j])

                temp_S[i].remove(job_i)
                temp_S[j].remove(job_j)
                temp_S[i].append(job_j)
                temp_S[j].append(job_i)

                temp_S[i].sort(key=lambda x: x[0] / x[1])
                temp_S[j].sort(key=lambda x: x[0] / x[1])

                avg_time, makespan = calculate_objective_local_search(temp_S, m, u)

                if fair_compromise_principle(avg_time, makespan, best_avg_time, best_makespan) < 0:
                    best_S = [list(sublist) for sublist in temp_S]
                    best_avg_time, best_makespan = avg_time, makespan

    return best_S, best_avg_time, best_makespan


def input_data():
    """Введення даних"""
    m = int(input("Введіть кількість машин: "))
    n = int(input("Введіть кількість робіт: "))
    u = list(map(int, input("Введіть вектор ваг: ").split()))
    p = list(map(int, input("Введіть вектор тривалостей робіт: ").split()))
    return m, n, u, p


def generate_data(m, n, min_weight, max_weight, min_time, max_time):
    """Генерація даних"""
    u = [random.randint(min_weight, max_weight) for _ in range(n)]
    p = [random.randint(min_time, max_time) for _ in range(n)]
    return m, n, u, p


def save_data(filename, m, n, u, p) -> None:
    """Збереження даних"""
    data = {"m": m, "n": n, "u": u, "p": p}
    with open(filename, 'w') as f:
        json.dump(data, f)


def load_data(filename):
    """Читання даних з файлу"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['m'], data['n'], data['u'], data['p']


def edit_data(filename):
    """Редагування даних"""
    m, n, u, p = load_data(filename)
    print(f"Поточні дані: m={m}, n={n}, u={u}, p={p}")
    m = int(input(f"Введіть кількість машин (поточне значення {m}): ") or m)
    n = int(input(f"Введіть кількість робіт (поточне значення {n}): ") or n)
    u = list(map(int, input(f"Введіть вектор ваг (поточне значення {u}): ").split() or u))
    p = list(map(int, input(f"Введіть вектор тривалостей робіт (поточне значення {p}): ").split() or p))
    save_data(filename, m, n, u, p)


def solve_problem(m=None, n=None, u=None, p=None, filename=None):
    """Розв'язання задачі"""
    if filename:
        m, n, u, p = load_data(filename)
    elif not m or not n or not u or not p:
        m, n, u, p = input_data()

    start_time = time.time()
    S, avg_weighted_completion_time, makespan = greedy_algorithm(m, n, u, p)
    time_greedy = time.time() - start_time
    print("\n--- ЖАДІБНИЙ АЛГОРИТМ ---")
    print(f"Розклад:")
    for i, S_j in enumerate(S):
        print(f"М{i + 1}: {S_j}")
    print(f"Середній зважений час проходження робіт F_u: {avg_weighted_completion_time:.2f}")
    print(f"Максимальний час закінчення робіт F_max: {makespan}")

    print("\n--- АЛГОРИТМ ЛОКАЛЬНОГО ПОШУКУ З ПЕРЕМІЩЕННЯМ ---")
    start_time = time.time()
    S_local_relocation, avg_weighted_completion_time_relocation, makespan_relocation = local_search_relocation(S, m, u)
    time_relocation = time.time() - start_time
    print(f"Розклад:")
    for i, S_j in enumerate(S_local_relocation):
        print(f"М{i + 1}: {S_j}")
    print(f"Середній зважений час проходження робіт F_u: {avg_weighted_completion_time_relocation:.2f}")
    print(f"Максимальний час закінчення робіт F_max: {makespan_relocation}")

    print("\n--- АЛГОРИТМ ЛОКАЛЬНОГО ПОШУКУ З ОБМІНОМ ---")
    start_time = time.time()
    S_local_exchange, avg_weighted_completion_time_exchange, makespan_exchange = local_search_exchange(S, m, u)
    time_exchange = time.time() - start_time
    print(f"Розклад:")
    for i, S_j in enumerate(S_local_exchange):
        print(f"М{i + 1}: {S_j}")
    print(f"Середній зважений час проходження робіт F_u: {avg_weighted_completion_time_exchange:.2f}")
    print(f"Максимальний час закінчення робіт F_max: {makespan_exchange}")

    return (time_greedy, time_relocation, time_exchange,
            avg_weighted_completion_time, makespan,
            avg_weighted_completion_time_relocation, makespan_relocation,
            avg_weighted_completion_time_exchange, makespan_exchange)
