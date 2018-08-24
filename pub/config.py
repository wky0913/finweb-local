# -*- coding:utf-8 -*-
#import jqdata
import os
import datetime
import numpy as np
import pandas as pd

from jqdatasdk import *

USE_LOCAL_DATA = True
USE_ONLINE_DATA = not USE_LOCAL_DATA
# 参数配置
TODAY   = datetime.datetime.today()
YESTDAY = TODAY-datetime.timedelta(days=1)
SDATE = '2018-07-01'
EDATE = TODAY
if USE_LOCAL_DATA:


    DATES=pd.date_range(SDATE, EDATE)

    # f_op = FileOperator(F_PATH+F_NAME)
    # dic = f_op.read_file()
    # info = dic['info']
    # df = dic[info.ix[0,0]]
    # print(df.index)



    # __date = []
    # for t in pd.date_range(SDATE, EDATE):
    #     __date.append(t.strftime('%Y-%m-%d'))
    # DATES = np.array(__date)
    # DATES =
else:
    auth('13811131769', '486194')
    DATES = np.array(get_trade_days(SDATE, EDATE))
F_PATH = os.path.abspath('./')
F_NAME = u'指数估值缓存文件.xlsx'
CODES = [
            ######宽基指数######
            #'000016.XSHG',#上证50
            '000300.XSHG',#沪深300
            '000905.XSHG',#中证500
            #'000852.XSHG',#中证1000
            #'399006.XSHE',#创业板指
            #'000922.XSHG',#中证红利
            ######行业指数######
            #'000991.XSHG',#全指医药
            #'000993.XSHG',#全指信息
            #'000990.XSHG',#全指消费
            #'000989.XSHG',#全指可选
            #'000992.XSHG',#全指金融
            ######主题指数######
            #'399812.XSHE',#中证养老
            #'399971.XSHE',#中证传媒
            #'399975.XSHE',#证券公司
            #'000827.XSHG',#中证环保
            #'399989.XSHE',#中证医疗
]
