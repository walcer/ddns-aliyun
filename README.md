# ddns-aliyun

ddns-aliyun 是基于[阿里云解析DNS](https://help.aliyun.com/product/29697.html)服务的动态解析脚本，用于检测 IP 变化并更新至阿里云，支持多域名解析。支持 Linux 设备，包括树莓派（[Raspberry Pi](https://www.raspberrypi.org/)）。定期动态监测外网IP变化，自动添加指定路线的解析记录。


`@version 0.1.1`    base on [`tinko`](https://github.com/dingguotu/ddns-aliyun)

---

## 关键词(Key Words)

1. domain ：域名
2. sub_domain ：子域名，二级域名
3. type ：记录类型（A、NS、MX、TXT、CNAME、SRV、AAAA、CAA、REDIRECT_URL、FORWARD_URL）[参见解析记录类型格式](https://help.aliyun.com/document_detail/29805.html?spm=a2c4g.11186623.2.15.402c2846nY0Gzp)    
4. line ：解析路线（default、telecom、unicom、mobile、oversea、edu、drpeng、btvn）[参见解析线路枚举](https://help.aliyun.com/document_detail/29807.html?spm=a2c4g.11186623.2.16.402c2846nY0Gzp)    

---

## 前置条件(Requirements)

1. Git
2. python 3.6+
3. 阿里云账号(已购置域名)

---

## 使用方法（Steps）    

**本步骤在树莓派3B+，[raspios_lite_arm64-2020-08-24](https://mirrors.tuna.tsinghua.edu.cn/raspberry-pi-os-images/raspios_lite_arm64/images/raspios_lite_arm64-2020-08-24/)下测试通过**    

+ 1.  首先，确保已经安装 [git](https://git-scm.com/) 客户端以及 [python 3.*](https://www.python.org/downloads/)，建议python 3.6+

        通过本命令，克隆ddns-aliyun到本地

        ```bash
        cd /opt
        sudo git clone https://github.com/dingguotu/ddns-aliyun.git
        ```

+ 2.  接下来到阿里云中创建AccessKey，具体步骤是：    
    登录阿里云 -> 进入控制台 -> 点击accesskeys    
    ![accesskeys](img/accesskeys.png)    
    -> 创建AccessKey     
    ![AccessKey](img/create-access-key.png)    
    **注** ：如果域名是在腾讯云或其他非阿里云处购买的，还需要进入相对应的服务商控制台，修改域名的DNS地址为：    
        ```bash
        ns1.alidns.com
        ns2.alidns.com
        ```

+ 3.  复制 `conf.sample.json` 文件，并重命名为 `conf.json`，根据您的DNSPod设置修改 `conf.json` 文件，填入以下内容：    
        ```bash
        {
            "access_key": <access_key>,
            "access_secret": <access_secret>,
            "domains": [
                {
                    "name": <first_domain>,
                    "type": "A",
                    "line": "default",
                    "sub_domains": [<first_sub_domain_name>, <second_sub_domain_name>,...]
                },
                {
                    "name": <second_domain>,
                    "type": "A",
                    "line": "edu",
                    "sub_domains": [<first_sub_domain_name>, <second_sub_domain_name>,...]
                }
            ]
        }
        ```
        > `domains`是一个数组，其中每一个变量为一个字典,列明了某个域名下要绑定的特定记录类型、特定解析路线的子域名,请按需设置；    
        
        > `name`即为在阿里云所拥有的域名；    

        > `type`即为记录类型，通常绑定IPv4地址为A，IPv6地址为AAAA，···；    
        
        > `line`即为解析路线，当一个IP只绑定到一个域名是，请务必设置为`default`,当绑定到多个域名时，至少保证有一个域名绑定为`default`，其它域名自行选择解析路线

        > `sub_domains`通常写 `@` 和 `*` 就够了，二级子域名直接用 `*` 代替，然后在自己的代理服务器（IIS，nginx，Apache等）上面去进行绑定。domain 和 sub_domain 可以不需要事先手动绑定，本程序会自动识别

+ 4. 设置 crontab 定时任务，没30分钟更新DNS记录，并将执行日志写道文件ddns.log：    
        ```bash
        sudo crontab -e
        */30 * * * * python3 /opt/ddns-aliyun/ddns.py >> /opt/ddns-aliyun/ddns.log 2>&1
        ```
        本教程的定时任务是Linux版本，`*/30` 表示每隔30分钟运行一次，可以自行修改，本教程不做限定。`/opt/ddns-aliyun/ddns.py` 是绝对路径，请根据实际情况进行修改    
        
        Windows版请自行学习[Windows 任务计划](https://jingyan.baidu.com/article/0964eca26a53b08285f536d2.html)
