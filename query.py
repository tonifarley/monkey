import bard
import openai

def ask(prompt, fn='', data='', ai='openai'):
    if fn:
        with open(fn) as f:
            data = f.read()
    if ai == 'bard':
        result = bard.query(prompt, data)
    else:
        result = openai.query(prompt, data)
    if result['error']:
        print('Error:', result['error'])
    else:
        if fn:
            fn, ext = fn.rsplit('.', 1)
            with open(f'{fn}-out.{ext}', 'w') as f:
                f.write(result['reply'])
        else:
            print(result['reply'])

def test():
    ask('Translate this text to French', data='Good morning', ai='bard')
    ask('Translate this text to French', data='Good morning')

def code(fn, task='correction'):
    tasks = {
        'completion': 'Complete the following code:',
        'correction': 'Correct the following code:'
    }
    ask(tasks[task], fn)

test()
code('local/code-error.py')
code('local/code-incomplete.py')
