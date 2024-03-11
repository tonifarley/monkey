import boto3, json, requests

secrets = boto3.client('secretsmanager')
s = secrets.get_secret_value(SecretId='palm')
key = json.loads(s['SecretString'])['key']

url = 'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001'
url += ':generateText'


def test():
    headers = {
        'Content-Type': 'application/json'
    }
    params = {'key':key}
    data = {'prompt': {'text': 'Write a poem about bananas'}}
    r = requests.post(url, headers=headers, params=params, data=json.dumps(data))
    if r.status_code == 200:
        print(r.json())
    else:
        print(r.status_code())

test()