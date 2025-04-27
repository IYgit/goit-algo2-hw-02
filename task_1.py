from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    # Сортуємо завдання за пріоритетом (від найвищого до найнижчого)
    print_jobs = sorted(print_jobs, key=lambda job: job["priority"])

    # Ініціалізуємо список для груп завдань та змінні для підрахунку часу
    groups = []
    current_group = []
    current_group_volume = 0
    current_group_time = 0

    # Проходимо по завданням і групуємо їх
    for job in print_jobs:
        # Якщо додавання цього завдання не перевищує обмеження, додаємо його до групи
        if len(current_group) < constraints["max_items"] and current_group_volume + job["volume"] <= constraints[
            "max_volume"]:
            current_group.append(job)
            current_group_volume += job["volume"]
            current_group_time = max(current_group_time, job["print_time"])  # Обчислюємо час як максимальний для групи
        else:
            # Якщо поточна група заповнена, зберігаємо її і починаємо нову групу
            groups.append(current_group)
            current_group = [job]
            current_group_volume = job["volume"]
            current_group_time = job["print_time"]

    # Додаємо останню групу
    if current_group:
        groups.append(current_group)

    # Рахуємо загальний час друку (сумуємо час для кожної групи)
    total_time = sum(max(job["print_time"] for job in group) for group in groups)

    # Створюємо порядок друку
    print_order = [job["id"] for group in groups for job in group]

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
