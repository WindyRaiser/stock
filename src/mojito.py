import mojito
import numpy as np
import pandas as pd

class MyMojito:
    def __init__(self,key,secret,acc):
        # 한국투자 API 접속 인스턴스 생성
        self.broker = mojito.KoreaInvestment(api_key=key,api_secret=secret,acc_no=acc)

        return
    

    def get_stock_symbols(self):
        # 종목검색을 위한 데이터 파싱 
        # 그룹코드 = 주식분류코드(ST)
        # 단축코드 = 주식코드(005930)
        # 한글명 = 주식회사명(삼성전자)
        # 시장 = 주식시장명(코스닥/코스피)
        self.df_symbols = self.broker.fetch_symbols().reset_index(drop=True)

        return self.df_symbols


    def get_today_1m_info(self,stockCode):
        res = self.broker.fetch_today_1m_ohlcv(stockCode)
        df_stock_1m = pd.DataFrame.from_records(res["output2"])
        df_stock_1m = df_stock_1m.drop(columns=["stck_hgpr","stck_lwpr"])
        df_stock_1m = df_stock_1m.rename(columns={"stck_bsop_date":"날짜","stck_cntg_hour":"시간","stck_oprc":"주식 시작가","stck_prpr":"주식 현재가","cntg_vol":"체결 거래량","acml_tr_pbmn":"누적 거래대금"}).astype(np.int64)

        df_stock_1m = df_stock_1m.sort_values(["날짜","시간"],ascending=True,ignore_index=True)
        df_stock_1m["날짜"] = df_stock_1m["날짜"].apply(lambda x: pd.to_datetime(x,format="%Y%m%d")).dt.strftime("%Y.%m.%d")
        df_stock_1m["시간"] = df_stock_1m["시간"].apply(lambda x: pd.to_datetime(x,format="%H%M%S")).dt.strftime("%H:%M:%S")
        df_stock_1m["누적 거래량"] = df_stock_1m["체결 거래량"].cumsum()

        openPrice = df_stock_1m.loc[0,"주식 시작가"]
        df_stock_1m["주식 상승률"] = round((df_stock_1m["주식 현재가"] - openPrice) / openPrice * 100,2)
        df_stock_1m = df_stock_1m.drop(columns=["체결 거래량"])
        df_stock_1m = df_stock_1m[["날짜","시간","주식 상승률","누적 거래량","누적 거래대금"]]

        self.df_stock_1m = df_stock_1m
        
        return self.df_stock_1m
    

    def get_stock_1m_to_xm(self,minute):
        df_stock_1m = self.df_stock_1m

        if minute == 5:
            df_stock_xm = df_stock_1m[(df_stock_1m["시간"].str.contains("09:01:00")) | (df_stock_1m["시간"].str.contains(":.0:",regex=True)) | (df_stock_1m["시간"].str.contains(":.5:",regex=True))].reset_index(drop=True).copy()
        elif minute == 10:
            df_stock_xm = df_stock_1m[(df_stock_1m["시간"].str.contains("09:01:00")) | (df_stock_1m["시간"].str.contains(":.0:",regex=True))].reset_index(drop=True).copy()

        df_stock_xm.loc[0,"시간"] = "09:00:00"
        self.df_stock_xm = df_stock_xm
        
        return self.df_stock_xm
    


# def parse_stock_info(rootPath, broker):
#     # 종목검색을 위한 데이터 파싱 
#     # 그룹코드 = 주식분류코드(ST)
#     # 단축코드 = 주식코드(005930)
#     # 한글명 = 주식회사명(삼성전자)
#     # 시장 = 주식시장명(코스닥/코스피)
#     df_symbols = broker.fetch_symbols().reset_index(drop=True)

#     pbar = tqdm(df_symbols.index)
#     for i in pbar:
#         ss_info = df_symbols.loc[i,:].copy()
#         pbar.set_description_str(f"Download at {ss_info["단축코드"]},{ss_info["한글명"]}...")

#         # 당일분봉 데이터 파싱 
#         result = broker.fetch_today_1m_ohlcv(ss_info["단축코드"])
#         ss_info["날짜"] = result["output2"][0]["stck_bsop_date"]

#         # 당일분봉 데이터 프레임 작업 진행
#         df_stock = pd.DataFrame.from_records(result["output2"])
#         df_stock = df_stock.drop(columns=["stck_oprc","stck_hgpr","stck_lwpr"])
#         df_stock = df_stock.rename(columns={"stck_bsop_date":"날짜","stck_cntg_hour":"시간","stck_prpr":"주식 현재가","cntg_vol":"체결 거래량","acml_tr_pbmn":"누적 거래 대금"}).astype(int)

#         df_stock = df_stock.sort_values(["날짜","시간"],ascending=True,ignore_index=True)
#         df_stock["날짜"] = df_stock["날짜"].apply(lambda x: pd.to_datetime(x,format="%Y%m%d")).dt.strftime("%Y.%m.%d")
#         df_stock["시간"] = df_stock["시간"].apply(lambda x: pd.to_datetime(x,format="%H%M%S")).dt.strftime("%H:%M:%S")
#         df_stock["누적 거래량"] = df_stock["체결 거래량"].cumsum()
#         df_stock = df_stock.drop(columns=["체결 거래량"])
#         df_stock = df_stock[["날짜","시간","주식 현재가","누적 거래량","누적 거래 대금"]]
        
#         # 당일 분봉 데이터 저장
#         savePath = f"{rootPath}/{ss_info["날짜"]}/{ss_info["시장"]}"
#         os.makedirs(f"{savePath}",exist_ok=True)
#         stockFile = f"{savePath}/{ss_info["단축코드"]}_분봉.tsv"
#         df_stock.to_csv(stockFile,sep='\t',header=True,index=False,encoding="utf-8-sig")

#         # break
#         time.sleep(0.3)

#     return


# def convert_flourish_format(rootPath,datePath,codeList,broker):
#     df_symbols = broker.fetch_symbols().reset_index(drop=True)

#     cols = []
#     dataAList = []
#     dataBList = []
#     dataCList = []
    
#     for code in codeList:
#         idx = df_symbols[df_symbols["단축코드"]==code].index.values.astype(int)[0]
#         ss_info = df_symbols.loc[idx,:].copy()
#         print(f"{ss_info["단축코드"]},{ss_info["한글명"]}")

#         savePath = f"{rootPath}/{datePath}/{ss_info["시장"]}"
#         stockFile = f"{savePath}/{ss_info["단축코드"]}_분봉.tsv"

#         df_stock = pd.read_csv(stockFile,sep='\t',encoding="utf-8-sig")
#         df_stock = df_stock.drop(columns=["체결 거래량"])
#         # df_stock_5m = df_stock[(df_stock["시간"].str.contains(":.0:",regex=True)) | (df_stock["시간"].str.contains(":.5:",regex=True))].copy()
#         df_stock_10m = df_stock[(df_stock["시간"].str.contains(":.0:",regex=True))].copy()
        
#         cols = ["종목명","종목코드","이미지URL"] + df_stock_10m["시간"].tolist()
#         dataA = [ss_info["한글명"],ss_info["단축코드"],""] + df_stock_10m["주식 현재가"].tolist()
#         dataB = [ss_info["한글명"],ss_info["단축코드"],""] + df_stock_10m["누적 거래량"].tolist()
#         dataC = [ss_info["한글명"],ss_info["단축코드"],""] + df_stock_10m["누적 거래 대금"].tolist()

#         dictA = dict(zip(cols, dataA))
#         dictB = dict(zip(cols, dataB))
#         dictC = dict(zip(cols, dataC))

#         dataAList.append(dictA)
#         dataBList.append(dictB)
#         dataCList.append(dictC)

#         # break
    
#     df_flourish_a = pd.DataFrame.from_records(dataAList)
#     df_flourish_b = pd.DataFrame.from_records(dataBList)
#     df_flourish_c = pd.DataFrame.from_records(dataCList)

#     saveAFile = f"{rootPath}/{datePath}/현재가.tsv"
#     saveBFile = f"{rootPath}/{datePath}/거래량.tsv"
#     saveCFile = f"{rootPath}/{datePath}/거래대금.tsv"

#     df_flourish_a.to_csv(saveAFile,sep='\t',header=True,index=False,encoding="utf-8-sig")
#     df_flourish_b.to_csv(saveBFile,sep='\t',header=True,index=False,encoding="utf-8-sig")
#     df_flourish_c.to_csv(saveCFile,sep='\t',header=True,index=False,encoding="utf-8-sig")
    
#     return


#     # parse_stock_info(rootPath,broker)
#     # convert_flourish_format(rootPath,datePath,codeList,broker)