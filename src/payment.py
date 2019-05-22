from src.time_utils import TimeUtils
from src.constants import CONSTRAINS


class PaymentUtils:

    def __init__(self):
        self.timeUtils = TimeUtils()

    def __getConstrain(self, valueByDate, iteration):
        if iteration == 2:
            startHourShiftNext = valueByDate[0]["start"]
            endHourShiftNext = valueByDate[1]["start"]
        else:
            startHourShiftNext = valueByDate[iteration + 1]["start"]
            endHourShiftNext = valueByDate[iteration+ + 1]["end"]
        return [startHourShiftNext, endHourShiftNext]

    def __isWithinTheLimit(self, startHour, endHour):
        lowerLimit = self.timeUtils.verifyHourLower(startHour[0], startHour[1])
        upperLimit = self.timeUtils.verifyHourUpper(endHour[0], endHour[1])
        return True if lowerLimit and upperLimit else False

    def __paymentPerDayWhenNotFound(self,startHour, endHour, valueByDate):
        for i in range(0, len(valueByDate), 1):
            startHourShift = valueByDate[i]["start"]
            endHourShift = valueByDate[i]["end"]

            [startHourShiftNext, endHourShiftNext] = self.__getConstrain(valueByDate, i)

            if self.__isWithinTheLimit([startHour, startHourShift], [endHour, endHourShiftNext]):
                totalFirstTurn = self.__paymentPerDay(startHour, [endHourShift[0], endHourShift[1]], valueByDate)
                totalSecondTurn = self.__paymentPerDay([startHourShiftNext[0], startHourShiftNext[1]], endHour, valueByDate)
                return totalFirstTurn + totalSecondTurn

    def __paymentPerDay(self,startHour, endHour, valueByDate):

        isFound = False
        amountToPay = 0

        for i in range(0, len(valueByDate),1):
            startHourShift = valueByDate[i]["start"]
            endHourShift = valueByDate[i]["end"]

            if self.__isWithinTheLimit([startHour, startHourShift], [endHour, endHourShift]):
                time = self.timeUtils.calculateTime(startHour, endHour)
                amountToPay = valueByDate[i]["USD"]*time
                isFound = True

        return amountToPay if isFound else self.__paymentPerDayWhenNotFound(startHour, endHour, valueByDate)

    def __calculateAmountToPay(self, name, employeeInfo):
        total = 0
        for i in range(0, len(employeeInfo)-1, 5):
            valueByDate = CONSTRAINS["TIME_WEEKDAY"] if (employeeInfo[i] in CONSTRAINS["WEEKDAY"]) else CONSTRAINS["TIME_WEEKEND"]
            total += self.__paymentPerDay([employeeInfo[i + 1], employeeInfo[i + 2]], [employeeInfo[i + 3], employeeInfo[i + 4]], valueByDate)
        return f'The amount to pay {name} is: {total} USD'

    def getAmountsToPaid(self, name, data):
        return list(map(lambda x: x(name, data), [self.__calculateAmountToPay]))
