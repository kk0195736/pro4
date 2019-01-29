import numpy as np
import urllib.parse
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split



# ２回デコードする
def decode_payload(string):
    string = urllib.parse.unquote_plus(string)
    string = urllib.parse.unquote_plus(string)
    return string


# テキストデータをパースする
def parse_dataset(filepath):
    text = ''
    with open(filepath) as f:
        for line in f:
            if ('GET' in line) or ('POST' in line) or ('PUT' in line):
                if text != '':
                    yield text
                    text = ''
            text += line
        yield text


# payloadを抽出する
def extract_payload(text):
    array = text.split('\n')
    method, url, _ = array[0].split(' ')
    u = urllib.parse.urlparse(url)

    payload = ''

    if method == 'GET':
        payload = u.query
    elif method == 'POST' or method == 'PUT':
        for line in reversed(array):
            if line == '':
                continue
            else:
                payload = line
                break

    return payload


# payloadを配列化する
def arrange_payload(payload):
    array = decode_payload(payload).split('&')
    while True:
        if len(array) == 14:
            return array
        array.append('')


# 全てのpayload配列を結合する
def payload_array(filepath):
    array = []

    for text in parse_dataset(filepath):
        payload = extract_payload(text)
        if payload == '':
            continue

        array.append(arrange_payload(payload))

    return array


# datasetが異常ならTrueを返す
def match_signature(signature, string):
    for i in signature:
        if i == 'script':
            if i in string.lower():
                return True
        else:
            if i in string:
                return True
    return False


# datasetを判定する
def check_dataset(signature, dataset):
    normal = 0
    anomalous = 0
    count = 0

    for row in dataset:
        if count == 500:
            break
        flag = False
        for i in row:
            if i == '':
                break
            if match_signature(signature, i):
                flag = True
                break
        count += 1
        if flag == True:
            anomalous += 1
        else:
            normal += 1

    return normal, anomalous


# 判定結果を平均する
def average_result(trials, result):
    array = []

    arrayNormal = []
    arrayAnomalous = []

    for i in range(trials):
        normal, anomalous = result
        arrayNormal.append(normal)
        arrayAnomalous.append(anomalous)

    array.append(sum(arrayNormal) / len(arrayNormal))
    array.append(sum(arrayAnomalous) / len(arrayAnomalous))

    return array

normalTarget = np.array([0]*16000)
anomalousTarget = np.array([1]*19586)

signature = np.array(['AND', 'OR', 'DELETE', 'SELECT', 'script', 'delay', 'cmd', 'A=', 'Set-cookie'])

if __name__ == "__main__":

    normalNpArray = np.array(payload_array('pro4/static/normalTrafficTest.txt'))
    anomalousNpArray = np.array(payload_array('pro4/static/anomalousTrafficTest.txt'))

    normalX_train, normalX_test, normaly_train, normaly_test = train_test_split(normalNpArray, normalTarget)
    anomalousX_train, anomalousX_test, anomalousy_train, anomalousy_test = train_test_split(anomalousNpArray, anomalousTarget)

    resultNormalDataset = average_result(10, check_dataset(signature, normalX_test))
    resultAnomalousDataset = average_result(10, check_dataset(signature, anomalousX_test))

    df_pie = pd.DataFrame([[resultNormalDataset[0], resultAnomalousDataset[0]], [resultNormalDataset[1], resultAnomalousDataset[1]]], index=['normal', 'anomalous'], columns=['normalTrafficTest', 'anomalousTrafficTest'])
    df_pie.plot.pie(subplots=True, autopct="%1.1f%%", figsize=(12, 6), startangle=90)

    print()
    print('signature:{}'.format(signature))
    print()
    print('-----normalTrafficTest-----')
    print('normal:{}'.format(resultNormalDataset[0]))
    print('anomalous:{}'.format(resultNormalDataset[1]))
    print('誤検知率:{}%'.format(resultNormalDataset[1] / 500 * 100))
    print()
    print('-----anomalousTrafficTest-----')
    print('normal:{}'.format(resultAnomalousDataset[0]))
    print('anomalous:{}'.format(resultAnomalousDataset[1]))
    print('検知率:{}%'.format(resultAnomalousDataset[1] / 500 * 100))
    print()

    plt.show()
