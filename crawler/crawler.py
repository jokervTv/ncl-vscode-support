from bs4 import BeautifulSoup
import time
import requests
import json
import random

def write_to_file(json_set, file_name):
    json_file = open(file_name, 'w', encoding='utf-8')
    json.dump(json_set, json_file, ensure_ascii=False, indent=4)
    json_file.close()

def read_json_file(file_name):
    json_file = open(file_name, 'r', encoding='utf-8')
    data = json.load(json_file)
    json_file.close()
    return data


# Calculation time
time_begin = time.time()
# requests setting
headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.18 Safari/537.36 Edg/75.0.139.4'
}
requests.adapters.DEFAULT_RETRIES = 5
crawler = requests.session()
crawler.keep_alive = False

url_home = 'http://www.ncl.ucar.edu'
url_list_func = '/Document/Functions/list_alpha.shtml'
url_list_res = '/Document/Graphics/Resources/list_alpha_res.shtml'
url_list_color = '/Document/Graphics/color_table_gallery.shtml'
json_set = {}

# crawl NCL functions
## get function list
print("\nLoading ...")
print("##########################\n")
list_func_html = crawler.get(url_home+url_list_func, headers=headers).text
soup = BeautifulSoup(list_func_html, 'lxml').body.table.find_all('td', valign="top")
soup = BeautifulSoup(str(soup), 'lxml').find_all('a')
for link in soup:
    ## for each function
    ### Note: the first func 'abs' is out of list because of multiple 'a' tags
    #time.sleep(1)
    if isinstance(link.get('href'), str):
        func_name = link.string.replace('\n', ' ').strip()
        print("start: " + func_name)
        func_html = crawler.get(url_home+link.get('href'), headers=headers).text
        func_soup = BeautifulSoup(func_html, 'lxml').find('div', id='general_main')
        # get descriptions
        description = func_soup.p.get_text().replace('\n', ' ').strip()
        ## for the args
        arguments_soup = func_soup.pre.get_text()
        arguments_soup = arguments_soup[arguments_soup.index('(')+1 : arguments_soup.index(')')]
        arguments = arguments_soup.replace('\n\t\t', '\n').strip()
        ### construct body
        json_body = func_name + "("
        if len(arguments):
            i = 0
            for args in arguments.split('\n'):
                i = i + 1
                if i != 1:
                    json_body = json_body + ", ${" + str(i) + ":" + args.strip().split()[0] + "}"
                else:
                    json_body = json_body + "${" + str(i) + ":" + args.strip().split()[0] + "}"
        json_body = json_body + ")"
        ## construct json objection
        func_obj = {
            "prefix": func_name,
            "body": json_body,
            "description": description
        }
        json_set[func_name] = func_obj
        print("{:>40}".format("done."))

# crawl NCL resources
str_home_html = crawler.get(url_home + url_list_res, headers=headers).text
soup = BeautifulSoup(str_home_html, 'lxml').body.find_all('dt')
for res in soup:
    if res.string != None:
        res_name = str(res.string).strip()
    elif res.code != None:
        res_name = res.code.string.strip()
    elif res.strong != None:
        res_name = res.strong.string.strip()
    else :
        print("error :")
        print(res)
    res_obj = {
        "prefix": res_name,
        "body": res_name,
    }
    json_set[res_name] = res_obj
    print("res: {:<40s}{:<}".format(res_name, "done."))

# crawl NCL color table
str_home_html = crawler.get(url_home + url_list_color, headers=headers).text
soup = BeautifulSoup(str_home_html, 'lxml').body.find_all('table', border='1')
color_soups = BeautifulSoup(str(soup), 'lxml').find_all('td')
for color in color_soups:
    color_name = color.get_text('\n', strip=True).split('\n')[0]
    color_obj = {
        "prefix": color_name,
        "body": color_name,
    }
    json_set[color_name] = color_obj
    print("color: {:<40s}{:<}".format(color_name, "done."))

# write
write_to_file(json_set, "../snippets/snippets.json")
# Calculation time
time_end = time.time()
print('total time:', time_end-time_begin)
