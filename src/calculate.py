import os
from src.utils import Utils
from src.payment import PaymentUtils

class EmployeePayment:

    def __init__(self, file):
        self.file=file
        self.util = Utils()
        self.paymentUtil = PaymentUtils()

    def __calculateTotalAmountToPay(self, data):
        values =[]
        info = self.util.getStructuratedData( data)
        [values.append(self.paymentUtil.getAmountsToPaid(employee[0],employee[1:])) for employee in info]
        return values

    def calculate(self):
        file = os.path.join(os.path.dirname(os.path.basename(os.getcwd())), "files", self.file)
        data = self.util.getInfoFromFile(file)
        return self.__calculateTotalAmountToPay(data)


if __name__ == '__main__':
    employeePayment=EmployeePayment("employees_data.txt")
    # print(employeePayment.calculate())
