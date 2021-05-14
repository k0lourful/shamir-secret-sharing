import json
from secrets import choice

def is_prime(num):
    for i in range(2, num//2 + 1):
        if num % i == 0:
            return False
    return True

def split_secret(secret, k, n):
    # get min prime p after secret number
    p = secret + 1
    while True:
        if is_prime(p):
            break;
        p += 1
    # get random function coefficients
    power = k - 1
    coeffs = []
    for i in range(power):
        coeffs.append(choice(range(-64,64)))
    # write parts to array
    parts = []
    for i in range(n):
        part = 0
        for j in range(power):
            part += coeffs[j] * ((i+1) ** (power-(j+1)))
        parts.append((part+secret) % p)
    # write parts to json files in splits dir
    for i in range(n):
        with open('splits/part%i.json' % (i+1), 'w') as out:
            data = {}
            data['k'] = k
            data['part'] = parts[i]
            json.dump(data, out, indent = 4)

with open('secret.json', 'r') as f:
    secret_file = json.load(f)
    k = secret_file['k']
    n = secret_file['n']
    secret = secret_file['secret']
    split_secret(secret, k, n)
