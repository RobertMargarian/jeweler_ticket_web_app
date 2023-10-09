def parse_zipcode_data(file_path):
    file_path = 'populate_location/zipcodes.txt'
    zip_code_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                zip_code = parts[1]
                city = parts[2]
                state = parts[3]
                zip_code_data[zip_code] = {'city': city, 'state': state}

    return zip_code_data