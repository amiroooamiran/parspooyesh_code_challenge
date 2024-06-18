import json

def filter_temperature(data):
    if 'temperature' in data:
        if data['temperature'] < 0 or data['temperature'] > 60:
            return None
    return data

def filter_temp_check(data):
    f_data = filter_temperature(data)
    if f_data is not None:
        finallyData = json.dumps(f_data)
        print(finallyData)
        return finallyData
    else:
        print('[*] Data did not pass the filter(for more information look temp.log).')
        