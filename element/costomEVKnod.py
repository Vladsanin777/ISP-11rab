async def costomEVK(tyo):
#p = tyo[0]
#u = tyo[1]
#f = tyo[2]
#t = tyo[3]
c = ("Способ Евклида усложнённый\n")
match tyo[2]:
  case "Да, с формулой":
    c += (f"Формула НОД: Повторять пока (|a - b|) и b не будут равны, если они равны, то это и будет ответ \nНОД чисел: {tyo[0]} и {tyo[1]}\n")
  case "Нет, без формулы":
    c += (f"НОД чисел: {tyo[0]} и {tyo[1]}\n")
i = 0
match tyo[3]:
  case "Пошаговое":
    while tyo[0] != tyo[1]:
      w = tyo[0]
      tyo[0] = tyo[1]
      tyo[1] = abs(w - tyo[1])
      i += 1
      if tyo[0] != tyo[1]:
        c += (f"    {i}) | (|{w} - {tyo[0]}|) = {tyo[1]} неравно {tyo[1]}\n")
      else: 
        c += (f"  {i}) | (|{w} - {tyo[0]}|) = {tyo[1]} равно {tyo[0]}\n")
    c += (f"Всё  ответ готов {tyo[0]}\n")
  case "Для галочки":
    while tyo[0] != tyo[1]:
      w = tyo[0]
      tyo[0] = tyo[1]
      tyo[1] = abs(w - tyo[1])
      i += 1
      if tyo[0] != tyo[1]: 
        c += (f"    {i}) Первое {tyo[0]} Второе {tyo[1]}\n")
      else:
        c += (f"  {i}) Первое {tyo[0]} Второе {tyo[1]}\n")
    c += (f"Всё  ответ готов {tyo[0]}\n")
return c