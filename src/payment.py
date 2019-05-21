from src.time_utils import TimeUtils
from src.constants import CONSTRAINS

class PaymentUtils:

    def __init__(self):
        self.timeUtils = TimeUtils()

    def __paymentPerDayWhenNotFound(self,startHour,endHour,valueByDate):
        for i in range(0, len(valueByDate), 1):
            startHourShift = valueByDate[i]["start"]
            endHourShift = valueByDate[i]["end"]
            if (i == 2):
                startHourShiftNext = valueByDate[0]["start"]
                endHourShiftNext = valueByDate[1]["start"]
            else:
                startHourShiftNext = valueByDate[i + 1]["start"]
                endHourShiftNext = valueByDate[i + 1]["end"]

            lowerLimit = self.timeUtils.verifyHourLower(startHour, startHourShift)
            upperLimit = self.timeUtils.verifyHourUpper(endHour, endHourShiftNext)

            if (lowerLimit and upperLimit):
                totalFirstTurn = self.__paymentPerDay(startHour, [endHourShift[0], endHourShift[1]],valueByDate)
                totalSecondTurn = self.__paymentPerDay([startHourShiftNext[0], startHourShiftNext[1]], endHour, valueByDate)
                return totalFirstTurn + totalSecondTurn

    def __paymentPerDay(self,startHour,endHour,valueByDate):

        isFound = False
        amountToPay = 0

        for i in range(0, len(valueByDate),1):
            startHourShift = valueByDate[i]["start"]
            endHourShift = valueByDate[i]["end"]
            lowerLimit = self.timeUtils.verifyHourLower(startHour, startHourShift)
            upperLimit = self.timeUtils.verifyHourUpper(endHour, endHourShift)
            if(lowerLimit and upperLimit):
                time = self.timeUtils.calculateTime(startHour, endHour)
                amountToPay = valueByDate[i]["USD"]*time
                isFound = True
        if isFound:
            return amountToPay
        else:
            return self.__paymentPerDayWhenNotFound(startHour, endHour, valueByDate)


    def __calculateAmountToPay(self,name,employeeInfo):
        total = 0

        for i in range(0, len(employeeInfo)-1, 5):
            valueByDate = CONSTRAINS["TIME_WEEKDAY"] if (employeeInfo[i] in CONSTRAINS["WEEKDAY"]) else CONSTRAINS["TIME_WEEKEND"]
            total += self.__paymentPerDay([employeeInfo[i + 1], employeeInfo[i + 2]], [employeeInfo[i + 3], employeeInfo[i + 4]], valueByDate)
        return f'The amount to pay {name} is: {total} USD'

    def getAmountsToPaid(self,name,data):
        return list(map(lambda x: x(name,data), [self.__calculateAmountToPay]))