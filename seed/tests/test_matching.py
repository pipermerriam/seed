from django.test import TestCase
from seed.tasks import _normalize_address_str


def make_method(message, expected):
    def run(self):
        result = _normalize_address_str(message)
        self.assertEquals(expected, result)
    return run


# Metaclass to create individual test methods per test case.
class NormalizeAddressTester(type):
    def __new__(cls, name, bases, attrs):
        cases = attrs.get('cases', [])

        for doc, message, expected in cases:
            test = make_method(message, expected)
            test_name = 'test_normalize_address_%s' % doc.lower().replace(' ', '_')
            test.__name__ = test_name
            test.__doc__ = doc
            attrs[test_name] = test
        return super(NormalizeAddressTester, cls).__new__(cls, name, bases, attrs)


class NormalizeStreetAddressTests(TestCase):
    __metaclass__ = NormalizeAddressTester

    # test name, input, expected output
    cases = [
        ('simple', '123 Test St.', '123 test st'),
        ('none input', None, None),
        ('empty input', '', None),
        ('missing number', 'Test St.', 'test st'),
        ('missing street', '123', '123'),
        ('integer address', 123, '123'),
        ('strip leading zeros', '0000123', '123'),
        ('street 1', 'STREET', 'st'),
        ('street 2', 'Street', 'st'),
        ('boulevard', 'Boulevard', 'blvd'),
        ('avenue', 'avenue', 'ave'),
        ('trailing direction', '123 Test St. NE', '123 test st ne'),
        ('prefix direction', '123 South Test St.', '123 s test st'),
        ('verbose direction', '123 Test St. Northeast', '123 test st ne'),
        ('two directions', '111 S West Main', '111 s west main'),
        ('numeric street and direction', '555 11th St. NW', '555 11th st nw'),
        ('direction 1', '100 Main S', '100 main s'),
        ('direction 2', '100 Main South', '100 main s'),
        ('direction 3', '100 Main S.', '100 main s'),
        ('direction 4', '100 Main', '100 main'),
    ]
