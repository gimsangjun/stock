import requests  # 크롤링하려는 웹페이지의 정보를 받아오기위해
from bs4 import BeautifulSoup  # 받아온 웹페이지의 정보를 다루기위해
import pandas as pd  # 엑셀 데이터(종목코드를)를 다루기 위해서
import openpyxl  #  엑셀(저장하기위해서)을 다루기위해서

# 내가 검색하고싶은 종목의 코드를 가져옴.
def get_company_code(company):

    df = pd.read_excel(
        r"C:\Users\kimsangjun\Documents\coding\test\all_stock.xlsx",
        dtype={"종목코드": str},
    )  # https://hogni.tistory.com/52 컬럼의 데이터타입 지정하기(불러올 때 부터 지정해놔여됨.), 0이 빠진것을 넣어줌.
    df = df[["회사명", "종목코드"]]  # https://wendys.tistory.com/173
    # print(df.index) #인덱스가 0 1 2 3 4 5 가나옴, 하지만 나는 인덱스가 회사명이었으면 좋겠음.
    df = df.set_index("회사명")  # 인덱스를 회사명으로 바꿈
    company_code = df.loc[company:company, ["종목코드"]]
    company_code = company_code.iloc[0, 0]
    return company_code


# 내가보고싶어하는 종목의 웹페이지 소스코드를 받아옴.
def get_bs_obj(company_code):
    url = r"https://finance.naver.com/item/main.nhn?code=" + company_code
    result = requests.get(
        url
    )  # url에 요청을 보냈고 성공적으로 응답을 받았으면 Response [200] 돌려준다. 바로 쓸수 있는 상태가 아니다. bs을 통해 쓸수있는 객체로 저장
    bs_obj = BeautifulSoup(
        result.content, "html.parser"
    )  # 웹페이지에 요청한뒤,여기서  받아낸 문서를 .content로 지정 후 BeautifulSoup를 통해 soup에 객체로 저장. 뒤에 html은 옵션이라고 한다.
    # BeautifulSoup(문자열, 'html.parser') 라고 하면 "이 문자열은 단순한 텍스트가 아니라 html 구조에 맞게 작성되어있어. 그러니 너도 html 의 관점에서 이 문자열을 이해해줘" 라고 하는 것과 동일합니다.
    return bs_obj


# 내가받아온 웹페이즈 소스코드중에서 내가 가져와야할 가격을 가져옴
def get_price(company):

    company_code = get_company_code(company)
    # 현재가격
    bs_obj = get_bs_obj(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    now_price = no_today.find("span", {"class": "blind"}).text
    now_price = now_price.replace(",", "")

    # 시가
    today = bs_obj.find_all("td", {"class": "first"})
    today = today[1]
    today_price = today.find("span", {"class": "blind"}).text
    today_price = today_price.replace(",", "")

    # 전일가격
    yesterday = bs_obj.find("td", {"class": "first"})
    yesterday_price = yesterday.find("span", {"class": "blind"}).text
    yesterday_price = yesterday_price.replace(",", "")

    return {
        "현재가": now_price,
        "시초가": today_price,
        "전일가": yesterday_price,
    }


# 내가 추가할려는 종목의 이름이 있는지 확인 하는 과정임.
def stock_exist(company):
    df = pd.read_excel(
        r"C:\Users\kimsangjun\Documents\coding\test\all_stock.xlsx",
        dtype={"종목코드": str},
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


# 내 주식에 종목추가하기 , 이미 존재하는 종목이면 수정 할수 있는 기능.
def plus_mystock(company, price, count):

    stock_exist(company)
    total_price = int(price) * int(count)
    filename = r"C:\Users\kimsangjun\Documents\coding\test\my_stock.xlsx"
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    sheet.append(
        [company, price, count, total_price]
    )  # append() takes 2 positional arguments but 4 were given
    wb.save(filename)


# 어떤 가격에 도달하면 알람을 주는지 추가
# stock_alarm실행중, 이미 존재하는 종목을 추가하는 경우. 이대로 추가할것인지 , 수정할것인지 물어보는 기능을 넣어보는게 좋을듯.
def stock_alarm(company, buy_price, sell_price):
    stock_exist(company)
    filename = r"C:\Users\kimsangjun\Documents\coding\test\alarm.xlsx"
    gp = get_price(company)  # 가격을 불러옴/
    now_price = gp[1]  # gp[1]에 해당하는게 현재가격이기 때문에 이런식으로 해줬음.
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    sheet.append([company, now_price, buy_price, sell_price])
    wb.save(filename)


def main_alarm():

    df = pd.read_excel(
        r"C:\Users\kimsangjun\Documents\coding\test\alarm.xlsx",
        dtype={"현재가격": int, "매수가격알림": int, "매도가격알림": int},
    )

    # 어떻게 엑셀을 불러와서 현재가격을 계속초기화할 생각을 하고있엇는데 그렇게 할 필요가 없을거 같음. 실시간으로 현재가격을 가져와야하기때문에, 엑셀에 현재가격을 표시할 이유가 없을듯.

    lists = df.values.tolist()
    message = []
    for i in range(len(lists)):  # list : [회사명,현재가격,매수가,매도가]
        company = lists[i][0]  # 회사명 할당
        price = get_price(company)  # 현재가격 할당
        now_price = price["현재가"]  # get_price가 딕셔너리형태로 반환을 해주기 떄문
        now_price = int(now_price)  # 딕셔너리형태라 그런지 str으로 되어있어서 int형으로 바꿔줌.
        # 계속 현대차 오류나길래 봣더니 엑셀안에서는 현대자동차로 되어있음.

        if int(now_price) == lists[i][2]:
            # print(list[0] + " 이/가 " + str(now_price) + "원(매수 가격)에 도달하였습니다.")
            mes = company + " 이/가 " + str(now_price) + "원(매수 가격)에 도달하였습니다."
            message.append(mes)
        elif int(now_price) == lists[i][3]:
            # print(list[0] + " 이/가 " + str(now_price) + "원(매도 가격)에 도달하였습니다.")
            mes = company + " 이/가 " + str(now_price) + "원(매도 가격)에 도달하였습니다."
            message.append(mes)
    return message


# message = [] 이렇게 선언하고, 바로 message[0] = 123 이런식으로 할당할려고 했는데 자꾸 아웃오브 인덱싱 오류가떠서 append로 하니 해결댐.
# 그리고 미리 message = [1,2,3] 이런식으로 선언하고, message[0]이런식으로 하니까 되긴함. , [] 이렇게 선언했을댸 인덱스가 아무것도 없어서 그런가봄.


# 전일대비 얼마나 올랐나,생각해보니 이거는 만들필요가 없었음. 현재가격이랑 전일가격만 있으면 그냥 계산할수있는거였음. 얻을수 있는 교훈 어떻게 만들지 먼저 생각을 해야한다.
print(main_alarm())
