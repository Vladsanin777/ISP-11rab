import element.razloz


async def tradid(tyo):
  #p = tyo[0]
  #u = tyo[1]
  #f = tyo[2]
  #t = tyo[3]
  c = ("Традиционный способ\n")
  match tyo[2]:
    case "Да, с формулой":
      c += (f"Формула Нод: Разложить дава числа на простые множители, выбрать одинаковые простые множители и перемножить их.\nНОД {tyo[0]} и {tyo[1]}:\n")
    case "Нет, без формулы":
      c += (f"НОД {tyo[0]} и {tyo[1]}:\n")
  op = await element.razloz.rapk(tyo[0])
  ou = await element.razloz.rapk(tyo[1])
  tp = op[1]
  lp = op[0]
  tu = ou[1]
  lu = ou[0]




  if len(tp) < len(tu):
    lkop = tp
    tp = tu
    tu = lkop
  ly = (f"Общие простые множители чисел {tyo[0]} и {tyo[1]}:\n")
  a = []
  kgh = 0
  for i in tp:
    fgh = -1
    for j in tu:
      fgh += 1
      if i == j:
        tp.remove(i)
        tu.insert(fgh, j)
        a.append(i)
        if kgh == 0:
          kgh += 1
          ly += (f"{i}")
          break
        else:
          ly += (f" + {i}")
          break
  lo = 1
  for qwerty in a:
    lo = lo * qwerty
  c += f"{lp}\n{lu}\n{ly} = {lo}"
  return c

