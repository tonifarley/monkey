import boto3, json, requests
from bardapi import Bard

secrets = boto3.client('secretsmanager')
r = secrets.get_secret_value(SecretId='bard')
keys = json.loads(r['SecretString'])['key']
# "__Secure-1PSID", "__Secure-1PSIDCC", "__Secure-1PSIDTS"


def get_session():
    session = requests.Session()
    session.headers = {
        "Host": "bard.google.com",
        "X-Same-Domain": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://bard.google.com",
        "Referer": "https://bard.google.com/"
    }
    session.cookies.set("__Secure-1PSID", key) 

def query(prompt, text):
    print(f'querying bard')
    result = {'error': None, 'reply': ''}

    session = get_session()
    # bard = Bard(token=key, session=session, timeout=30)
    bard = Bard(token=key)
    reply = bard.get_answer(query)['content']
    return reply

def testedit():
    fn = 'wrecked'
    with open(f'local/{fn}.txt') as f:
        bard = Bard(token=key, session=session, timeout=30)
        reply = bard.get_answer('Edit to fix spelling, grammar and semantic errors:'
            + f.read()
        )['content']
        with open(f'local/{fn}-bard.txt', 'w') as fout:
            fout.write(reply)
