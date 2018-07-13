# -*- coding:utf-8 -*-
import pandas as pd


from operator import mod

WORDS = ['price','pe','pb','pee','pbe','pem','pbm']

# 数据加载类：获取数据，初步整理
class DataLoaderSingle(object):
    def __init__(self,code,date):
        stocks=get_index_stocks(code, date)
        dfn=len(stocks)
        if dfn<=0:
            df=pd.DataFrame()
        q=query(
            valuation.market_cap,valuation.pe_ratio,
            valuation.pb_ratio,              
            ).filter(valuation.code.in_(stocks))
        df=get_fundamentals(q, date)
        df=df.fillna(0)
        
        self.stocks = get_index_stocks(code, date)
        self.df = df
        self.dfn = len(stocks)
        self.code = code
        self.date = date
        
    def get_pe(self):
        if self.df.empty:
            return float('NaN')
        sum_p=sum(self.df.market_cap)
        sum_e=sum(self.df.market_cap/self.df.pe_ratio)    
        if sum_e > 0:
            pe=sum_p / sum_e
        else:
            pe=float('NaN') 
        return pe

    def get_pb(self):
        if self.df.empty:
            return float('NaN')
        sum_p=sum(self.df.market_cap)
        sum_b=sum(self.df.market_cap/self.df.pb_ratio)
        pb=sum_p/sum_b
        return pb

    def get_pee(self):
        if self.df.empty:
            return float('NaN')
        pee=len(self.df)/sum([1/p if p>0 else 0 for p in self.df.pe_ratio])
        return pee

    def get_pbe(self):
        if self.df.empty:
            return float('NaN')
        pbe=len(self.df)/sum([1/b if b>0 else 0 for b in self.df.pb_ratio])
        return pbe

    def get_pem(self):
        if self.df.empty:
            return float('NaN')
    
        pes=list(self.df.pe_ratio);pes.sort()    
        if mod(self.dfn,2)==0:
            pem=0.5*sum(pes[round(self.dfn/2-1):round(self.dfn/2+1)])
        else:
            pem=pes[round((self.dfn-1)/2)]
        return pem

    def get_pbm(self):
        if self.df.empty:
            return float('NaN')

        pbs=list(self.df.pb_ratio);pbs.sort()
        if mod(self.dfn,2)==0:
            pbm=0.5*sum(pbs[round(self.dfn/2-1):round(self.dfn/2+1)])
        else:
            pbm=pbs[round((self.dfn-1)/2)]
        return pbm
    
    def get_index_price(self):
        price = get_price(self.code, end_date=self.date, count=1, frequency='1d', fields=['close'])
        return price.ix[0,'close']


class DataLoaderSingleCode(object):
    def __init__(self, code, dates):
        s_date = get_all_securities(['index']).ix[code].start_date
        self.code = code
        self.dates = dates[dates>s_date]

    def get_pes(self):
        tmp = []
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            tmp.append(dls.get_pe())
        return pd.Series(tmp, index=self.dates)

    def get_pbs(self):
        tmp = []
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            tmp.append(dls.get_pb())
        return pd.Series(tmp, index=self.dates)

    def get_pees(self):
        tmp = []
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            tmp.append(dls.get_pee())
        return pd.Series(tmp, index=self.dates)

    def get_pbes(self):
        tmp = []
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            tmp.append(dls.get_pbe())
        return pd.Series(tmp, index=self.dates)

    def get_pems(self):
        tmp = []
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            tmp.append(dls.get_pem())
        return pd.Series(tmp, index=self.dates)

    def get_pbms(self):
        tmp = []
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            tmp.append(dls.get_pbm())
        return pd.Series(tmp, index=self.dates)

    def get_index_df(self):
        pes,pbs,pees,pbes,pems,pbms,prices = [],[],[],[],[],[],[]
        for date in self.dates:
            dls = DataLoaderSingle(self.code,date)
            pes.append(dls.get_pe())
            pbs.append(dls.get_pb())
            pees.append(dls.get_pee())
            pbes.append(dls.get_pbe())
            pems.append(dls.get_pem())
            pbms.append(dls.get_pbm())
            prices.append(dls.get_index_price())
        df = pd.DataFrame(index=self.dates) 
        for word in WORDS:
            df[word.upper()]=eval(word+'s')
        return df

    
class DataLoader(object):
    def __init__(self, codes, dates):
        self.codes = codes
        self.dates = dates
    def get_index_dic(self):
        dic = {}
        info = {}
        display_name=[]
        codes = []
        start_date = []
        end_date = []
        for code in self.codes:
            dl = DataLoaderSingleCode(code, self.dates)
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
        dic['info'] = pd.DataFrame(info)
        return dic
