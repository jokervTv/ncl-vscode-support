import json


def write_to_file(json_set, file_name):
    json_file = open(file_name, 'w', encoding='utf-8')
    json.dump(json_set, json_file, ensure_ascii=False, indent=4)
    json_file.close()


def read_json_file(file_name):
    json_file = open(file_name, 'r', encoding='utf-8')
    data = json.load(json_file)
    json_file.close()
    return data


if __name__ == '__main__':

    params_json = read_json_file('../snippets/function.json')
    tmLanguage_str = ""
    items = params_json.items()
    for key, value in items:
        tmLanguage_str += key + '|'
    print(tmLanguage_str)

    print("\n--------------------------------\n")

    params_json = read_json_file('../snippets/resources.json')
    tmLanguage_str = ""
    items = params_json.items()
    for key, value in items:
        tmLanguage_str += key + '|'
    print(tmLanguage_str)