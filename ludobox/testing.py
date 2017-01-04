#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Used to launch autotests of the program
import doctest
import pytest

# unexported constasts used as pytest.main return codes
# c.f. https://github.com/pytest-dev/pytest/blob/master/_pytest/main.py
PYTEST_EXIT_OK = 0
PYTEST_EXIT_TESTSFAILED = 1
PYTEST_EXIT_INTERRUPTED = 2
PYTEST_EXIT_INTERNALERROR = 3
PYTEST_EXIT_USAGEERROR = 4
PYTEST_EXIT_NOTESTSCOLLECTED = 5

def autotest(**kwargs):
    """
    Execute all the test to check if the program works correctly.

    The tests are:
    *   test from the documentation of the code itself (via :mod:`doctest`
        module). They basically check if the usage of the function has not
        changed. This is the equivalent of doing :command:`python -m doctest -v
        ludocore.py`.
    *   unittest from the `tests` directory. Those test are here to check that
        every function works as expected and that all functionnalities are ok
        even in corner cases. They use :mod:`pytest` module.
    *   functionnal tests that try to replicate actuel usecases. They are
        located in `functional_test.py`. They use :mod:`pytest` module. This is
        the equivalent of doing :command:`py.test --quiet --tb=line
        functional_test.py`

    kwargs is used here since this function is called by :func:`main` via
    :mod:`argparse`. And all the params are provided automagically by
    :func:`argparse.ArgumentParser.parse_args` converted to a dict using
    :func:`vars`.
    See `Namespace object<https://docs.python.org/2/library/argparse.html#the-namespace-object>`_
    """
    # Doctests
    print("DOCTESTS".center(80, '#'))
    print("Tests examples from the documentation".center(80, '-'))
    nb_fails, nb_tests = doctest.testmod(verbose=False)
    nb_oks = nb_tests - nb_fails
    print(nb_oks, "/", nb_tests, "tests are OK.")
    if nb_fails > 0:
        print("FAIL")
        print("     To have more details about the errors you should try "
              "the command: python -m doctest -v ludocore.py")
    else:
        print("SUCCESS")

    # Unit tests
    print("UNIT TESTS".center(80, '#'))
    print("Tests every functionnality in deep".center(80, '-'))
    unit_result = pytest.main([
        "--quiet",
        "--color=no",
        "--tb=line",
        "tests"])
    if unit_result not in (PYTEST_EXIT_OK, PYTEST_EXIT_NOTESTSCOLLECTED):
        print("FAIL")
        print("     To have more details about the errors you should try "
              "the command: py.test tests")
    else:
        print("SUCCESS")

    # Functional tests
    print("FUNCTIONAL TESTS".center(80, '#'))
    print("Tests actual real life usage and data".center(80, '-'))
    func_result = pytest.main([
        "--quiet",
        "--color=no",
        "--tb=line",
        "tests/functional_tests.py"])
    if func_result not in (PYTEST_EXIT_OK, PYTEST_EXIT_NOTESTSCOLLECTED):
        print("FAIL")
        print("     To have more details about the errors you should try "
              "the command: py.test tests/functional_tests.py")
    else:
        print("SUCCESS")
