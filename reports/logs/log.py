# -*- coding:utf-8 -*-
import logging
import os
import time
from logging.handlers import RotatingFileHandler # 按文件大小滚动备份
from web_keys.environment_info.montage_url import home

logs_path = os.path.join(home,'logs')
# print('logs路径：',logs_path)

if not os.path.exists(logs_path):
    os.mkdir(logs_path)

log_name =  'test.{}.log'.format(time.strftime('%Y%m%f'))
logfile_name = os.path.join(home,log_name)
print('日志名：',logfile_name)

class HandeLogs:
    @classmethod
    def output_logs(self):
        logger = logging.getLogger(__name__)

        #防止重复答应
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s'
            )

            # 把日志输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(log_format)
            logger.addHandler(sh)

            # 把日志输出到文件里面
            fh = RotatingFileHandler(filename=logfile_name,mode='a',maxBytes=5242880,backupCount=7,encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(log_format)
            logger.addHandler(fh)

        return logger

handle = HandeLogs()
logs = handle.output_logs()

logs.info('这是info的日志信息')
logs.error('这是err')
logs.debug('这是debug')
logs.warning('这是警告')
