# -*- coding:utf-8 -*-
from jqdatasdk import *
from data_loader import DataLoader
from data_ploter import TdFigPloter
from data_ploter import GzFigPloter
from file_operator import FileOperator
from data_analyzer import DataAnalyzer
from config import TODAY, YESTDAY, SDATE, EDATE
from config import DATES, FILEN, CODES


# 评价类：评价数据，给出结论
class Evaluator(object):
    def __init__(self):
        pass
    def get_summary_data(self):
        pass
    def get_pe_plot_data(self):
        pass


def main():
    f_op = FileOperator(FILEN)
    dic = f_op.read_file()
    if not dic:
        dl = DataLoader(CODES, DATES[:])
        dic = dl.get_index_dic()
        f_op.save_file(dic)
    else:
        dic = f_op.flush_file(dic, DATES[:])
        f_op.save_file(dic)
    da = DataAnalyzer(dic, CODES, DATES[:], TODAY)
    summary = da.get_summary()

    for code in CODES:
        tdp = TdFigPloter(dic, code, DATES[:], TODAY, 'fig_type', method='pee')
        tdp.display()
        gzp = GzFigPloter(dic, code, DATES[:], TODAY, 'fig_type', method='pee')
        gzp.display()
    return summary


main()


