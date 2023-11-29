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
        PyErr_SetString(PyExc_TypeError, "Invalid string format");
        // Py_DECREF(result);
        return NULL;
    }
    *start += 1;

    int end = *start;
    while (json_str[end] != '"' && end < max_len) {
        ++end;
    }
    if (end >= max_len) {
        PyErr_SetString(PyExc_TypeError, "Invalid string format");
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

    if (json_str[i] != '{' && json_str[max_len] != '}') {
        PyErr_SetString(PyExc_TypeError, "Invalid JSON format1");
        return NULL;
    }
    ++i;

    while (i < max_len) {
        i = skip_spaces(json_str, i, max_len);

        // Проверяем, не конец строки
        if (i >= max_len) {
            break;
        }

        // Парсим key
        PyObject* key = parse_string(json_str, &i, max_len);
        if (!key) {
            PyErr_SetString(PyExc_TypeError, "Error parse JSON key");
            return NULL;
        }

        // Пропускаем пробелы
        i = skip_spaces(json_str, i, max_len);

        // Проверяем, следующий символ - ":"
        if (json_str[i] != ':') {
            PyErr_SetString(PyExc_TypeError, "Invalid JSON format2");
            return NULL;
        }

        // Пропускаем пробелы
        i = skip_spaces(json_str, i + 1, max_len);

        PyObject* value = NULL;

        // Парсим value
        if (json_str[i] == '"') {
            value = parse_string(json_str, &i, max_len);
        } else {
            value = parse_number(json_str, &i, max_len);
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
            ++i;
            i = skip_spaces(json_str, i, max_len);
            if (json_str[i] != '"') {
                PyErr_SetString(PyExc_TypeError, "Invalid key format");
                return NULL;
            }
        } else if (json_str[i] == '}') {
            // Завершаем цикл, если следующий символ - "}"
            break;
        } else {
            PyErr_SetString(PyExc_TypeError, "Invalid JSON format3");
            return NULL;
        }
    }

    return result;
}

static PyMethodDef methods[] = {
    // {"load", cjson_load, METH_NOARGS, "parse json file from string"},
    {"loads", cjson_loads, METH_VARARGS, "parse json file from string"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cjson_module = {PyModuleDef_HEAD_INIT, "cjson", NULL, -1, methods};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson_module);
}