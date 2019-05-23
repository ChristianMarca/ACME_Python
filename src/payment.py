from src.time_utils import TimeUtils
from src.constants import CONSTRAINS


class PaymentUtils:

    def __init__(self):
        self.timeUtils = TimeUtils()

    def __get_constrain(self, value_by_date, iteration):
        if iteration == 2:
            start_hour_shift_next = value_by_date[0]["start"]
            end_hour_shift_next = value_by_date[1]["start"]
        else:
            start_hour_shift_next = value_by_date[iteration + 1]["start"]
            end_hour_shift_next = value_by_date[iteration + 1]["end"]
        return [start_hour_shift_next, end_hour_shift_next]

    def __is_within_the_limit(self, start_hour, end_hour):
        lower_limit = self.timeUtils.verify_hour_lower(start_hour[0], start_hour[1])
        upper_limit = self.timeUtils.verify_hour_upper(end_hour[0], end_hour[1])
        return lower_limit and upper_limit

    def __payment_per_day_when_not_found(self, start_hour, end_hour, value_by_date):
        for i in range(0, len(value_by_date), 1):
            start_hour_shift = value_by_date[i]["start"]
            end_hour_shift = value_by_date[i]["end"]

            [start_hour_shift_next, end_hour_shift_next] = self.__get_constrain(value_by_date, i)

            if self.__is_within_the_limit([start_hour, start_hour_shift], [end_hour, end_hour_shift_next]):
                total_first_turn = self.__payment_per_day(start_hour, [end_hour_shift[0], end_hour_shift[1]], value_by_date)
                total_second_turn = self.__payment_per_day([start_hour_shift_next[0], start_hour_shift_next[1]], end_hour, value_by_date)
                return total_first_turn + total_second_turn

    def __payment_per_day(self, start_hour, end_hour, value_by_date):

        is_found = False
        amount_to_pay = 0

        for i in range(0, len(value_by_date), 1):
            start_hour_shift = value_by_date[i]["start"]
            end_hour_shift = value_by_date[i]["end"]

            if self.__is_within_the_limit([start_hour, start_hour_shift], [end_hour, end_hour_shift]):
                time = self.timeUtils.calculate_time(start_hour, end_hour)
                amount_to_pay = value_by_date[i]["USD"]*time
                is_found = True

        return amount_to_pay if is_found else self.__payment_per_day_when_not_found(start_hour, end_hour, value_by_date)

    def __calculate_amount_to_pay(self, name, employee_info):
        total = 0
        for i in range(0, len(employee_info)-1, 5):
            value_by_date = CONSTRAINS["TIME_WEEKDAY"] if (employee_info[i] in CONSTRAINS["WEEKDAY"]) else CONSTRAINS["TIME_WEEKEND"]
            total += self.__payment_per_day([employee_info[i + 1], employee_info[i + 2]], [employee_info[i + 3], employee_info[i + 4]], value_by_date)
        return f'The amount to pay {name} is: {total} USD'

    def get_amounts_to_paid(self, name, data):
        return list(map(lambda x: x(name, data), [self.__calculate_amount_to_pay]))
