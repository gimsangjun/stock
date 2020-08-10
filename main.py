import requests  # 크롤링하려는 웹페이지의 정보를 받아오기위해
from bs4 import BeautifulSoup  # 받아온 웹페이지의 정보를 다루기위해
import pandas as pd  # 엑셀 데이터(종목코드를)를 다루기 위해서
import openpyxl  #  엑셀(저장하기위해서)을 다루기위해서

# 내가 검색하고싶은 종목의 코드를 가져옴.
def get_company_code(company):

    df = pd.read_excel(
        r"C:\Users\kimsangjun\Documents\coding\test\all_stock.xlsx", dtype={"종목코드": str}
    )  # https://hogni.tistory.com/52 컬럼의 데이터타입 지정하기(불러올 때 부터 지정해놔여됨.), 0이 빠진것을 넣어줌.
    df = df[["회사명", "종목코드"]]  # https://wendys.tistory.com/173
    # print(df.index) #인덱스가 0 1 2 3 4 5 가나옴, 하지만 나는 인덱스가 회사명이었으면 좋겠음.
    df = df.set_index("회사명")  # 인덱스를 회사명으로 바꿈
    company_code = df.loc[company:company, ["종목코드"]]
    company_code = company_code.iloc[0, 0]
    return company_code


# 내가보고싶어하는 종목의 웹페이지 소스코드를 받아옴.
def get_bs_obj(company_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code
    result = requests.get(
        url
    )  # url에 요청을 보냈고 성공적으로 응답을 받았으면 Response [200] 돌려준다. 바로 쓸수 있는 상태가 아니다. bs을 통해 쓸수있는 객체로 저장
    bs_obj = BeautifulSoup(
        result.content, "html.parser"
    )  # 웹페이지에 요청한뒤,여기서  받아낸 문서를 .content로 지정 후 BeautifulSoup를 통해 soup에 객체로 저장. 뒤에 html은 옵션이라고 한다.
    # BeautifulSoup(문자열, 'html.parser') 라고 하면 "이 문자열은 단순한 텍스트가 아니라 html 구조에 맞게 작성되어있어. 그러니 너도 html 의 관점에서 이 문자열을 이해해줘" 라고 하는 것과 동일합니다.
    return bs_obj


# 내가받아온 웹페이즈 소스코드중에서 내가 가져와야할 가격을 가져옴
def get_price(company_code):

    # 현재가격
    bs_obj = get_bs_obj(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    now_price = no_today.find("span", {"class": "blind"}).text

    # 시가
    today = bs_obj.find_all("td", {"class": "first"})
    today = today[1]
    today_price = today.find("span", {"class": "blind"}).text

    # 전일가격
    yesterday = bs_obj.find("td", {"class": "first"})
    yesterday_price = yesterday.find("span", {"class": "blind"}).text

    return {
        "now_price": now_price,
        "today_price": today_price,
        "yesterday_price": yesterday_price,
    }


# 내가 추가할려는 종목의 이름이 있는지 확인 하는 과정임.
def stock_exist(company):
    df = pd.read_excel(
        r"C:\Users\kimsangjun\Documents\coding\test\all_stock.xlsx", dtype={"종목코드": str}
    )  # 엑셀파일불러오기
    df = df.loc[:, ["회사명"]]
    # df = df.set_index("회사명")
    df = df.values.tolist()  # if문을 활용하기 위해 list으로 데이터를 바꿔줬음.
    # print(df)
    if [company] in df:
        print("존재하는 종목입니다.")
    else:
        print("존재하지 않는 종목입니다. 다시 실행시켜주시기 바랍니다.")
        exit(1)  # 그냥종료시켜보리기


# 전일대비 얼마나 올랐나,생각해보니 이거는 만들필요가 없었음. 현재가격이랑 전일가격만 있으면 그냥 계산할수있는거였음. 얻을수 있는 교훈 어떻게 만들지 먼저 생각을 해야한다.

"""
company = input("알고 싶어하는 종목의 이름을 적어주세요\n")
company_code = get_company_code(company)

filename = "my_stock.xlsx" #내가 열 파일이름을 저장.
book = openpyxl.load_workbook(filename) # 파일을 불러옴. 엑셀파일 열기까지의 과정임.
sheet = book.worksheets[0] # 맨 앞의 시트 추출하기

# sheet = wb.active # 활성화된 시트를 새로운 변수에 할당합니다.

print(company_code)
print(get_price(company_code))
"""
company = input("추가하고싶은 종목의 이름을 넣어주세요\n")
stock_exist(company)

price = input("가격을 입력해주세요\n")
count = input("갯수를 입력해주세요\n")
total_price = int(price) * int(count)

filename = r"C:\Users\kimsangjun\Documents\coding\test\my_stock.xlsx"
wb = openpyxl.load_workbook(filename)
sheet = wb.active
sheet.append(
    [company, price, count, total_price]
)  # append() takes 2 positional arguments but 4 were given
wb.save(filename)

