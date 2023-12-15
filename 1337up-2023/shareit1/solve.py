from base64 import b64decode
from base64 import b64encode
import json

def updateiv(iv):
    list1 = list(iv)
    pos = [10, 11, 12, 13, 14]
    str1 = "false"
    str2 = "true "
    for i in range(0, len(pos)):
        list1[pos[i]] = list1[pos[i]] ^ ord(str1[i]) ^ ord(str2[i])
    return b64encode(bytes(list1)).decode()

cookie = "eyJ1c2VyX2RpY3QiOiAiUkh6VUVSd1hIdXVKbENISlBjUXg1NkpJakxoNDdKa1haN1hLT1pQd1haaG5UZDV6Q2x4R2UrVS9EdGVqVVNVWSIsICJpdiI6ICI0R1FSU09HbWNjKzh5RURsMUVmUmZBPT0ifQ=="
json_cookie = json.loads(b64decode(cookie).decode())
iv = b64decode(json_cookie['iv'])
new_iv = updateiv(iv)
json_cookie['iv'] = new_iv
new_cookie = b64encode(json.dumps(json_cookie).encode()).decode()
print(new_cookie)

# INTIGRITI{1v_1ike_t0_fl1p_bit5}
