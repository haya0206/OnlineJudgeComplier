import requests
url = "http://127.0.0.1:5000"
payload = {
    'source':'print("6",end="")',
    #'source' : "while True:\n   print('Hi')",
    'qnum':'1002',
    'languege':'5'
}
r = requests.post(url, payload)
print(r.text)