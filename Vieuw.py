import json 


def get_data(name_file: str): 
    with open(name_file) as f: 
        print(json.load(f))

get_data("result_scrap.json")