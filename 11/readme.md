# Домашнее задание #11 (Расширения на C)

### Запуск тестов
```bash
make
make coverage
```

Или просто ```make test```

### Написать тест производительности
Сравнивать скорость работы своей реализации с json и ujson на одних и тех же данных. Данные должны быть большие (как количество JSON, так и размер каждого JSON). Требование: выполнение тестов не менее 100 мс.

#### Запустить тестирование скорости можно командой ниже
```bash
make main
```
Предварительно следует прогнать команду ```make```

### Результаты
### 1000 итераций по 1000 объектов в каждой
#### ===== Test dump method =====
Total/Mean in seconds

json  duration: 0.046172 / 2.3086e-07

ujson duration: 0.023932 / 1.1966e-07

cjson duration: 1.1154 / 5.577e-06

Performance test passed successfully total time: 18.587s.

#### ===== Test load method =====
Total/Mean in seconds

json  duration: 0.034571 / 1.7285e-07

ujson duration: 0.028099 / 1.405e-07

cjson duration: 0.023366 / 1.1683e-07

Performance test passed successfully total time: 17.097s.

### 10 итераций по 10000 объектов в каждой
#### ===== Test dump method =====
Total/Mean in seconds

json  duration: 0.052448 / 2.6224e-07

ujson duration: 0.026488 / 1.3244e-07

cjson duration: 1.2396 / 6.1979e-06

Performance test passed successfully total time: 20.722s.

#### ===== Test load method =====
Total/Mean in seconds

json  duration: 0.037848 / 1.8924e-07

ujson duration: 0.030665 / 1.5333e-07

cjson duration: 0.024768 / 1.2384e-07

Performance test passed successfully total time: 18.363s.

### 100 итераций по 10000 объектов в каждой
#### ===== Test dump method =====
Total/Mean in seconds

json  duration: 0.051022 / 2.5511e-07

ujson duration: 0.025191 / 1.2595e-07

cjson duration: 1.2493 / 6.2466e-06

Performance test passed successfully total time: 20.021s.

#### ===== Test load method =====
Total/Mean in seconds

json  duration: 0.039706 / 1.9853e-07

ujson duration: 0.031609 / 1.5804e-07

cjson duration: 0.025676 / 1.2838e-07

Performance test passed successfully total time: 19.017s.

### 100 итераций по 15000 объектов в каждой
#### ===== Test dump method =====
Total/Mean in seconds

json  duration: 0.045179 / 2.2589e-07

ujson duration: 0.023972 / 1.1986e-07

cjson duration: 1.1053 / 5.5263e-06

Performance test passed successfully total time: 18.475s.

#### ===== Test load method =====
Total/Mean in seconds

json  duration: 0.036127 / 1.8063e-07

ujson duration: 0.029176 / 1.4588e-07

cjson duration: 0.023837 / 1.1919e-07

Performance test passed successfully total time: 17.54s.

#### Получилось повысить скорость на методе load, но метод dump показывает сильно хуже результат. Очевидно, что нужно углубиться в работу с памятью, и оптимизировать сам алгоритм, убрать по возможности методы Py.., чтобы повысить скорость на чистом C, но я итак знатно помучился писать код на C, если понадобиться выкатить это в прод - я займусь оптимизацией, а пока дел слишком много. 

### Код был прогнан линтерами black & ruff & clang_format
