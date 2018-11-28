# 1. read dataset
# 2. parse dataset
'''
def read_dataset(path):
        f = open(path)
        for line in f:
                if line.find('GET') == 0 or if line.find('POST') == 0:
                        string 
        f.close()

if __name__ == '__main__':
read_dataset('./static/normalTrafficTraining.txt')
'''

import urllib.parse

def parse_dataset(filepath):
    text = ''
    with open(filepath) as f:
        for line in f:
            if ('GET' in line) or ('POST' in line) or ('PUT' in line):
                if text != '':
                    yield text
                    text = ''
            text = text + line
        yield text

def extract_http(str):
    arr = str.split('\n')
    method, url, _ = arr[0].split(' ')
    u = urllib.parse.urlparse(url)

    payload = ''

    if method == 'GET':
        payload = u.query
    elif method == 'POST' or method == 'PUT':
        for line in reversed(arr):
            if line == '':
                continue
            else:
                payload = line
                break


    return payload

if __name__ == "__main__":
    counter = 0

    for i in parse_dataset('pro4/static/normalTrafficTraining.txt'):
        if extract_http(i) != '':
            print(extract_http(i))
            print("--------------------------------------------------------------------------------")
            counter += 1
    print(counter)