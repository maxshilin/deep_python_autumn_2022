#include <stdlib.h>
#include <stdio.h>

#include <Python.h>

PyObject* matrix_multiplication(PyObject* self, PyObject* args)
{
    PyObject* matrix_1 = NULL;
    PyObject* matrix_2 = NULL;

    if (!PyArg_ParseTuple(args, "OO", &matrix_1, &matrix_2))
    {
        printf("ERROR: Failed to parse argument");
        return NULL;
    }

    if (!PyList_CheckExact(matrix_1)) 
        {
            PyErr_SetString(PyExc_RuntimeError, "Matrix should be a list type.");
            return NULL;
        }
    if (!PyList_CheckExact(matrix_2)) 
        {
            PyErr_SetString(PyExc_RuntimeError, "Matrix should be a list type.");
            return NULL;
        }

    long len1_y = PyList_Size(matrix_1);
    long len2_y = PyList_Size(matrix_2);
    if  ((len1_y == 0) || (len2_y == 0))
    {
        PyErr_SetString(PyExc_RuntimeError, "Matrix should not be a empty.");
        return NULL;
    }

    long len1_x = PyList_Size(PyList_GET_ITEM(matrix_1, 0));

    for (long i = 0; i < len1_y; i++)
    {
        PyObject* row = PyList_GET_ITEM(matrix_1, i);
        if (!PyList_CheckExact(row)) 
        {
            PyErr_SetString(PyExc_RuntimeError, "Non-list type found in list of lists.");
            return NULL;
        }
        if (PyList_Size(row) != len1_x) 
        {
            PyErr_SetString(PyExc_RuntimeError, "Matrix should not be with variable row size.");
            return NULL;
        }
    }

    long len2_x = PyList_Size(PyList_GET_ITEM(matrix_2, 0));

    for (long i = 0; i < len2_y; i++)
    {
        PyObject* row = PyList_GET_ITEM(matrix_2, i);
        if (!PyList_CheckExact(row)) 
        {
            PyErr_SetString(PyExc_RuntimeError, "Non-list type found in list of lists.");
            return NULL;
        }
        if (PyList_Size(row) != len2_x) 
        {
            PyErr_SetString(PyExc_RuntimeError, "Matrix should not be with variable row size.");
            return NULL;
        }
    }

    if (len1_x != len2_y)
    {
        PyErr_SetString(PyExc_RuntimeError, "ERROR: matrices should look like (m, n) and (n, l)");
        return NULL;
    }

    double* out = malloc((len1_y * len2_x) * sizeof(double));
    for (long i = 0; i < len1_y * len2_x; i++)
        out[i] = 0;

    double* mat_1 = malloc((len1_y * len1_x) * sizeof(double));
    for (long i = 0; i < len1_y; i++)
    {
        PyObject *col = PyList_GetItem(matrix_1, i);
        for (long j = 0; j < len1_x; j++)
        {
            mat_1[i * len1_x + j] = PyFloat_AsDouble(PyList_GetItem(col, j));
        }
    }

    double* mat_2 = malloc((len2_y * len2_x) * sizeof(double));
    for (long i = 0; i < len2_y; i++)
    {
        PyObject *col = PyList_GetItem(matrix_2, i);
        for (long j = 0; j < len2_x; j++)
        {
            mat_2[i * len2_x + j] = PyFloat_AsDouble(PyList_GetItem(col, j));
        }
    }

    for (long i = 0; i < len1_y; i++)
    {
        for (long j = 0; j < len1_x; j++) 
        {
            for (long k = 0; k < len2_x; k++)
            {
                out[i * len2_x + k] += mat_1[i * len1_x + j] * mat_2[j * len2_x + k];
            }
        }
    }

    PyObject *out_list = PyList_New(len1_y);
    for (long i = 0; i < len1_y; i++) 
    {
        PyObject *tmp_list = PyList_New(len2_x);
        for (long j = 0; j < len2_x; j++)
            PyList_SetItem(tmp_list, j, PyFloat_FromDouble(out[i * len2_x + j]));
        PyList_SetItem(out_list, i, tmp_list);
    }
 
    free(out);
    free(mat_1);
    free(mat_2);
    return Py_BuildValue("O", out_list);
}

static PyMethodDef methods[] = {
    { "multiply", matrix_multiplication, METH_VARARGS, "Matrix multiplication of two 2D lists"},
    { NULL, NULL, 0, NULL}
};

static struct PyModuleDef multiply = {
    PyModuleDef_HEAD_INIT, "multiply",
    NULL, -1, methods
};

PyMODINIT_FUNC PyInit_multiply() {
    return PyModule_Create(&multiply);
}
