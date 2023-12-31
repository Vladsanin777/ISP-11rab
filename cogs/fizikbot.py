import disnake
from disnake.ext import commands 

import os


class CMDUsers3 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")


  @commands.slash_command(
    name = "физика",
    description = "Правила по физике"
  )
  async def physics(
    ctx,
    prav = commands.Param(
      name = "правило",
      description = "Выберите правило",
      choices = [
        "1МАГНИТНОЕ ПОЛЕ",
        "1Движущиеся заряды",
        "2Магнитное вихревое поле",
        "Ампер Андре Мари",
        "3Направления силы Ампера",
        "4Основа устройства электроизмерительных приборов",
        "5Взаимодействие токов и пьезоэлектрический",
        "6Модуль силы Лоренца",
        "7Взаимодействие веществ с магнитное поле",
        "9Магнитный поток",
        "Правило Ленца",
        "10Направление индукционного тока",
        "Закон электромагнитной индукции",
        "11ЭДС",
        "12Вихревое электрическое поле",
        "14Электродинамический микрофон",
        "16Энергия магнитного поля тока"
      ]
    )
  ):
    print(prav)
    match prav:
      case "1МАГНИТНОЕ ПОЛЕ":
        await ctx.send("Неподвижные электрические заряды создают во- круг себя электрическое поле. Движущиеся заря- ды создают, кроме того, магнитное поле.")
      case "1Движущиеся заряды":
        await ctx.send("Движущиеся заряды (электриче- ский ток) создают магнитное поле. Вокруг любых направленно дви- жущихся зарядов возникает маг- нитное поле. Оно также появляется в случае, если в пространстве суще- ствует электрическое поле, изме- няющееся со временем. Обнаруживается магнитное поле по действию на электрический ток.")
      case "2Магнитное вихревое поле":
         await ctx.send("Магнитное вихревое поле, в каждой точке поля вектор магнитной индукции имеет определенное направле- ние. Это направление указывает магнитная стрелка или его можно определить по правилу буравчика. Магнитное поле не имеет источников; магнитных зарядов в природе не су- ществует.")
      case "Ампер Андре Мари":
        await ctx.send("Ампер Андре Мари (1775—1836) -великий французский физик и математик, один из основоположников электродинамики. Ввел в физику понятие «электрический ток» и разработал первую теорию магнетизма, основанную на гипотезе молекулярных токов, открыл механическое взаимодействие электрических токов и установил количественные соотношения для силы этого взаимодействия. Назван Максвеллом «Ньютон электричества». Работал также в области механики, теории вероятностей и математического анализа.")
      case "Закон Ампера":
        await ctx.send("F= I|B| Al sin α\nЭто выражение называют законом Ампера. Сила Ампера равна произведению модуля силы тока, век-Мора магнитной индукции, длины отрезка проводника и синуса угла между направлениями векторов магнитной индукции и тока.")
      case "3Направления силы Ампера":
        await ctx.send("Измеряя силу, действующую со стороны магнитного поля на участок проводника с током, можно определить модуль вектора магнитной индукции. Сформулирован закон Ампера для силы, действующей на участок проводни- ка с током в магнитном поле.")
      case "4Основа устройства электроизмерительных приборов":
        await ctx.send("В основе устройства электроизмерительных приборов магнитоэлектрической системы лежит действие магнитного поля на рамку с током.")
      case "5Взаимодействие токов и пьезоэлектрический":
        await ctx.send("Взаимодействие токов и пьезоэлектрический эффект по- ложены в основу принципа работы современных громкого- ворителей.")
      case "Модуль силы Лоренца":
        await ctx.send("Силу, действующую на движущуюся заряженную части- цу со стороны магнитного поля, называют силой Лоренца в честь великого голландского физика Х. Лоренца (1853- 1928) - основателя электронной теории строения вещест ва. Сиду Лоренца можно найти с помощью закона Ампера. Модуль силы Лоренца равен отношению модуля силы Г. действующей на участок проводника длиной М, к числу заряженных частиц, упорядоченно движущихся в этомучастке проводника:\nFл = F\n     N\nРассмотрим отрезок тонкого прямого проводника сто. Пусть длина отрезка М и площадь по ного сечения проводника 8 настолько малы, что вектор индукции магнитного поля В можно считать одинако в пределах этого отрезка проводника. Сила тока / в про водник связана с зарядом час 4.концентрацией заряжен вых частиц (числом зарядов в единице объема) и скоростью их упорядоченного движения следующей формулой:\nI = qnvS\nМодуль силы, действующей со стороны магнитного поля на выбранный элемент тока, равен:\nF = |I|BAL sin α\nПодставляя в эту формулу выражение I = qnvS для силы тока, получаем:\nF = q nvSAIB sin a = v|q|NB sin α\nгде N = n*S*Delta*I число заряженных частиц в рассматривае мом объеме. Следовательно, на каждый движущийся ряд со стороны магнитного поля действует сила Лоренца,равная:\nFл = F = |q|uB sin α,\n     N/nгде угол между вектором скорости и вектором магнит ной индукции. Сила Лоренца перпендикулярна векторам B и u. Ее направление определяется с помощью того же правила левой руки, что и направление силы Ампера: если ле вую руку расположить так, чтобы составляющая магнитной индукции, перпендикулярная скорости заряда, входила в ладонь, а четыре вытянутых пальца были направлены по движению положительного заряда (против движения отрица тельного), то отогнутый на 90° большой палец укажет направ ление действующей на заряд силы Лоренца Ру (рис. 1.24). Электрическое поле действует на заряд у с силой Лоренса")
      case "7Взаимодействие веществ с магнитное поле":
        await ctx.send("Все вещества, помещенные в магнитное поле, создают собственное поле. Наиболее сильные поля создают ферро- магнетики. Из них делают постоянные магниты, так как поле ферромагнетика не исчезает после выключения на- магничивающего поля. Ферромагнетики широко применя- ются на практике.")
      case "8Магнитная индукция":
        await ctx.send("В проводящем замкнутом контуре возникает электрический ток, если контур находится в переменном магнитном поле так, что число линий магнитной индукции, пронизы-поле или движется в постоянном во времени магнитном вающих контур, меняется.")
      case "9Магнитный поток":
        await ctx.send("Ф = B(n-sq)S\nМагнитный поток зависит от ориентации поверхности, которую пронизывает магнитное поле.")
      case "Правило Ленца":
        await ctx.send("Согласно правилу Ленца возникающий в замкнутом контуре индукционный ток своим магнитным по- лем противодействует тому изменению магнит- ного потока, которым он вызван.")
      case "10Направление индукционного тока":
        await ctx.send("Направление индукционного тока определяется с помо- щью закона сохранения энергии. Индукционный ток во всех случаях направлен так, чтобы своим магнитным по- лем препятствовать изменению магнитного потока, вызы- вающего данный индукционный ток.")
      case "Закон электромагнитной индукции":
        await ctx.send("Согласно закону электромагнитной индукции ЭДС индукции в замкнутом контуре равна по модулю скорости изменения магнитного потока через по- верхность, ограниченную контуром:")
      case "11ЭДС":
        await ctx.send("ЭДС индукции определяется скоростью изменения маг- нитного потока.")
      case "12Вихревое электрическое поле":
        await ctx.send("Наряду с потенциальным кулоновским электрическим полем существует вихревое электрическое поле. Линии на- пряженности этого поля замкнуты. Вихревое поле порож дается меняющимся магнитным полем.")
      case "13ЭДС индукции в движушихся проводниках":
        await ctx.send("ЭДС индукции в проводниках, движущихся в постоян ном магнитном поле, возникает за счет действия на заряды проводника силы Лоренца.")
      case "14Электродинамический микрофон":
        await ctx.send("В громкоговорителе сила Ампера вызывает колебания катушки и связанной с ней диафрагмы. В микрофоне колебания диафрагмы передаются под- вижной катушке, и в ней возникает индукционный ток.")
      case "15Самоиндукция индуктивность":
        await ctx.send("При изменении силы тока в проводнике в нем возникает вихревое электрическое поле. Это поле тормозит электроны при возрастании силы тока и ускоряет при убывании.")
      case "16Энергия магнитного поля тока":
        await ctx.send("Магнитное поле, созданное электрическим током, обла- дает энергией, прямо пропорциональной квадрату силы тока.")
      case "":
        await ctx.send("")
      case "":
        await ctx.send("")
      case "":
        await ctx.send("")
      case "":
        await ctx.send("")
      case "":
        await ctx.send("")
      case "":
        await ctx.send("")
      case "":
        await ctx.send("")

def setup(bot):
  bot.add_cog(CMDUsers3 (bot))