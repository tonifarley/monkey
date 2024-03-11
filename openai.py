import boto3, requests, json

secrets = boto3.client('secretsmanager')
s = secrets.get_secret_value(SecretId='openai_api')
key = json.loads(s['SecretString'])['apikey']

headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}

def _response(response):
    result = {'error': None, 'result': {}}
    if response.status_code == 200:
        result['result'] = response.json()
    else:
        result['error'] = f'{response.status_code}: {response.reason}'
    return result

def get_model(id):
    r = requests.get('https://api.openai.com/v1/models/{id}', headers=headers)
    r = _response(r)
    if r['result']:
        r['result'] = r['result']['data']
    return r

def list_models():
    r = requests.get('https://api.openai.com/v1/models', headers=headers)
    r = _response(r)
    if r['result']:
        r['result'] = r['result']['data']
    return r

def list_model_ids():
    models = list_models()
    ids = [x['id'] for x in models['result']]
    return sorted(ids)

def query(prompt, text, model='gpt-3.5-turbo'):
    print(f'querying {model}')
    result = {'error': None, 'reply': '', 'usage': 0}
    config = {
        'model': model,
        'messages': [{'role': 'user', 'content': f'{prompt}: "{text}"'}],
        'temperature': .01
    }
    retries = 5
    while(retries):
        r = requests.post('https://api.openai.com/v1/chat/completions',
            json=config, headers=headers
        )
        if r.status_code == 200:
            r = r.json()
            choice = r['choices'][0]
            reason = choice['finish_reason']
            if reason != 'stop':
                result['error'] = f'Incomplete response, finish_reason = {reason}'
            result['reply'] = choice['message']['content'].strip()
            result['usage'] = r['usage']['total_tokens']
            retries = 0
        else:
            if r.status_code == 429:
                print(f'429 sleeping with retries={retries}')
                sleep(10/retries)
                retries -= 1
            else:
                result['error'] = handle_exception(r.text)
                retries = 0
    return result
