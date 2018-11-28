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


N = []

if __name__ == "__main__":

    N.append(parse_dataset("./static/normalTrafficTraining.txt"))

    print(N)
