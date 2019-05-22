class TimeUtils:

    def __castToInt(self, arrayValue):
        castItems = []
        for item in arrayValue:
            castItems.append(int(item))
        return castItems

    def calculateTime(self, _startHour, _endHour):

        [startHour, startMinute] = self.__castToInt(_startHour)
        [endHour, endMinute] = self.__castToInt(_endHour)

        if startHour >= 24 or endHour >= 24 or startMinute >= 60 or endMinute >= 60 or endHour < startHour:
            return 0
        if startMinute > endMinute:
            endHour -= 1
            endMinute += 60
        return round(float(endHour - startHour + (endMinute - startMinute) / 60.0), 2)

    def verifyHourLower(self,time, shift):

        shiftHour = self.__castToInt(shift)[0]
        [hour, minute] = self.__castToInt(time)

        return (False if minute == 0 else True) if hour == shiftHour else True if hour > shiftHour else False

        # if hour == shiftHour:
        #     return False if minute == 0 else True
        # elif (hour > shiftHour):
        #     return True
        # else:
        #     return False

    def verifyHourUpper(self, time, shift):

        shiftHour = self.__castToInt(shift)[0]
        [hour, minute] = self.__castToInt(time)

        if hour == shiftHour:
            return False if minute != 0 else True
        elif shiftHour == 0:
            if hour < 24:
                return True
        elif hour < shiftHour:
            return True
        else:
            return False
