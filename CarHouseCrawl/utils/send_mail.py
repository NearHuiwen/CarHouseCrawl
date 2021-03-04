# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/8/28 17:59
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class SendMail(object):

    def __init__(self, smtp_server="smtp.qq.com",
                 smtp_port=465,
                 smtp_sender="寄件人",
                 smtp_senderpassword="senderpassword秘钥",
                 smtp_receiver=["收件人"],
                 smtp_subject="爬虫日志",
                 smtp_body="爬虫日志内容",
                 smtp_file=None):
        """
        to init parameter
        :param smtp_server: 邮件服务器
        :param smtp_port:端口号
        :param smtp_sender:发件人
        :param smtp_senderpassword:密码
        :param smtp_receiver:收件人
        :param smtp_subject:邮件主题
        :param smtp_body:邮件内容
        :param smtp_file_path:文件路径
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_sender = smtp_sender
        self.smtp_senderpassword = smtp_senderpassword
        self.smtp_receiver = smtp_receiver
        self.smtp_subject = smtp_subject
        self.smtp_body = smtp_body
        self.smtp_file = smtp_file

    def mail_content(self):
        """
        to edit mail content
        :param subject: 邮件主题
        :param body:邮件内容
        :return:msg
        """
        if self.smtp_file != None:
            msg = MIMEMultipart()

            apart=MIMEApplication(open(self.smtp_file, 'rb').read())
            apart.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.smtp_file))

            msg.attach(apart)

            msg.attach(MIMEText(self.smtp_body, "html", "utf-8"))
            msg['from'] = self.smtp_sender
            msg['to'] = ";".join(self.smtp_receiver)
            msg['subject'] = self.smtp_subject
            return msg
        else:
            msg = MIMEText(self.smtp_body, "html", "utf-8")
            msg['from'] = self.smtp_sender
            msg['to'] = ";".join(self.smtp_receiver)
            msg['subject'] = self.smtp_subject
            return msg

    def send_mail(self):
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp_server)
            smtp.login(user=self.smtp_sender, password=self.smtp_senderpassword)
        except:
            smtp = smtplib.SMTP_SSL()
            smtp.login(user=self.smtp_sender, password=self.smtp_senderpassword)
        aaa = self.mail_content()
        try:
            smtp.sendmail(self.smtp_sender, self.smtp_receiver, aaa.as_string())
            print("发送成功----")
        except Exception as e:
            print("发送失败...", e)
        smtp.quit()

