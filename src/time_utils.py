class TimeUtils:

    @staticmethod
    def __cast_to_int(array_value):
        cast_items = []
        for item in array_value:
            cast_items.append(int(item))
        return cast_items

    def calculate_time(self, _start_hour, _end_hour):

        [start_hour, start_minute] = self.__cast_to_int(_start_hour)
        [end_hour, end_minute] = self.__cast_to_int(_end_hour)

        if start_hour >= 24 or end_hour >= 24 or start_minute >= 60 or end_minute >= 60 or end_hour < start_hour:
            return 0
        if start_minute > end_minute:
            end_hour -= 1
            end_minute += 60
        return round(float(end_hour - start_hour + (end_minute - start_minute) / 60.0), 2)

    @staticmethod
    def __is_lower(minute, hour, shift_hour):
        if hour == shift_hour:
            return not (minute and 0)
        return hour > shift_hour

    @staticmethod
    def __is_upper(minute, hour, shift_hour):
        if hour == shift_hour:
            return not (minute != 0)
        if shift_hour == 0 and hour < 24:
            return True
        return True if hour < shift_hour else False

    def verify_hour_lower(self, time, shift):

        shift_hour = self.__cast_to_int(shift)[0]
        [hour, minute] = self.__cast_to_int(time)

        return self.__is_lower(minute, hour, shift_hour)

    def verify_hour_upper(self, time, shift):

        shift_hour = self.__cast_to_int(shift)[0]
        [hour, minute] = self.__cast_to_int(time)

        return self.__is_upper(minute, hour, shift_hour)


