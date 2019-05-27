import os
from src.utils import Utils
from src.payment import PaymentUtils


class EmployeePayment:

    def __init__(self, file):
        self.file = file
        self.util = Utils()
        self.paymentUtil = PaymentUtils()

    def __calculate_total_amount_to_pay(self, data):
        values = []
        info = self.util.get_structure_of_data(data)
        for employee in info:
            values.append(self.paymentUtil.get_amounts_to_paid(employee[0], employee[1:]))
        return values

    def calculate(self):
        file = os.path.join(os.path.dirname(os.path.basename(os.getcwd())), "files", self.file)
        data = self.util.get_info_from_file(file)
        return self.__calculate_total_amount_to_pay(data)


if __name__ == '__main__':
    employeePayment = EmployeePayment("employees_data.txt")
    data_with_info_to_paid = employeePayment.calculate()
    print(data_with_info_to_paid)

