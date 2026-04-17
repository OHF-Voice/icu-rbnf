#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unicode/utypes.h>
#include <unicode/rbnf.h>
#include <unicode/locid.h>
#include <unicode/unistr.h>
#include <unicode/ustream.h>

static PyObject* icu_rbnf_error = NULL;

/* Helper to convert ICU UnicodeString to Python string */
static PyObject* unicode_string_to_pystring(const icu::UnicodeString* us) {
    if (!us) {
        Py_RETURN_NONE;
    }

    char* buffer = NULL;
    int32_t len = 0;

    /* Convert to UTF-8 */
    len = us->extract(0, us->length(), NULL, 0, "UTF-8");
    if (len < 0) {
        PyErr_SetString(icu_rbnf_error, "Failed to get string length");
        return NULL;
    }

    buffer = (char*)PyMem_Malloc(len + 1);
    if (!buffer) {
        PyErr_NoMemory();
        return NULL;
    }

    us->extract(0, us->length(), buffer, len + 1, "UTF-8");
    buffer[len] = '\0';

    PyObject* result = PyUnicode_FromString(buffer);
    PyMem_Free(buffer);
    return result;
}

/* Helper to convert Python number to int64_t */
static int parse_number(PyObject* obj, int64_t* result) {
    /* Try int first */
    if (PyLong_Check(obj)) {
        *result = PyLong_AsLongLong(obj);
        return PyErr_Occurred() ? -1 : 0;
    }

    /* Try float */
    if (PyFloat_Check(obj)) {
        double d = PyFloat_AsDouble(obj);
        if (PyErr_Occurred()) {
            return -1;
        }
        *result = (int64_t)d;
        return 0;
    }

    /* Try to convert via float */
    PyObject* float_obj = PyNumber_Float(obj);
    if (float_obj) {
        double d = PyFloat_AsDouble(float_obj);
        Py_DECREF(float_obj);
        if (PyErr_Occurred()) {
            return -1;
        }
        *result = (int64_t)d;
        return 0;
    }

    PyErr_SetString(PyExc_TypeError, "argument must be a number");
    return -1;
}

/* Helper to convert Python number to double */
static int parse_number_double(PyObject* obj, double* result) {
    /* Try to convert via float */
    PyObject* float_obj = PyNumber_Float(obj);
    if (float_obj) {
        *result = PyFloat_AsDouble(float_obj);
        Py_DECREF(float_obj);
        if (PyErr_Occurred()) {
            return -1;
        }
        return 0;
    }

    PyErr_SetString(PyExc_TypeError, "argument must be a number");
    return -1;
}

/* Check if a locale is supported by ICU RBNF */
static PyObject* rbnf_is_locale_supported(PyObject* self, PyObject* args) {
    const char* locale_str;

    if (!PyArg_ParseTuple(args, "s", &locale_str)) {
        return NULL;
    }

    /* ICU is very permissive and falls back to default locale for invalid inputs.
     * We check if the locale string is syntactically valid and if ICU can create
     * a formatter with it. Since ICU always succeeds with fallback, we just verify
     * that the locale string is non-empty and contains valid characters.
     *
     * A locale string should be in the format: language[_SCRIPT][_REGION]
     * where language is 2-3 letter ISO 639 code, SCRIPT is 4 letter ISO 15924 code,
     * and REGION is 2-3 letter ISO 3166 code.
     */

    /* Basic validation: locale string must not be empty */
    if (!locale_str || locale_str[0] == '\0') {
        Py_RETURN_FALSE;
    }

    /* Check for basic validity - should contain only alphanumeric, underscore, hyphen */
    for (const char* p = locale_str; *p; ++p) {
        if (!isalnum((unsigned char)*p) && *p != '_' && *p != '-') {
            Py_RETURN_FALSE;
        }
    }

    /* Try to create a spellout formatter to verify ICU can handle it */
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale locale(locale_str);

    /* Check if the locale is valid by checking its name */
    icu::UnicodeString locale_name = locale.getName();
    if (locale_name.isEmpty()) {
        Py_RETURN_FALSE;
    }

    /* Try to create a formatter */
    icu::RuleBasedNumberFormat* rbnf = nullptr;
    rbnf = new icu::RuleBasedNumberFormat(icu::URBNF_SPELLOUT, locale, status);

    if (U_FAILURE(status) || !rbnf) {
        delete rbnf;
        Py_RETURN_FALSE;
    }

    delete rbnf;
    Py_RETURN_TRUE;
}

/* Spell out a number using ICU RBNF (supports both integers and floats) */
static PyObject* rbnf_spellout(PyObject* self, PyObject* args) {
    PyObject* number_obj;
    const char* locale_str;

    if (!PyArg_ParseTuple(args, "Os", &number_obj, &locale_str)) {
        return NULL;
    }

    /* Get the number as double (supports both int and float) */
    double number;
    if (parse_number_double(number_obj, &number) != 0) {
        return NULL;
    }

    /* Create locale */
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale locale(locale_str);

    /* Create RBNF rules for spellout */
    icu::RuleBasedNumberFormat* rbnf = nullptr;

    /* Use the spellout format (spoken number) */
    rbnf = new icu::RuleBasedNumberFormat(icu::URBNF_SPELLOUT, locale, status);

    if (U_FAILURE(status) || !rbnf) {
        PyErr_SetString(icu_rbnf_error, "Failed to create RBNF formatter");
        delete rbnf;
        return NULL;
    }

    /* Format the number - ICU handles both integers and floats */
    icu::UnicodeString result;
    rbnf->format(number, result);

    delete rbnf;

    return unicode_string_to_pystring(&result);
}

/* Get ordinal form of a number (e.g., "1st", "2nd") */
static PyObject* rbnf_ordinal(PyObject* self, PyObject* args) {
    PyObject* number_obj;
    const char* locale_str;

    if (!PyArg_ParseTuple(args, "Os", &number_obj, &locale_str)) {
        return NULL;
    }

    /* Get the number as int64_t (truncate floats) */
    int64_t number;
    if (parse_number(number_obj, &number) != 0) {
        return NULL;
    }

    /* Create locale */
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale locale(locale_str);

    /* Create RBNF rules for ordinal */
    icu::RuleBasedNumberFormat* rbnf = nullptr;

    /* Use the ordinal format */
    rbnf = new icu::RuleBasedNumberFormat(icu::URBNF_ORDINAL, locale, status);

    if (U_FAILURE(status) || !rbnf) {
        PyErr_SetString(icu_rbnf_error, "Failed to create RBNF formatter");
        delete rbnf;
        return NULL;
    }

    /* Format the number */
    icu::UnicodeString result;
    rbnf->format(number, result);

    delete rbnf;

    return unicode_string_to_pystring(&result);
}

/* Spell out ordinal form of a number (e.g., "first", "twenty-first") */
static PyObject* rbnf_spellout_ordinal(PyObject* self, PyObject* args) {
    PyObject* number_obj;
    const char* locale_str;

    if (!PyArg_ParseTuple(args, "Os", &number_obj, &locale_str)) {
        return NULL;
    }

    /* Get the number as int64_t (truncate floats) */
    int64_t number;
    if (parse_number(number_obj, &number) != 0) {
        return NULL;
    }

    /* Create locale */
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale locale(locale_str);

    /* Create RBNF rules for spellout */
    icu::RuleBasedNumberFormat* rbnf = nullptr;
    rbnf = new icu::RuleBasedNumberFormat(icu::URBNF_SPELLOUT, locale, status);

    if (U_FAILURE(status) || !rbnf) {
        PyErr_SetString(icu_rbnf_error, "Failed to create RBNF formatter");
        delete rbnf;
        return NULL;
    }

    /* Try to use the %spellout-ordinal ruleset if available */
    icu::UnicodeString result;
    bool used_ordinal_ruleset = false;

    /* Check if the ruleset exists by trying to set it */
    icu::UnicodeString ruleset_name("%spellout-ordinal");
    icu::UnicodeString original_default = rbnf->getDefaultRuleSetName();

    status = U_ZERO_ERROR;
    rbnf->setDefaultRuleSet(ruleset_name, status);

    if (U_SUCCESS(status)) {
        /* The ruleset exists and was set - format using it */
        rbnf->format(number, result);
        used_ordinal_ruleset = true;
    }

    /* Fallback to regular ordinal format if %spellout-ordinal not available */
    if (!used_ordinal_ruleset) {
        delete rbnf;
        status = U_ZERO_ERROR;  /* Reset status for new formatter */
        rbnf = new icu::RuleBasedNumberFormat(icu::URBNF_ORDINAL, locale, status);
        if (U_FAILURE(status) || !rbnf) {
            PyErr_SetString(icu_rbnf_error, "Failed to create RBNF formatter");
            delete rbnf;
            return NULL;
        }
        rbnf->format(number, result);
    }

    delete rbnf;

    return unicode_string_to_pystring(&result);
}

/* Module methods */
static PyMethodDef IcuRbnfMethods[] = {
    {"is_locale_supported", rbnf_is_locale_supported, METH_VARARGS, "Check if a locale is supported by ICU RBNF"},
    {"spellout", rbnf_spellout, METH_VARARGS, "Spell out a number in words"},
    {"ordinal", rbnf_ordinal, METH_VARARGS, "Get ordinal form of a number (e.g., '1st', '2nd')"},
    {"spellout_ordinal", rbnf_spellout_ordinal, METH_VARARGS, "Spell out ordinal form of a number (e.g., 'first', 'twenty-first')"},
    {NULL, NULL, 0, NULL}
};

/* Module definition */
static struct PyModuleDef icu_rbnf_module = {
    PyModuleDef_HEAD_INIT,
    "_icu",
    "ICU RBNF extension module",
    -1,
    IcuRbnfMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

/* Module initialization */
PyMODINIT_FUNC PyInit__icu(void) {
    PyObject* m = PyModule_Create(&icu_rbnf_module);
    if (!m) {
        return NULL;
    }

    /* Create exception class */
    icu_rbnf_error = PyErr_NewException("icu_rbnf.error", NULL, NULL);
    if (icu_rbnf_error) {
        PyModule_AddObject(m, "error", icu_rbnf_error);
    }

    return m;
}
