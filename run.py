from discord.ext import commands
import function as f  # 내가 기존에 만든 웹스크래핑 장치들

bot = commands.Bot(
    command_prefix="!"
)  # prefix를 가지고있을때 명령어를 칠 때는 저 prefix가 꼭 앞에 있어야 한다.

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


@bot.command()
async def 종목추가(ctx, company, price, count):
    f.plus_mystock(company, price, count)


@bot.command()
async def 가격(ctx, company):  # 현재가 시초가 어제가격
    company_code = f.get_company_code(company)
    price_list = f.get_price(company_code)
    await ctx.send(price_list)


bot.run("")
