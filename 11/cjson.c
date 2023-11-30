#include <Python.h>

const int MAX_KEY_LENGTH = 100;

// Пропуск всех пробелов в строке начиная с индекса i
static int skip_spaces(const char* json_str, int start, int max_len) {
    while (start < max_len &&
           (json_str[start] == ' ' || json_str[start] == '\t' || json_str[start] == '\n' || json_str[start] == '\r')) {
        start++;
    }

    return start;
}

static PyObject* parse_string(const char* json_str, int* start, int max_len) {
    // Проверяем, текущий символ - "
    if (json_str[*start] != '"') {
        PyErr_SetString(PyExc_TypeError, "Invalid string format: must start with '\"'");
        // Py_DECREF(result);
        return NULL;
    }
    *start += 1;

    int end = *start;
    while (json_str[end] != '"' && end < max_len) {
        ++end;
    }
    if (end >= max_len) {
        PyErr_SetString(PyExc_TypeError, "Invalid string format: must end with '\"'");
        // Py_DECREF(result);
        return NULL;
    }

    // Создаем строку-ключ
    PyObject* result = PyUnicode_DecodeUTF8(json_str + *start, end - *start, "strict");
    if (!result) {
        printf("ERROR: Failed to create string\n");
        // Py_DECREF(result);
        return NULL;
    }
    *start = end + 1;
    return result;
}

static PyObject* parse_number(const char* json_str, int* start, int max_len) {
    PyObject* result = NULL;

    int num = 0;
    while (json_str[*start] >= '0' && json_str[*start] <= '9') {
        num = num * 10 + (json_str[*start] - '0');
        *start += 1;
    }
    result = PyLong_FromLong(num);
    return result;
}

static PyObject* cjson_loads(PyObject* self, PyObject* args) {
    const char* json_str;
    // Парсим аргументы
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument type");
        // Py_RETURN_NONE;
        return NULL;
    }

    PyObject* result = NULL;
    if (!(result = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        // Py_RETURN_NONE;
        return NULL;
    }

    int i = 0;
    int max_len = strlen(json_str);
    if (json_str[i] != '{' || json_str[max_len - 1] != '}') {
        PyErr_SetString(PyExc_TypeError, "Invalid JSON format: must start with '{' and end with '}'");
        return NULL;
    }
    // Переходим к следующему символу, пропуская пробелы
    i = skip_spaces(json_str, i + 1, max_len);
    // Обработка пустого словаря
    if (json_str[i] == '}') {
        return result;
    }

    while (i < max_len) {
        i = skip_spaces(json_str, i, max_len);

        // Проверяем, не конец строки
        if (i >= max_len) {
            break;
        }

        // Парсим key
        PyObject* key = parse_string(json_str, &i, max_len);
        if (!key) {
            PyErr_SetString(PyExc_TypeError, "Error parse JSON key: must start with '\"' and end with '\"'");
            return NULL;
        }

        // Пропускаем пробелы
        i = skip_spaces(json_str, i, max_len);

        // Проверяем, следующий символ - ":"
        if (json_str[i] != ':') {
            PyErr_SetString(PyExc_TypeError, "Invalid JSON format: after key should be a ':'");
            return NULL;
        }

        // Пропускаем пробелы со следующего символа
        i = skip_spaces(json_str, i + 1, max_len);

        PyObject* value = NULL;

        // Парсим value
        if (json_str[i] == '"') {
            value = parse_string(json_str, &i, max_len);
        } else if (json_str[i] >= '0' && json_str[i] <= '9') {
            value = parse_number(json_str, &i, max_len);
        } else {
            PyErr_SetString(PyExc_TypeError, "Error parse JSON value");
            return NULL;
        }

        if (!value) {
            PyErr_SetString(PyExc_TypeError, "Error parse JSON value");
            return NULL;
        }

        // Добавляем в словарь
        PyDict_SetItem(result, key, value);

        // Пропускаем пробелы
        i = skip_spaces(json_str, i, max_len);
        // Проверяем, следующий символ - ","
        if (json_str[i] == ',') {
            i = skip_spaces(json_str, i + 1, max_len);
            if (json_str[i] != '\"') {
                PyErr_SetString(PyExc_TypeError, "Error parse JSON key: must start with '\"' and end with '\"'");
                return NULL;
            }
        } else if (json_str[i] == '}') {
            if (i != max_len - 1) {
                PyErr_SetString(PyExc_TypeError, "Invalid JSON format: got '}' at not end of json string");
                return NULL;
            }
            // Завершаем цикл, если следующий символ - "}"
            break;
        } else {
            PyErr_SetString(PyExc_TypeError, "Invalid JSON format: expected ',' or '}'");
            return NULL;
        }
    }

    return result;
}

static PyObject* cjson_dumps(PyObject* self, PyObject* args) {
    PyObject* obj;

    // Парсим аргументы
    if (!PyArg_ParseTuple(args, "O", &obj)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument type");
        return NULL;
    }

    if (!PyDict_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected dictionary");
        return NULL;
    }

    PyObject* key;
    PyObject* value;
    Py_ssize_t pos = 0;
    PyObject* result = PyUnicode_DecodeUTF8("{", 1, "strict");

    while (PyDict_Next(obj, &pos, &key, &value)) {
        // Формируем ключ
        PyObject* key_str;
        if (PyUnicode_Check(key)) {
            key_str = PyUnicode_FromFormat("\"%S\"", key);
        } else {
            PyErr_SetString(PyExc_TypeError, "Invalid key type");
            return NULL;
        }

        if (!key_str) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to convert key to string");
            return NULL;
        }

        // printf("Debug: Key: %s\n", PyUnicode_AsUTF8(key_str));

        // Формируем значение
        PyObject* value_str;
        if (PyLong_Check(value)) {
            value_str = PyObject_Str(value);
        } else if (PyUnicode_Check(value)) {
            value_str = PyUnicode_FromFormat("\"%S\"", value);
        } else {
            PyErr_SetString(PyExc_TypeError, "Invalid value type");
            return NULL;
        }

        if (!value_str) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to convert value to string");
            return NULL;
        }

        // Добавляем ключ и значение к результату
        // printf("Debug: result: %s\n", PyUnicode_AsUTF8(result));
        PyObject* result_tmp = PyUnicode_Concat(result, key_str);
        Py_XDECREF(result);
        Py_XDECREF(key_str);
        result = result_tmp;
        if (!result) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate key to result");
            return NULL;
        }

        // printf("Debug: result: %s\n", PyUnicode_AsUTF8(result));
        result_tmp = PyUnicode_Concat(result, PyUnicode_DecodeUTF8(": ", 2, "strict"));
        Py_XDECREF(result);
        result = result_tmp;
        if (!result) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate ': ' to result");
            return NULL;
        }

        // printf("Debug: result: %s\n", PyUnicode_AsUTF8(result));
        result_tmp = PyUnicode_Concat(result, value_str);
        result = result_tmp;
        if (!result) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate value to result");
            return NULL;
        }

        // printf("Debug: result: %s\n", PyUnicode_AsUTF8(result));

        // Добавляем запятую между парами ключ-значение
        result_tmp = PyUnicode_Concat(result, PyUnicode_DecodeUTF8(", ", 2, "strict"));
        Py_XDECREF(result);
        result = result_tmp;
        if (!result) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate ', ' to result");
            return NULL;
        }
    }

    // Удаляем последнюю запятую с пробелом
    // printf("Debug: end result: %s\n", PyUnicode_AsUTF8(result));
    Py_ssize_t len = PyUnicode_GetLength(result);
    // PyUnicode_SetLength(result, len - 1);
    PyObject* result_tmp = PyUnicode_Substring(result, 0, len - 2);

    // Добавляем закрывающую фигурную скобку
    result = PyUnicode_Concat(result_tmp, PyUnicode_DecodeUTF8("}", 1, "strict"));
    if (!result) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate ',' to result");
        return NULL;
    }

    return result;
}

static PyMethodDef methods[] = {{"loads", cjson_loads, METH_VARARGS, "parse json file from string"},
                                {"dumps", cjson_dumps, METH_VARARGS, "serialize dictionary to json string"},
                                {NULL, NULL, 0, NULL}};

static struct PyModuleDef cjson_module = {PyModuleDef_HEAD_INIT, "cjson", NULL, -1, methods};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson_module);
}