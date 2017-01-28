import requests
import json


class CommentBot:

    @classmethod
    def post_comment(cls, form_data, ad_id):

        headers = {}

        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

        headers['Content-Type'] = 'application/json; charset=UTF-8'

        data = {
            'machineId': "",
            'adId':ad_id,
            'buyerName':form_data['name'],
            'email':form_data['email'],
            'fileName':'',
            'phoneNumber':form_data['phone'],
            'rand':'',
            'replyMessage': form_data['message']
        }

        data = json.dumps(data)

        session = requests.Session()

        response = session.post('https://www.gumtree.sg/rui-api/page/reply/model/en_SG', headers=headers, data=data)

        if response.status_code == 200 and '"replyFieldValid":true' in response.text:
            return True
        return False