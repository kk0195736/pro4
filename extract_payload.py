import urllib.parse

def decode_payload(str):
    str = urllib.parse.unquote_plus(str)
    str = urllib.parse.unquote_plus(str)
    return str

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

if __name__ == "__main__":
    counter = 0

    for i in parse_dataset('pro4/static/anomalousTrafficTest.txt'):
        if extract_payload(i) != '':
            print(decode_payload(extract_payload(i)))
            print("---------------------------------------")
            counter += 1

    print(counter)
