from math import floor
from string import ascii_lowercase, ascii_uppercase
import base64
import string

from urlparse import urlparse

str_encode = str

url = 'https://docs.djangoproject.com/en/2.1/topics/forms/'

host = 'http://127.0.0.1:8000/'


def to_base62(num, b=62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + ascii_lowercase + ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res


def to_base10(num, b=62):
    base = string.digits + ascii_lowercase + ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res


original_url = url
print(urlparse(original_url).scheme)
if urlparse(original_url).scheme == '':
    url = 'http://' + original_url
else:
    url = original_url
b64 = base64.urlsafe_b64encode(url)
a = []
a.append(b64)
print b64
encoded_string = to_base62(a.index(b64))
print encoded_string

decoded = to_base10('absc123ab12asffgg11223')
print decoded
#
# url2 = base64.urlsafe_b64decode(a[decoded])
# print(url2)
# print(url == url2)
