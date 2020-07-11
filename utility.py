def shift_data(data):
    data_shift = data[6:] + '.' + data[4:6] + '.' + data[0:4]
    return data_shift
