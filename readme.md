# 한국투자 API 활용 거래대금/거래량 Top30 출력 프로그램

## 사용법

1. config.toml에 한국투자 API(https://apiportal.koreainvestment.com/intro)에서 회원가입 
2. 한투 API key, secret, account 입력
```
[hantoo]
key = "api키"
secret = "고유값"
account = "계좌번호"

[path]
root = "파일 다운로드 경로"
output = "프로그램 실행 결과 경로"
```

3. python 라이브러리 설치

```
pip install mojito2
pip install numpy pandas tomlkit, selenium
```

4. main 프로그램 실행

```
python main.py 아무말 - 단일 실행
python main.py auto - 자동 워크플로우
```

---

## 프로그램 설명

   1. 한국거래소 정보데이터시스템(http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0302)에서 거래량 상하위 50종목에 대해 확인 가능하다.
   2. 위 자료를 excel 파일로 다운로드 받는다.
   3. 위 과정을 selenium crawling을 통해 자동화 작업한다.
   4. mojito 프로그램을 통해 한국투자API를 활용하여 top50 중 한 종목에 대한 실시간 거래량 및 거래금액을 확인이 가능하다.
   5. 분단위로 실시간 데이터를 excel파일로 생성한 후, 프로그램 종료한다.

---

## 한계
 - 데이터 시각화 추가가 필요

