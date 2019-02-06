import requests
from urllib.parse import urlencode
import json
import keydata

def call_api(val):
    print(val)
    headers = {'Authorization': keydata.key()}
    payload = {'cid': 'TC0ONETIME',
               'partner_order_id': 'TESTAPI',
               'partner_user_id': 'TESTAPI',
               'item_name': '테스트 상품',
               'quantity': '0',
               'total_amount': val,
               'tax_free_amount': val,
               'approval_url': 'test.com/s',
               'cancel_url': 'test.com/c',
               'fail_url': 'test.com/f'}

    param = urlencode(payload)
    r = requests.post("https://kapi.kakao.com/v1/payment/ready", params=param, headers=headers)
    print(r)
    data = json.loads(r.text)
    print(data['next_redirect_mobile_url'])

    return data['next_redirect_mobile_url']

