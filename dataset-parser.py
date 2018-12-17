# 1. read dataset
# 2. parse dataset

# Testとtrainingをまぜてラベルをつける

# ホワイトリストとブラックリスト

#[TP FP] F値

import numpy as np
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

def extract_payload(str):
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

def decode_payload(str):
    str = urllib.parse.unquote_plus(str)
    str = urllib.parse.unquote_plus(str)
    return str

def generate_signature_password(str):
    arr = str.split('&')
    for data in arr:
        if 'password' in data:
            signature_arr = data.split('=')
            return signature_arr[1]

def check():
    pass

if __name__ == "__main__":
    counter = 0
    signature = np.array([])


    for i in parse_dataset('pro4/static/normalTrafficTraining.txt'):

        signature = signature.append(signature, generate_signature_password(extract_payload(i)))

    print(signature)

