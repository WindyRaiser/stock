import os
import time
from itertools import product
from glob import glob

from selenium import webdriver
from selenium.webdriver.common.by import By

class MyKrx:
    def __init__(self,rootPath):
        self.rootPath = rootPath
        self.driver = webdriver.Edge()
        self.driver.implicitly_wait(10)
        self.url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0302"
        
        return

    def get_stock_info(self):
        self.driver.get(self.url)
        self.driver.find_element(By.XPATH,'//*[@id="jsMdiMenu"]/div[4]/ul/li[6]/ul/li[2]/div/div[1]/ul/li[1]/a').click()
        
        # 거래 상/하위 50종목 클릭 (거래량, 전체 기본)
        self.driver.find_element(By.XPATH,'//*[@id="jsMdiMenu"]/div[4]/ul/li[6]/ul/li[2]/div/div[1]/ul/li[1]/ul/li[2]/a').click()
        time.sleep(3)
        
        # 1일 단위로 변경
        self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[4]/td/div/div/button[2]').click()
        time.sleep(1)
        # 조회 버튼 클릭
        self.driver.find_element(By.XPATH,'//*[@id="jsSearchButton"]').click()
        time.sleep(2)

        # 다운로드
        self.driver.find_element(By.XPATH,'//*[@id="UNIT-WRAP0"]/div/p[2]/button[2]/img').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a').click()
        time.sleep(5)

        # # 코스피로 변경 (거래량, 코스피)
        # self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[1]/td/label[2]').click()
        # time.sleep(1)
        # # 조회 버튼 클릭
        # self.driver.find_element(By.XPATH,'//*[@id="jsSearchButton"]').click()
        # time.sleep(2)

        # # 다운로드
        # self.driver.find_element(By.XPATH,'//*[@id="UNIT-WRAP0"]/div/p[2]/button[2]/img').click()
        # time.sleep(2)
        # self.driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a').click()
        # time.sleep(5)

        # # 코스닥으로 변경(거래량, 코스닥)
        # self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[1]/td/label[3]').click()
        # time.sleep(1)
        # # 조회 버튼 클릭
        # self.driver.find_element(By.XPATH,'//*[@id="jsSearchButton"]').click()
        # time.sleep(2)

        # # 다운로드
        # self.driver.find_element(By.XPATH,'//*[@id="UNIT-WRAP0"]/div/p[2]/button[2]/img').click()
        # time.sleep(2)
        # self.driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a').click()
        # time.sleep(5)


        # 거래대금으로 변경 (거래대금, 코스닥)
        self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[3]/td/label[2]').click()
        time.sleep(1)
        # 전체로 변경 (거래대금, 전체)
        self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[1]/td/label[1]').click()
        time.sleep(1)
        # 조회 버튼 클릭
        self.driver.find_element(By.XPATH,'//*[@id="jsSearchButton"]').click()
        time.sleep(2)

        # 다운로드
        self.driver.find_element(By.XPATH,'//*[@id="UNIT-WRAP0"]/div/p[2]/button[2]/img').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a').click()
        time.sleep(5)

        # # 코스피로 변경 (거래대금, 코스피)
        # self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[1]/td/label[2]').click()
        # time.sleep(1)
        # # 조회 버튼 클릭
        # self.driver.find_element(By.XPATH,'//*[@id="jsSearchButton"]').click()
        # time.sleep(2)

        # # 다운로드
        # self.driver.find_element(By.XPATH,'//*[@id="UNIT-WRAP0"]/div/p[2]/button[2]/img').click()
        # time.sleep(2)
        # self.driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a').click()
        # time.sleep(5)

        # # 코스닥으로 변경(거래대금, 코스닥)
        # self.driver.find_element(By.XPATH,'//*[@id="MDCEASY016_FORM"]/div[1]/div/table/tbody/tr[1]/td/label[3]').click()
        # time.sleep(1)
        # # 조회 버튼 클릭
        # self.driver.find_element(By.XPATH,'//*[@id="jsSearchButton"]').click()
        # time.sleep(2)

        # # 다운로드
        # self.driver.find_element(By.XPATH,'//*[@id="UNIT-WRAP0"]/div/p[2]/button[2]/img').click()
        # time.sleep(2)
        # self.driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a').click()
        # time.sleep(5)

        return

    def reproduce_info(self):
        # 59분->00분으로 넘어갈 경우, 시간 오버플로우로 문제에 대한 예외가 없으니 59분 전에 작업 할 것.
        infoList = ["거래량","거래대금"]
        # marketList = ["전체","코스피","코스닥"]
        marketList = ["전체"]
        inputList = [ f"{info}_{market}" for info,market in product(infoList,marketList) ] 

        downloadFileName = f"{self.rootPath}/data_*_*.csv"
        downloadFileList = glob(downloadFileName)
        downloadFileList.sort()

        date = downloadFileList[0].split('_')[2].split('.')[0]
        newPath = f"{self.rootPath}/{date}"
        os.makedirs(newPath,exist_ok=True)

        for i, input in enumerate(inputList):
            oldFile = downloadFileList[i]
            newFile = f"{newPath}/{input}.csv"
            os.rename(oldFile,newFile)
        
        return date