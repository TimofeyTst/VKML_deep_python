import time
import weakref
from memory_profiler import profile


class CarName:
    def __init__(self, name):
        self.name = name


class CarYear:
    def __init__(self, year):
        self.year = year


class TeslaModel:
    def __init__(self, name, year):
        self.name = CarName(name)
        self.year = CarYear(year)


class TeslaModelSlots:
    __slots__ = ("name", "year")

    def __init__(self, name, year):
        self.name = CarName(name)
        self.year = CarYear(year)


class TeslaModelWeakRef:
    def __init__(self, name, year):
        self.name = weakref.ref(CarName(name))
        self.year = weakref.ref(CarYear(year))


@profile
def creation_time(class_type, num_instances):
    start_time = time.time()
    instances = [class_type(f"Model{i}", 2023) for i in range(num_instances)]
    creation_time = time.time() - start_time

    return instances, creation_time


# @profile
def access_time(class_type, instances, num_accesses):
    start_time = time.time()
    for _ in range(num_accesses):
        for instance in instances:
            _ = instance.name
            _ = instance.year
    access_time = time.time() - start_time

    return access_time


num_instances = 100000
num_accesses = 1000

# creation time
instances_regular, creation_time_regular = creation_time(TeslaModel, num_instances)
instances_slots, creation_time_slots = creation_time(TeslaModelSlots, num_instances)
instances_weakref, creation_time_weakref = creation_time(
    TeslaModelWeakRef, num_instances
)

# access time
access_time_regular = access_time(TeslaModel, instances_regular, num_accesses)
access_time_slots = access_time(TeslaModelSlots, instances_slots, num_accesses)
access_time_weakref = access_time(TeslaModelWeakRef, instances_weakref, num_accesses)

# Отсортируем по времени доступа
class_types = [
    ("Regular", creation_time_regular, access_time_regular),
    ("Slots", creation_time_slots, access_time_slots),
    ("WeakRef", creation_time_weakref, access_time_weakref),
]

sorted_by_creation_time = sorted(class_types, key=lambda x: x[1])
sorted_by_access_time = sorted(class_types, key=lambda x: x[2])

print("\n=========== Время создания (Total) ===========")
print(f"Обычного класса: {creation_time_regular:.5f} секунд")
print(f"Класса со слотами: {creation_time_slots:.5f} секунд")
print(f"Класса с weakref: {creation_time_weakref:.5f} секунд")

print("\n=========== Время доступа (Total/Mean) ===========")
print(
    f"К аттрибутам обычного класса: {access_time_regular:.3f} \
    / {access_time_regular/num_accesses:.3f} секунд"
)
print(
    f"К аттрибутам класса со слотами: {access_time_slots:.3f} \
    / {access_time_slots/num_accesses:.3f} секунд"
)
print(
    f"К аттрибутам класса с weakref: {access_time_weakref:.3f} \
    / {access_time_weakref/num_accesses:.3f} секунд"
)


print("\nSorted Create -> ", end=" | ")
for class_type, creation_time, _ in sorted_by_creation_time:
    print(f"{class_type}: {creation_time:.3f}с", end=" | ")
print("\nSorted Access -> ", end=" | ")
for class_type, _, access_time in sorted_by_access_time:
    print(f"{class_type}: {access_time:.3f}с", end=" | ")
print("\n")
