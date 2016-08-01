#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by yangliru,zhoupan on 8/1/16.
"""
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from Configure import Configure


class Alam():
    def __init__(self, mail):
        self.server = "smtp.mailgun.org"  # 设置服务器
        self.user = "ru@raydina.me"  # 用户名
        self.passwd = "823264073"  # 口令
        self.mail = mail  # 告警用户等级字典

    def send_list(self, level):
        match_data = []
        for (key, value) in self.mail.items():
            if int(key) <= level:
                match_data.append(value)
        return match_data

    def send_mail(self, level, message):
        mail_tuple = self.send_list(level)
        for i in range(len(mail_tuple)):
            print(mail_tuple[i])
            message = MIMEText('告警信息:%s' % message, 'plain', 'utf-8')
            message['From'] = Header(u"服务器<%s>" % self.user)
            message['To'] = Header(u"用户 <%s>" % mail_tuple[i])
            message['Subject'] = Header(u"告警信息")
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(self.server, 25)  # 25 为 SMTP 端口号
                smtpObj.login(self.user, self.passwd)
                smtpObj.sendmail(self.user, mail_tuple[i], message.as_string())
                print("邮件发送成功")
            except smtplib.SMTPException:
                print("Error: 无法发送邮件")


class Strategies():
    """告警策略定义"""

    def __init__(self):
        """类初始化"""
        cf = Configure()
        self.cpu_percent = float(cf.read_config('strategy.conf', 'cpu', 'usage'))
        self.svmem_precent = float(cf.read_config('strategy.conf', 'svmem', 'usage'))
        self.swap_precent = float(cf.read_config('strategy.conf', 'swap', 'usage'))
        self.diskio_precent = float(cf.read_config('strategy.conf', 'diskio', 'usage'))
        self.diskusage_precent = float(cf.read_config('strategy.conf', 'diskusage', 'usage'))
        self.netio_precent = float(cf.read_config('strategy.conf', 'netio', 'usage'))
        self.user = tuple(eval(cf.read_config('strategy.conf', 'user', 'user')))
        self.port = tuple(eval(cf.read_config('strategy.conf', 'port', 'port')))

    def check_cpu_data(self, cpu_percent):
        if cpu_percent > self.cpu_percent:
            return 1, "CPU使用率过高"
        else:
            return 0, "CPU使用率正常"

    def check_svmem_data(self, svmem_precent):
        if svmem_precent > self.svmem_precent:
            return 1, "内存使用率过高"
        else:
            return 0, "内存使用率正常"

    def check_swap_data(self, swap_precent):
        if swap_precent > self.swap_precent:
            return 1, "交换分区使用率过高，内存不足"
        else:
            return 0, "内存使用率正常"

    def check_diskio_data(self, diskio_precent):
        if diskio_precent > self.diskio_precent:
            return 1, "磁盘IO过高"
        else:
            return 0, "磁盘正常"

    def check_diskusage_data(self, diskusage_precent):
        if diskusage_precent > self.diskusage_precent:
            return 2, " 磁盘空间不足"
        else:
            return 0, "磁盘空间充足"

    def check_netio_data(self, netio_precent):
        if netio_precent > self.netio_precent:
            return 1, "网络占用率过高"
        else:
            return 0, "网络占用正常"

    def check_user_data(self, user):
        rtu = "以下用户非法登录："
        sign = 0
        for i in user:
            if i not in self.user:
                rtu += str(i)
                rtu += ','
                sign = 4

        if sign:
            return sign, rtu
        else:
            return 0, "登录用户正常"

    def check_port_data(self, port):
        rtu = "以下端口非法开启："
        sign = 0
        for i in port:
            if i not in self.port:
                rtu += str(i)
                rtu += ','
                sign = 4
        if sign:
            return sign, rtu
        else:
            return 0, "端口开启正常"


if __name__ == '__main__':
    # data = {'1': 'zhoupans_mail@163.com', '2': 'zhoupan@xiyoulinux.org'}
    # a = Alam(data, 2, '一号机器CPU使用率过高！')
    # a.send_mail()
    s = Strategies()
    print(s.check_cpu_data(80))
    print(s.check_cpu_data(91))
    print(s.check_svmem_data(40))
    print(s.check_svmem_data(93))
    print(s.check_swap_data(0))
    print(s.check_swap_data(11))
    print(s.check_diskio_data(80))
    print(s.check_diskio_data(94))
    print(s.check_diskusage_data(40))
    print(s.check_diskusage_data(71))
    print(s.check_netio_data(20))
    print(s.check_netio_data(91))
    print(s.check_user_data(('zhoupan', 'root', 'ubuntu',)))
    print(s.check_user_data(('zhoupan',)))
    print(s.check_port_data((80, 8000, 22, 3306, 90,)))
    print(s.check_port_data((80, 8000, 22, 3306,)))