import re


class Utils:

    def __matchData(self, data):
        pattern = '([{[a-z]+|[^a-z]+],[0-9]+}|[^=,:-]+)'
        return re.findall(pattern, data, re.IGNORECASE)

    def getStructuratedData(self, data):
        data_output = []
        for i in data:
            employeeInfo = list(map(lambda x: x(i), [self.__matchData]))
            [data_output.append(info) for info in employeeInfo]
        return data_output

    def getInfoFromFile(self,file):
        employees_data = []
        file_data = open(file, "r").read().splitlines()
        for line in file_data:
            if len(line):
                employees_data.append(line)
            else:
                print("Empty Line")
        return employees_data
