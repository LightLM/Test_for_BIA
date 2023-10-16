from django.http import JsonResponse
import random
from datetime import date, time
from django.db.models import Q
from .models import Employee, Shift


def choice_worker(workers):
    # Выбор работника с часами
    choice = random.choice(workers)
    if random.choice(workers).hours != 0:
        return choice
    else:
        return choice_worker(workers)


def generate_schedule(request, year, month):
    # Получаем число дней в указанном месяце
    days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month in [4, 6, 9, 11] else 28
    # Удаляем данные о месяце который пересоздаем
    Shift.objects.filter(
        Q(date__year=year, date__month=month)
    ).delete()
    # Создаем 10 сотрудников, если их еще нет в базе данных и обновляем часы, если есть
    if not Employee.objects.exists():
        for i in range(1, 11):
            employee = Employee(name=f'worker{i}', hours=144)
            employee.save()
    else:
        Employee.objects.all().update(hours=144)

    # Получаем список сотрудников
    employees = Employee.objects.all()
    # Генерируем график смен
    schedule = {}
    for day in range(1, days_in_month + 1):
        date_obj = date(year, month, day)
        if date_obj.weekday() == 0:  # Понедельник
            employees_needed = 4
        elif date_obj.weekday() == 6:  # Воскресенье
            employees_needed = 2
        else:
            employees_needed = 3
        #Дата конкретного дня год/месяц/день/день недели
        date_for_d = f'{str(year)}_{str(month)}_{str(day)}_{str(date_obj.weekday())}'
        schedule[date_for_d] = []
        for i in range(employees_needed):  # Кол-во людей нужных в этот день
            # Выбираем случайного сотрудника для смены
            employee = choice_worker(employees)
            # Меняем его часы
            employee.hours -= 12
            employee.save()

            # Создаем запись о смене
            shift_start = time(8, 0) if i != employees_needed - 1 else time(10, 0)
            shift_end = time(20, 0) if i != employees_needed - 1 else time(22, 0)
            shift = Shift(date=date_obj, employee=employee, start_time=shift_start, end_time=shift_end)
            shift.save()
            schedule[date_for_d].append(
                f"{date_obj}: {employee.name}, {shift_start} - {shift_end}")

    return JsonResponse({'schedule': schedule})
