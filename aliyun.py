#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request, parse
import hmac, datetime, uuid, base64
import json

Headers = {
    'Accept': 'text/json',
    'Content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

CommonParams = {
        'Format':'json',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureVersion': '1.0',
        'Timestamp': datetime.datetime.utcnow().isoformat(),
        'Version': '2015-01-09',
    }


def get_response_data(accessKeySecret, params):
    CommonParams['SignatureNonce'] = uuid.uuid1()
    params = sort_dict(params)

    params['Signature'] = sign(accessKeySecret, params)
    req = request.Request(url=f'https://alidns.aliyuncs.com/?{parse.urlencode(params)}', headers=Headers, method='GET')
    response = request.urlopen(req)
    return json.loads(response.read().decode('utf-8'))


def sort_dict(dic):
    result = {}
    for key in sorted(dic.keys()):
        result[key] = dic[key]
    return result


def check_domain_exists(access_key_id, access_key_secret, domain_name):
    CommonParams['AccessKeyId'] = access_key_id
    CommonParams['Action'] = 'DescribeDomainInfo'
    CommonParams['DomainName'] = domain_name
    try:
        get_response_data(access_key_secret, CommonParams)
        return True
    except Exception as e:
        print(e)
        return False


def create_domain(access_key_id, access_key_secret, domain_name):
    CommonParams['AccessKeyId'] = access_key_id
    CommonParams['Action'] = 'AddDomain'
    CommonParams['DomainName'] = domain_name
    try:
        get_response_data(access_key_secret, CommonParams)
    except Exception as e:
        print(e)
        pass


def get_record_value(access_key_id, access_key_secret, domain_name, domain_type, domain_line, sub_domain):
    CommonParams['AccessKeyId'] = access_key_id
    CommonParams['Action'] = 'DescribeDomainRecords'
    CommonParams['DomainName'] = domain_name
    CommonParams['TypeKeyWord'] = domain_type
    CommonParams['RRKeyWord'] = sub_domain
    try:
        data = get_response_data(access_key_secret, CommonParams)
        records = data['DomainRecords']['Record']
        for record in records:
            if record['Line'] == domain_line:
                return record['Value']
        return 0
    except Exception as e:
        print(e)
        return 0


def get_record_id(access_key_id, access_key_secret, domain_name, domain_type, domain_line, sub_domain):
    CommonParams['AccessKeyId'] = access_key_id
    CommonParams['Action'] = 'DescribeDomainRecords'
    CommonParams['DomainName'] = domain_name
    CommonParams['TypeKeyWord'] = domain_type
    CommonParams['RRKeyWord'] = sub_domain
    try:
        data = get_response_data(access_key_secret, CommonParams)
        records = data['DomainRecords']['Record']
        for record in records:
            if record['Line'] == domain_line:
                return record['RecordId']
        return 0
    except Exception as e:
        print(e)
        return 0


def add_record(access_key_id, access_key_secret, domain_name, domain_type, domain_line, sub_domain, localIP):
    CommonParams['AccessKeyId'] = access_key_id
    CommonParams['Action'] = 'AddDomainRecord'
    CommonParams['DomainName'] = domain_name
    CommonParams['RR'] = sub_domain
    CommonParams['Type'] = domain_type
    CommonParams['Line'] = domain_line
    CommonParams['Value'] = localIP

    try:
        data = get_response_data(access_key_secret, CommonParams)
        return data['RecordId']
    except Exception as e:
        print(e)
        return 0


def record_ddns(access_key_id, access_key_secret, record_id, domain_type, domain_line, sub_domain, localIP):
    CommonParams['AccessKeyId'] = access_key_id
    CommonParams['Action'] = 'UpdateDomainRecord'
    CommonParams['RecordId'] = record_id
    CommonParams['RR'] = sub_domain
    CommonParams['Type'] = domain_type
    CommonParams['Line'] = domain_line
    CommonParams['Value'] = localIP

    try:
        data = get_response_data(access_key_secret, CommonParams)
        return data['RecordId']
    except Exception as e:
        print(e)
        return 0


def sign(accessKeySecret, params):
    stringToSign = 'GET&%2F&' + parse.quote(parse.urlencode(params))
    h = hmac.new((accessKeySecret+'&').encode('utf-8'), stringToSign.encode('utf-8'), digestmod='sha1').digest()
    signature = base64.b64encode(h).decode('utf-8')
    print(signature)
    return signature
