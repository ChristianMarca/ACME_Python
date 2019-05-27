import pytest
import os
# from _pytest.fixtures import SubRequest
from src.calculate import EmployeePayment
from src.utils import Utils
from src.payment import PaymentUtils
from src.time_utils import TimeUtils
from src.constants import CONSTRAINS


@pytest.fixture
def employee_payment():
    prepare_employee_payment = EmployeePayment("test_employee_data.txt")
    return prepare_employee_payment


@pytest.fixture
def utils():
    prepare_utils = Utils()
    return prepare_utils


@pytest.fixture
def utils_payment():
    prepare_payment_utils = PaymentUtils()
    return prepare_payment_utils


@pytest.fixture
def utils_time():
    prepare_time_utils = TimeUtils()
    return prepare_time_utils


def check_not_found_file(utils, file):
    _file = os.path.join(os.path.dirname(os.path.basename(os.getcwd())), "files", file)
    return utils.get_info_from_file(_file)


# File not Found
@pytest.mark.parametrize("file", [("employees_data1.txt")])
def test_read_file_fail(utils, file):
    with pytest.raises(Exception, message="Archivo Invalido") as e:
        check_not_found_file(utils, file)


# File Found with correct data
@pytest.mark.parametrize(
    "file,expected",
     [("employees_data.txt",
       ['RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00',
         'ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00', 'JHON=MO08:00-15:00,TH12:00-23:00,SU20:00-21:00',
         'ESTHER=MO08:03-10:30,TU06:00-09:00,WE09:30-17:30,FR09:30-18:00',
         'ELVIS=MO07:00-09:00,WE02:35-08:30,FR02:30-09:30,SA09:30-17:30,SU18:30-23:30',
         'JHOANA=FR21:30-23:00,SA09:30-17:30,SU09:30-17:30']
        )
      ]
)
def test_read_file(utils, file, expected):
    _file = os.path.join(os.path.dirname(os.path.basename(os.getcwd())), "files", file)
    print(_file)
    data_received = utils.get_info_from_file(_file)
    assert all([a == b for a, b in zip(data_received, expected)])

# Calculate the time between two hours of the day
@pytest.mark.parametrize("start_hour,end_hour,expected", [(['08', '30'], ['10', '00'], 1.5)])
def test_calculate_time_with_valid_data(utils_time, start_hour, end_hour, expected):
    assert utils_time.calculate_time(start_hour, end_hour) == expected

# Calculate the time between two hours of the day in two turns
@pytest.mark.parametrize("start_hour, end_hour, expected", [(['00', '12'], ['23', '37'], 23.42)])
def test_calculate_time_with_valid_data_two_turns(utils_time, start_hour, end_hour, expected):
    assert utils_time.calculate_time(start_hour, end_hour) == expected

# Calculate time with two invalid hours
@pytest.mark.parametrize("start_hour, end_hour, expected", [(['08', '30'], ['10', '60'], 0)])
def test_calculate_time_with_invalid_data(utils_time, start_hour, end_hour, expected):
    assert utils_time.calculate_time(start_hour, end_hour) == expected

# Calculate the time with two disordered hours
@pytest.mark.parametrize("start_hour, end_hour, expected", [([9, 30], ['08', '00'], 0)])
def test_calculate_time_with_valid_disordered_data(utils_time, start_hour, end_hour, expected):
    assert utils_time.calculate_time(start_hour, end_hour) == expected


# Verify hour with restrictions of upper and lower limit

# Lower limit with valid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [9, 30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            True)])
def test_is_at_lower_limit(utils_time, time, constrains, expected):
    start_hour_shift = constrains[1]["start"]
    assert utils_time.verify_hour_lower(time, start_hour_shift) == expected


# Lower limit with invalid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [8, 30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            False)])
def test_is_at_invalid_lower_limit(utils_time, time, constrains, expected):
    start_hour_shift = constrains[1]["start"]
    assert utils_time.verify_hour_lower(time, start_hour_shift) == expected


# Upper limit with valid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [8, 30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            True)])
def test_is_at_upper_limit(utils_time, time, constrains, expected):
    end_hour_shift = constrains[0]["end"]
    assert utils_time.verify_hour_upper(time, end_hour_shift) == expected


# Upper limit with invalid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [9, 30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            False)])
def test_is_at_invalid_upper_limit(utils_time, time, constrains, expected):
    end_hour_shift = constrains[0]["end"]
    assert utils_time.verify_hour_upper(time, end_hour_shift) == expected


# Calculate the value to pay per day

# Calculate value to pay per day with valid hour two
@pytest.mark.parametrize("start_hour, end_hour, constrains, expected",
                         [(
                            [10, 30],
                            [15, 30],
                            CONSTRAINS["TIME_WEEKEND"],
                            100),
                            (
                            [19, 30],
                            [8, 30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            0
                             )])
def test_payment_per_day(utils_payment, start_hour, end_hour, constrains, expected):
    assert utils_payment._PaymentUtils__payment_per_day(start_hour, end_hour, constrains) == expected


# Calculate value to pay per day with work hours between two constraints
@pytest.mark.parametrize("start_hour, end_hour, constrains, expected",
                         [(
                            [10, 30],
                            [15, 30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            75)])
def test_payment_two_constrains(utils_payment, start_hour, end_hour, constrains, expected):
    assert utils_payment._PaymentUtils__payment_per_day(start_hour, end_hour, constrains) == expected


# Calculate value to pay per day with invalid hour
@pytest.mark.parametrize("start_hour, end_hour, constrains, expected",
                         [(
                            [10, 30],
                            [15, 65],
                            CONSTRAINS["TIME_WEEKDAY"],
                            0)])
def test_payment_invalid_hour(utils_payment, start_hour, end_hour, constrains, expected):
    assert utils_payment._PaymentUtils__payment_per_day(start_hour, end_hour, constrains) == expected


# Calculate the value to pay per day with disordered hours
@pytest.mark.parametrize("start_hour, end_hour, constrains, expected",
                         [(
                            [10, 30],
                            [9, 35],
                            CONSTRAINS["TIME_WEEKEND"],
                            0)])
def test_payment_disordered_hours(utils_payment, start_hour, end_hour, constrains, expected):
    assert utils_payment._PaymentUtils__payment_per_day(start_hour, end_hour, constrains) == expected


# Calculate the value to pay per employee

# Calculate total value to paid with valid data
@pytest.mark.parametrize("employee_info ,employee_data, expected",
                         [('TestName',
                            ['MO', '10', '00', '12', '00', 'TH', '12', '00', '14', '00', 'SU', '20', '00', '21', '00'],
                           f'The amount to pay TestName is: {85.0} USD'
                         ),
                          ('TestName',
                           ['MO', '10', '00', '12', '00', 'TH', '12', '00', '14', '00', 'SU', '20', '00', '21', '60'],
                           f'The amount to pay TestName is: {60.0} USD'
                           )
                          ])
def test_calculate_amount_to_pay(utils_payment, employee_info, employee_data, expected):
    assert utils_payment._PaymentUtils__calculate_amount_to_pay(employee_info, employee_data) == expected


# Calculate the total value to pay
# Calculate the total value to pay with valid data
@pytest.mark.parametrize("expected",
                         [
                            ([['The amount to pay RENE is: 215.0 USD'], ['The amount to pay ASTRID is: 85.0 USD'],['The amount to pay JHON is: 329.3 USD']])
                         ])
def test_calculate_payment(employee_payment, expected):
    assert employee_payment.calculate() == expected


def calculate_employee_payment(file):
    employee_payment_1 = EmployeePayment(file)
    return employee_payment_1.calculate()


# Calculate the total value to pay with a nonexistent file
@pytest.mark.parametrize("file", [("employees_data1.txt")])
def test_calculate_payment_fail(file):
    with pytest.raises(Exception, message="Archivo Invalido") as e:
        calculate_employee_payment(file)
