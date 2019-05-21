class TimeUtils:

    def calculateTime(self,_startHour, _endHour):
        startHour = int(_startHour[0])
        startMinute = int(_startHour[1])
        endHour = int(_endHour[0])
        endMinute = int(_endHour[1])

        if (startHour >= 24 or endHour >= 24 or startMinute >= 60 or endMinute >= 60 or endHour < startHour): return 0
        if (startMinute > endMinute):
            endHour -= 1
            endMinute += 60
        return round(float(endHour - startHour + (endMinute - startMinute) / 60.0), 2)

    def verifyHourLower(self,time, shift):

        shiftHour = int(shift[0])
        hour = int(time[0])
        minute =int(time[1])
        if hour == shiftHour:
            return False if minute == 0 else True
        elif (hour > shiftHour):
            return True
        else:
            return False

    def verifyHourUpper(self,time, shift):

        shiftHour = int(shift[0])
        hour = int(time[0])
        minute =int(time[1])
        if (hour == shiftHour):
            return False if minute != 0 else True
        elif (shiftHour == 0):
            if (hour < 24):
                return True
        elif (hour < shiftHour):
            return True
        else:
            return False