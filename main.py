from algorithms import (solve_problem, generate_data,
                        save_data, load_data, edit_data)

if __name__ == '__main__':
    mode = input("1 - введення даних вручну\n"
                 "2 - генерація даних випадковим чином\n"
                 "3 - читання з файлу\n"
                 "4 - редагування даних файлу\n"
                 "Оберіть дію: ")
    try:
        mode = int(mode)
    except ValueError:
        mode = -1

    if mode == 1:
        solve_problem()

    elif mode == 2:
        m_input = int(input("\nВведіть кількість машин: "))
        n_input = int(input("Введіть кількість робіт: "))
        for i in range(1):
            m, n, u, p = generate_data(m_input, n_input, 100, 250, 10, 20)
            print(f"\nЗгенеровані дані:\n{m=}, {n=}\n{u=}\n{p=}")
            save_data("data/generated_data.json", m, n, u, p)
            solve_problem(filename="data/generated_data.json")

    elif mode == 3:
        m, n, u, p = load_data('data/individual_task_data.json')
        print(f"\nДані з файлу:\n{m=}, {n=}\n{u=}\n{p=}")
        solve_problem(filename='data/individual_task_data.json')

    elif mode == 4:
        edit_data('data/individual_task_data.json')
        m, n, u, p = load_data('data/individual_task_data.json')
        print(f"\nДані з файлу:\n{m=}, {n=}\n{u=}\n{p=}")
        solve_problem(filename='data/individual_task_data.json')

    else:
        print("Обраної дії не існує")
