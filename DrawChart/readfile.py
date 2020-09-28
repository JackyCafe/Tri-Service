import pandas as pd
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

class TriMongo(object):
    df:pd.DataFrame

    def __init__(self,df):
        self.df = df
        self.clients = MongoClient()
        self.database = self.clients['tri_db']
        self.collection = self.database['health_data']
        self.records = self.df.to_dict("records")

    # 丟入兩個參數，尋訪mongodb 後
    # 取得 [{id,參數1,參數2}]

    def get_by_param(self,base,relation)-> dict:
        datas = self.collection.find({},{base:1,relation:1})
        c_id = []
        c_base = []
        c_relation = []
        c = {}
        for num,data in enumerate(datas,start=1):
            # print(f'{i},{data}')
            c_id.append(f'{data.get("_id")}')
            c_base.append(float(data.get(base)))
            c_relation.append(float(data.get(relation)))



        c = {'id':c_id,base:c_base,relation:c_relation}
        return c

    def insert(self):
        self.collection.insert_many(self.records)


def main():
    df = pd.read_csv('../data/health_data.csv')
    cols = df.columns.array
    tri_db = TriMongo(df)
    # 將資料寫入mongodb,只需run 一次
    # tri_db.insert()

    # for num,col in  enumerate(cols,start=0):
    #     print(f'{num},{col}')
    base = cols[152]

    for i in range(153,228):
        relation = cols[i]
        c = tri_db.get_by_param(base,relation)
        draw(c,base,relation)
#
def draw(c,base,relation,num=1000):
    try:
        x = np.array(c.get(base), np.float32)
        y = np.array(c.get(relation), np.float32)
        from math import nan
        coff = np.corrcoef(x,y)
        fig, ax = plt.subplots()
        plt.title(f'{base} vs { relation}  ')
        ax.scatter(x,y,s=10,c='red',marker='o',alpha=0.5,label= relation)
        ax.text(10,10,str(coff),fontsize=12)
        plt.savefig(f'..\\pic\\{base} vs { relation.replace("/","_")}.png')
        plt.show()
    except:
        print(f'..\\pic\\{base} vs { relation.replace("/","_")}.png')

if __name__ == '__main__':
    main()