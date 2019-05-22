import pytest
import os
# from _pytest.fixtures import SubRequest
from src.calculate import EmployeePayment
from src.utils import Utils
from src.payment import PaymentUtils
from src.time_utils import TimeUtils
from src.constants import CONSTRAINS


@pytest.fixture
def employeePayment():
    prepare_employeePayment = EmployeePayment("test_employee_data.txt")
    return prepare_employeePayment

@pytest.fixture
def utils():
    prepare_utils = Utils()
    return prepare_utils

@pytest.fixture
def utilsPayment():
    prepare_paymentUtils = PaymentUtils()
    return prepare_paymentUtils


@pytest.fixture
def utilsTime():
    prepare_timeUtils = TimeUtils()
    return prepare_timeUtils


def checkNotFoundFile(utils, file):
    _file= os.path.join(os.path.dirname(os.path.basename(os.getcwd())), "files", file)
    return utils.getInfoFromFile(_file)


# File not Found
@pytest.mark.parametrize("file",[("employees_data1.txt")])
def test_readFile_fail(utils,file):
    with pytest.raises(FileNotFoundError):
       checkNotFoundFile(utils, file)


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
def test_readFile(utils,file, expected):
    _file = os.path.join(os.path.dirname(os.path.basename(os.getcwd())), "files", file)
    data_received = utils.getInfoFromFile(_file)
    assert all([a == b for a, b in zip(data_received, expected)])

# Calculate the time between two hours of the day
@pytest.mark.parametrize("startHour,endHour,expected", [(['08', '30'], ['10', '00'], 1.5)])
def test_calculateTimeWithValidData(utilsTime,startHour, endHour, expected):
    assert utilsTime.calculateTime(startHour, endHour) == expected

# Calculate the time between two hours of the day in two turns
@pytest.mark.parametrize("startHour, endHour, expected", [(['00', '12'], ['23', '37'], 23.42)])
def test_calculateTimeWithValidaDataTwoTurns(utilsTime,startHour, endHour, expected):
    assert utilsTime.calculateTime(startHour, endHour) == expected

# Calculate time with two invalid hours
@pytest.mark.parametrize("startHour, endHour, expected", [(['08', '30'], ['10', '60'], 0)])
def test_calculateTimeWithInvalidaData(utilsTime,startHour, endHour, expected):
    assert utilsTime.calculateTime(startHour, endHour) == expected

# Calculate the time with two disordered hours
@pytest.mark.parametrize("startHour, endHour, expected", [([9,30], ['08', '00'], 0)])
def test_calculateTimeWithValidaData(utilsTime, startHour, endHour, expected):
    assert utilsTime.calculateTime(startHour, endHour) == expected

# Verify hour with restrictions of upper and lower limit

# Lower limit with valid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [9,30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            True)])
def test_isAtLowerLimit(utilsTime, time, constrains, expected):
    startHourShift = constrains[1]["start"]
    assert utilsTime.verifyHourLower(time, startHourShift) == expected

# Lower limit with invalid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [8,30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            False)])
def test_isAtInvalidLowerLimit(utilsTime, time, constrains, expected):
    startHourShift = constrains[1]["start"]
    assert utilsTime.verifyHourLower(time, startHourShift) == expected


# Upper limit with valid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [8,30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            True)])
def test_isAtUpperLimit(utilsTime, time, constrains, expected):
    endHourShift = constrains[0]["end"]
    assert utilsTime.verifyHourUpper(time, endHourShift) == expected


# Upper limit with invalid hour
@pytest.mark.parametrize("time, constrains, expected",
                         [(
                            [9,30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            False)])
def test_isAtInvelidUpperLimit(utilsTime, time, constrains, expected):
    endHourShift = constrains[0]["end"]
    assert utilsTime.verifyHourUpper(time, endHourShift) == expected


# Calculate the value to pay per day

# Calculate value to pay per day with valid hour
@pytest.mark.parametrize("startHour, endHour, constrains, expected",
                         [(
                            [10,30],
                            [15,30],
                            CONSTRAINS["TIME_WEEKEND"],
                            100)])
def test_paymentPerDay(utilsPayment, startHour, endHour, constrains, expected):
    assert utilsPayment._PaymentUtils__paymentPerDay(startHour, endHour, constrains) == expected

# Calculate value to pay per day with valid hour two
@pytest.mark.parametrize("startHour, endHour, constrains, expected",
                         [(
                            [10,30],
                            [15,30],
                            CONSTRAINS["TIME_WEEKEND"],
                            100),
                            (
                            [19,30],
                            [8,30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            0
                             )])
def test_paymentPerDay(utilsPayment, startHour, endHour, constrains, expected):
    assert utilsPayment._PaymentUtils__paymentPerDay(startHour, endHour, constrains) == expected


# Calculate value to pay per day with work hours between two constraints
@pytest.mark.parametrize("startHour, endHour, constrains, expected",
                         [(
                            [10,30],
                            [15,30],
                            CONSTRAINS["TIME_WEEKDAY"],
                            75)])
def test_paymentTwoConstrains(utilsPayment, startHour, endHour, constrains, expected):
    assert utilsPayment._PaymentUtils__paymentPerDay(startHour, endHour, constrains) == expected


# Calculate value to pay per day with invalid hour
@pytest.mark.parametrize("startHour, endHour, constrains, expected",
                         [(
                            [10,30],
                            [15,65],
                            CONSTRAINS["TIME_WEEKDAY"],
                            0)])
def test_paymentInvalidHour(utilsPayment, startHour, endHour, constrains, expected):
    assert utilsPayment._PaymentUtils__paymentPerDay(startHour, endHour, constrains) == expected

# Calculate the value to pay per day with disordered hours
@pytest.mark.parametrize("startHour, endHour, constrains, expected",
                         [(
                            [10,30],
                            [9,35],
                            CONSTRAINS["TIME_WEEKEND"],
                            0)])
def test_paymentDisrderedHours(utilsPayment, startHour, endHour, constrains, expected):
    assert utilsPayment._PaymentUtils__paymentPerDay(startHour, endHour, constrains) == expected


# Calculate the value to pay per employee

# Calculate total value to paid with valid data
@pytest.mark.parametrize("employeeInfo ,employeeData, expected",
                         [('TestName',
                            ['MO','10','00','12','00','TH','12','00','14','00','SU','20','00','21','00'],
                           f'The amount to pay TestName is: {85.0} USD'
                         ),
                          ('TestName',
                           ['MO', '10', '00', '12', '00', 'TH', '12', '00', '14', '00', 'SU', '20', '00', '21', '60'],
                           f'The amount to pay TestName is: {60.0} USD'
                           )
                          ])
def test_calculateAmounToPay(utilsPayment,employeeInfo, employeeData, expected):
    assert utilsPayment._PaymentUtils__calculateAmountToPay(employeeInfo, employeeData) == expected



# Calculate the total value to pay

# Calculate the total value to pay with valid data
@pytest.mark.parametrize("expected",
                         [
                            ([ ['The amount to pay RENE is: 215.0 USD'],['The amount to pay ASTRID is: 85.0 USD'],['The amount to pay JHON is: 329.3 USD'] ])
                         ])
def test_calculatePayment(employeePayment, expected):
    assert employeePayment.calculate() == expected


def calculateEmployeePayment(file):
    employeePayment1 = EmployeePayment(file)
    employeePayment1.calculate()

# Calculate the total value to pay with a nonexistent file
@pytest.mark.parametrize("file", [("employees_data1.txt")])
def test_calculatePayment_fail(file):
    with pytest.raises(FileNotFoundError):
       calculateEmployeePayment(file)