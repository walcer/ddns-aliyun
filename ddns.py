#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request
from datetime import datetime
import socket 
import json
import os
import re
import aliyun

global LocalIP
global HostIP
global Login_Token
global Domain_Id
global Access_Key_Id
global Access_Key_Secret

def init_domain(domain):
    domain_exists = aliyun.check_domain_exists(Access_Key_Id, Access_Key_Secret, domain['name'])
    if domain_exists == False:
        aliyun.create_domain(Access_Key_Id, Access_Key_Secret, domain['name'])


def ddns(domain):
    for sub_domain in domain['sub_domains']:
        record_value = aliyun.get_record_value(Access_Key_Id, Access_Key_Secret, domain['name'], 
                                                domain['type'], domain['line'], sub_domain)
        if record_value == 0:
            aliyun.add_record(Access_Key_Id, Access_Key_Secret, domain['name'], domain['type'], 
                                domain['line'], sub_domain, LocalIP)
        elif record_value != LocalIP:
            print(f"Begin update [{sub_domain}.{domain['name']}].")
            record_id = aliyun.get_record_id(Access_Key_Id, Access_Key_Secret, domain['name'], 
                                                domain['type'], domain['line'], sub_domain)
            aliyun.record_ddns(Access_Key_Id, Access_Key_Secret, record_id, domain['type'], 
                                domain['line'], sub_domain, LocalIP)
    
def get_ip():
    global LocalIP
    url = str(request.urlopen(r'http://txt.go.sohu.com/ip/soip').read())
    ip = re.findall(r'\d+.\d+.\d+.\d+', url)
    LocalIP = ip[0]
    print(f'LocalIP is {LocalIP}')
    #sock.close()

    
if __name__ == '__main__':
    global Login_Token
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.json"), "r"))

    Access_Key_Id = conf['access_key']
    Access_Key_Secret = conf['access_secret']
    Domains = conf['domains']
    
    try:
        get_ip()
        if os.path.isfile("ip_records.ddns"):
            with open("ip_records.ddns", "r") as f:
                lines = f.readlines()
                line = lines[-1].strip("\n")
                last_ip = line.split(" ")[-1]
                if last_ip != LocalIP:
                    print("IP addres changed, update the configure of aliyundns!")
                    for domain in Domains:
                        init_domain(domain)
                        ddns(domain)
                else:
                    print("IP addres not change!")
            with open("ip_records.ddns", "a") as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+last_ip+"\n")
        else:
            print("file not found, create it!")
            with open("ip_records.ddns", "w") as f:
                for domain in Domains:
                    init_domain(domain)
                    ddns(domain)
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+LocalIP+"\n")
    except Exception as e:
        print(e)
        pass
