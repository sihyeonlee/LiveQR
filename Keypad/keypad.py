import serial


def connection(port, baudrate):
    ser = serial.Serial(port, baudrate)

    return ser


def read_data(serial):
    raw_data = serial.readline()
    len = raw_data.index(13)            # Index '\r'
    int_data = int(raw_data[0:len])

    return int_data


def mapping(num, map):
    if num < 740:
        for i in range(0, 16):
            if map[i][0] <= num <= map[i][1]:
                return i


def check_overlap(temp, data):
    if temp != data:
        return data
    else:
        return -1


def cal_array(array):
    len_ = len(array)
    sum_ = 0

    for i in range(0, len_):
        sum_ += array[i] * (10 ** (len_ - i - 1))

    return sum_


def activation():
    array_adc_map = [[0, 10],
                     [38, 48],
                     [85, 100],
                     [130, 150],
                     [175, 195],
                     [222, 245],
                     [270, 290],
                     [315, 335],
                     [364, 385],
                     [410, 435],
                     [440, 485],
                     [501, 530],
                     [550, 575],
                     [598, 630],
                     [648, 680],
                     [695, 730]]
    array_key_map = [[0, 7],
                     [1, 8],
                     [2, 9],
                     [3, 'A'],
                     [4, 4],
                     [5, 5],
                     [6, 6],
                     [7, 'B'],
                     [8, 1],
                     [9, 2],
                     [10, 3],
                     [11, 'C'],
                     [12, 'ESC'],
                     [13, 0],
                     [14, 'Enter'],
                     [15, 'D']]
    dic_key_map = {0: 7, 1: 8, 2: 9, 3: 'A', 4: 4, 5: 5, 6: 6, 7: 'B', 8: 1, 9: 2, 10: 3, 11: 'C',
                   12: 'ESC', 13: 0, 14: 'Enter', 15: 'D'}
    array_command = [3, 7, 11, 12, 14, 15]
    array_num = [0, 1, 2, 4, 5, 6, 8, 9, 10, 13]
    temp = -1
    array_value = []

    try:
        ser = connection('COM4', 9600)

    except serial.serialutil.SerialException:
        ser = connection('/dev/ttyUSB0', 9600)

    while 1:
        data = mapping(read_data(ser), array_adc_map)
        if check_overlap(temp, data) == -1 or data == None:
            temp = data
            continue

        temp = data

        if data in array_num:
            array_value.append(dic_key_map[data])
            print(array_value)
        if data in array_command:
            if dic_key_map[data] == 'ESC':
                try:
                    array_value.pop()
                    print(array_value)
                except IndexError:
                    pass
            elif dic_key_map[data] == 'Enter':
                total = cal_array(array_value)
                print(total)
                array_value = []

                return total
            else:
                pass