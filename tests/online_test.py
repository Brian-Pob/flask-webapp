import requests
try:
    r = requests.head("https://news.brianpob.me")
    print(r.status_code)
    assert r.status_code == 200
    # prints the int of the status code. Find more at httpstatusrappers.com :)
except requests.ConnectionError:
    print("failed to connect")
