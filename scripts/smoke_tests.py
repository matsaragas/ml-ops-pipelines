import requests, time


URL = 'http://localhost:8080'
# wait up to 20s for service
for _ in range(20):
    try:
        r = requests.get(URL + '/health', timeout=2)
        if r.status_code == 200:
            print('Health OK')
            break
    except Exception:
        time.sleep(1)
else:
    print('Service did not become healthy')
    raise SystemExit(1)


# simple inference test
r = requests.post(URL + '/predict', json={'text': 'i love this'})
if r.status_code != 200:
    print('Predict endpoint failed:', r.text)
    raise SystemExit(1)
print('Predict OK, response:', r.json())