import re


class Utils:

    @staticmethod
    def __match_data(data):
        pattern = '([{[a-z]+|[^a-z]+],[0-9]+}|[^=,:-]+)'
        return re.findall(pattern, data, re.IGNORECASE)

    def get_structure_of_data(self, data):
        data_output = []
        for i in data:
            data_output.append(self.__match_data(i))
        return data_output

    @staticmethod
    def get_info_from_file(file):
        employees_data = []
        try:
            file_data = open(file, "r").read().splitlines()
        except IOError:
            raise Exception("Archivo Invalido")
        for line in file_data:
            if len(line):
                employees_data.append(line)
            else:
                print("Empty Line")
        return employees_data
