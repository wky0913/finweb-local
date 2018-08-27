# -*- coding:utf-8 -*-
from jqdatasdk import *
from pub.config import TODAY, DATES, CODES
from pub.config import F_PATH, F_NAME
from pub.config import USE_LOCAL_DATA
from data_loader.data_loader import DataLoader
from data_ploter.data_ploter import TdFigPloter
from data_ploter.data_ploter import GzFigPloter
from file_operator.file_operator import FileOperator
from data_analyzer.data_analyzer import DataAnalyzer



# 评价类：评价数据，给出结论
class Evaluator(object):
    def __init__(self):
        pass
    def get_summary_data(self):
        pass
    def get_pe_plot_data(self):
        pass


def main():
    f_op = FileOperator(F_PATH+F_NAME)
    print(F_PATH+F_NAME)
    dic = f_op.read_file()


    if USE_LOCAL_DATA:
        info = dic['info']
        df = dic[info.ix[0,0]]
        dates = DATES
        dates = dates[dates.isin(df.index) ]
        DATES_LOCAL = dates

        da = DataAnalyzer(dic, CODES, DATES_LOCAL, TODAY)
        summary = da.get_summary()
    else:
        if not dic:
            dl = DataLoader(CODES, DATES)
            dic = dl.get_index_dic()
            f_op.save_file(dic)
        else:
            dic = f_op.flush_file(dic, DATES)
            f_op.save_file(dic)
        da = DataAnalyzer(dic, CODES, DATES, TODAY)
        summary = da.get_summary()

    for code in CODES:
        tdp = TdFigPloter(dic, code, DATES, TODAY, 'fig_type', method='pee')
        tdp.display()
        gzp = GzFigPloter(dic, code, DATES, TODAY, 'fig_type', method='pee')
        gzp.display()
    return summary


main()


