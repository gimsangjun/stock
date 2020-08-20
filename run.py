from discord.ext import commands
import function as f  # 내가 기존에 만든 웹스크래핑 장치들
import discord, os, asyncio  # 토큰값을 숨기기위해

bot = commands.Bot(
    command_prefix="!"
)  # prefix를 가지고있을때 명령어를 칠 때는 저 prefix가 꼭 앞에 있어야 한다.

token_path = os.path.dirname(os.path.abspath(__file__)) + "/token.txt"
t = open(r"C:\Users\kimsangjun\Documents\coding\test\token.txt", "r", encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ", token)

# game = discord.Game("!도움")
"""
# @이거는 뜻이 뭘까?
@bot.command()
async def test(
    ctx, arg
):  # ctxd의 뜻은 context 인 거 같다. 필요도 없는 상황이 있어도 될거 같은데 왜 있는 걸까? 아 예제를 만든 내가 만든 봇인가 보다.
    await ctx.send(arg)


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


def to_upper(argument):
    return argument.upper()


@bot.command()  # 이런식으로도 연계할수 있다.
async def upper(ctx, content: to_upper):
    await ctx.send(content)
"""


@bot.event
async def on_ready():
    print("봇 시작")


@bot.command()
async def 도움(ctx):
    await ctx.send("명령어 : !가격 회사명 - 현재가, 시초가 ,전일가격을 알수있습니다.")
    await ctx.send("명령어 : !종목추가 회사명 가격 갯수 - 아직 미완성입니다.")
    await ctx.send("명령어 : !종목알람추가 회사명 매수가격 매도가격 - 그 가격에 오면 매수알람,매도알람이 오게 해줍니다.")


@bot.command()
async def 종목추가(ctx, company, price, count):
    f.plus_mystock(company, price, count)


@bot.command()
async def 가격(ctx, company):  # 현재가 시초가 어제가격
    price_list = f.get_price(company)
    for company, price in price_list.items():
        message = company + " : " + price
        await ctx.send(message)


@bot.command()
async def 종목알람추가(ctx, company, buy_price, sell_price):
    f.stock_alarm(company, buy_price, sell_price)

    df = f.stock_alarm_list()
    # 이부분 수정필요.
    if company in df:
        await ctx.send("이미 존재하는 종목입니다.")
    else:
        exit(1)  # 그냥종료시켜보리기


@bot.command()
async def 알람(ctx):
    message = f.main_alarm()
    if message != 1:  # 매수가격 도달
        await ctx.send(message)


bot.run(token)
