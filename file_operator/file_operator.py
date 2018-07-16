# -*- coding:utf-8 -*-
import pandas as pd
import os

from jqdatasdk import *
from data_loader.data_loader import DataLoaderSingleCode
from pub.config import CODES

class FileOperator(object):
    def __init__(self,file,dic={}):
        self.dic = dic
        self.file = file
    def save_file(self, dic):
        try:
            writer=pd.ExcelWriter(self.file)
            for code in dic:
                df=dic[code]
                df.to_excel(writer,code)
            writer.save()
            writer.close()
        except Exception as e:
            print("[save_file]:Save file failed!")
            print(e)

    def read_file(self):
        try:
            if not os.path.exists(self.file):
                return {}
            info=pd.read_excel(self.file,'info')
            dic={}
            for code in list(set(CODES+list(info.ix[:,'code']))):
                if code in info['code'].values:
                    dic[code]=pd.read_excel(self.file,code)
            dic['info'] = info
            return dic
        except FileNotFoundError:
            return {}

    def flush_file(self, dic, dates):
        # 获取要更新的日期
        for code in dic:
            if code != 'info':
                old_dates=dic[code].index
                break
        old_dates = [d.date() for d in old_dates]
        new_dates=pd.Series(list(set(dates)-set(old_dates))).sort_index(ascending=True)
        
        # 更新旧指数中的日期数据
        if not new_dates.empty:
            tmp={}
            for code in dic:
                if code != 'info':
                    dlsc = DataLoaderSingleCode(code, new_dates)
                    tmp[code] = dlsc.get_index_df()
                    dic[code] = dic[code].reindex(index=[d.date() for d in dic[code].index])
                    dic[code] = pd.concat([dic[code],tmp[code]]).sort_index(ascending=True)

        # 增加旧dic中的指数
        new_codes=set(CODES)-set(dic)
        info = {}
        display_name=[]
        codes = []
        start_date = []
        end_date = []
        if new_codes:
            for code in new_codes:
                if code != 'info':
                    dl = DataLoaderSingleCode(code, dates[:])
                    dic[code] = dl.get_index_df()
                raw_info = get_security_info(code)
                codes.append(raw_info.code)
                display_name.append(raw_info.display_name)
                start_date.append(raw_info.start_date)
                end_date.append(raw_info.end_date)
            info['code'] = codes
            info['display_name'] = display_name
            info['start_date'] = start_date
            info['end_date'] = end_date
            info=pd.DataFrame(info)
            dic['info']=pd.concat([dic['info'],info],axis=0,ignore_index=True)
        return dic

