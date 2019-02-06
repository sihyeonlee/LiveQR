import requests
from urllib.parse import urlencode
import json
import keydata


headers = {'Authorization': keydata.key()}
payload = {'cid': 'TC0ONETIME',
           'partner_order_id': '000',
           'partner_user_id': '100',
           'item_name': 'test',
           'quantity': '0',
           'total_amount': '1000',
           'tax_free_amount': '1000',
           'approval_url': 'test.com/s',
           'cancel_url': 'test.com/c',
           'fail_url': 'test.com/f'}

param = urlencode(payload)
print()
r = requests.post("https://kapi.kakao.com/v1/payment/ready", params=param, headers=headers)
data = json.loads(r.text)
print(data['next_redirect_mobile_url'])