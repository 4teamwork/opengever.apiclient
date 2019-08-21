from . import TestSuite


def pytest_configure(config):
    TestSuite.setUp()


def pytest_unconfigure(config):
    TestSuite.tearDown()
