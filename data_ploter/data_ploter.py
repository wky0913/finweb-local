# -*- coding:utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt

from jqdatasdk import *

class Ploter(object):
    def __init__(self, dic, code, dates, date, fig_type, method='pee'):
        self.dic = dic
        self.code = code
        self.dates = dates
        self.date = date
        self.fig_type = fig_type
        self.method = method
        df=self.dic[self.code]
        self.df = df[df.index.isin(self.dates)]
    
    def get_fig_name(self):
        df = self.dic['info']
        return df[df['code']==self.code].display_name.iloc[0]
    
    def get_fig_cal_cur_val(self):
        return self.df.ix[self.date.date(),self.method.upper()]
    
    def get_fig_cal_price(self):
        cal_val = self.get_fig_cal_cur_val()
        cal_price = self.df['PRICE']*(cal_val/self.df[self.method.upper()])
        
        return cal_price
        
    def display_single(self, fig_data):
        plt.figure(figsize=(15,8))
        plt.title(fig_data['name']+fig_data['desc'])
        for d in fig_data['data']:
            #plt.plot(self.dates, d['data'], label=d['label'])
            plt.plot(d['data'].index, d['data'], label=d['label'])
        plt.legend()
        plt.grid(True)
        plt.savefig('../' + fig_data['name'] + fig_data['desc'])
        plt.show()



'''
fig_data={
         'name':'中证500',
         'desc':'中证500估值图',
         'data':[{'data':[], 'label':u'指数'},
                 {'data':[], 'label':u'指数'}]
 }
'''
class TdFigPloter(Ploter):
    def assemble_fig_data(self):
        data1 = {'data':self.df['PRICE'],
                 'label':u'指数'
                }
        data2 = {'data':self.get_fig_cal_price(),
                 'label':u'当前估值线'
                }
        fig_data={'name':self.get_fig_name(),
                  'desc':u'通道图',
                  'data':[data1,data2]
                 }
        return fig_data

    def display(self):
        fig_data = self.assemble_fig_data()
        self.display_single(fig_data)
    

    
class GzFigPloter(Ploter):
    def assemble_fig_data(self):
        data1 = {'data':self.df[self.method.upper()],
                 'label':self.method.upper()
                }
        data2 = {'data':pd.Series(self.get_fig_cal_cur_val(), index=self.df[self.method.upper()].index),
                 'label':u'当前'+self.method.upper()
                }
        fig_data={'name':self.get_fig_name(),
                  'desc':u'估值图',
                  'data':[data1,data2]
                 }
        return fig_data

    def display(self):
        fig_data = self.assemble_fig_data()
        self.display_single(fig_data)    


