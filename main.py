import os 
import time

from tqdm import tqdm
import pandas as pd
import tomlkit

import src.krx as k
import src.mojito as m


def work1():
    # 설정 정보 불러오기
    conf = None
    with open("config.toml",'r',encoding="utf-8") as f:
        conf = tomlkit.load(f)

    # 저장/불러오기 경로
    rootPath =conf['path']['root']

    mk = k.MyKrx(rootPath)
    mk.get_stock_info()
    date = mk.reproduce_info()

    return date
    
    
def work2(date):
    # 설정 정보 불러오기
    conf = None
    with open("config.toml",'r',encoding="utf-8") as f:
        conf = tomlkit.load(f)
    
    # 저장/불러오기 경로
    rootPath =conf['path']['root']
    outputPath =conf['path']['output']

    # API 정보
    key=conf['hantoo']['key']
    secret=conf['hantoo']['secret']
    acc=conf['hantoo']['account']

    mym = m.MyMojito(key,secret,acc)
    df_symbols = mym.get_stock_symbols()
    # print(df_symbols)

    # 시장 전체 분봉 뽑기 (현재 안씀)
    # for i in df_symbols.index:
        # ss_info = df_symbols.loc[i,:].copy()
        # df_stock_1m = mym.get_today_1m_info(ss_info["단축코드"])

        # savePath = f"{rootPath}/{datePath}/{ss_info["시장"]}"
        # os.makedirs(f"{savePath}",exist_ok=True)
        # stock1mFile = f"{savePath}/{ss_info["단축코드"]}_분봉.tsv"
        # df_stock_1m.to_csv(df_stock_1m,sep='\t',header=True,index=False,encoding="utf-8-sig")

    rank = 30
    # nameList = ['거래량_전체', '거래량_코스피', '거래량_코스닥', '거래대금_전체', '거래대금_코스피', '거래대금_코스닥']
    nameList = ['거래량_전체','거래대금_전체']
    pbar1 = tqdm(nameList)
    for name in pbar1:
        pbar1.set_description(f"{name} 작업 중...")
        inputFile = f"{rootPath}/{date}/{name}.csv"
        df_input = pd.read_csv(inputFile,encoding="cp949",dtype=str).head(rank)
        inputList = df_input["종목코드"].tolist()

        outputCol = f"누적 {name.split('_')[0]}"  
        outputList = []
        pbar2 = tqdm(inputList)
        for i in pbar2:
            idx = df_symbols[df_symbols["단축코드"]==i].index.values.astype(int)[0]
            ss_info = df_symbols.loc[idx,:].copy()
            pbar2.set_description(f"{ss_info["단축코드"]},{ss_info["한글명"]}...")

            df_stock_1m = mym.get_today_1m_info(i)
            df_stock_10m = mym.get_stock_1m_to_xm(10)

            datePath = df_stock_10m.loc[0,"날짜"].replace('.','')
            cols = ["Label","Categories","Image"] + df_stock_10m["시간"].tolist()
            data = [ss_info["한글명"],"",""] + df_stock_10m[outputCol].tolist()
            outputDict = dict(zip(cols, data))
            outputList.append(outputDict)
            
            time.sleep(0.5)
        
        savePath = f"{outputPath}/{datePath}"
        os.makedirs(f"{savePath}",exist_ok=True)

        saveFile = f"{savePath}/{name}_{rank}.tsv"
        df_flourish = pd.DataFrame.from_records(outputList)
        df_flourish.to_csv(saveFile,sep='\t',header=True,index=False,encoding="utf-8-sig")

    return

def workflow():
    print('자동 부업 프로그램 실행.')
    date = work1()
    # date = "20240308"
    work2(date)
    print('자동 부업 프로그램 종료.')

    return

def subjob_schedule():
    import schedule

    schedule.every().monday.at('15:35').do(workflow)
    schedule.every().tuesday.at('15:35').do(workflow)
    schedule.every().wednesday.at('15:35').do(workflow)
    schedule.every().thursday.at('15:35').do(workflow)
    schedule.every().friday.at('15:35').do(workflow)

    print('자동 부업 스크립트 동작 중...')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__=="__main__":
    import sys
    args = sys.argv
    
    if args[1]=='auto':
        subjob_schedule()
    else:
        workflow()