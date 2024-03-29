async def EVK(tyo):
  #p = tyo[0]
  #u = tyo[1]
  #f = tyo[2]
  #t = tyo[3]
  c = ("Способ Евклида\n")
  match tyo[2]:
    case "Да, с формулой":
      c += (f"Формула НОД: НОД (a, b) = НОД (b, с), где с — остаток от деления a на b.\n Алгоритм Евклида заключается в следующем: если большее из двух чисел делится на меньшее — наименьшее число и будет их наибольшим общим делителем. Использовать метод Евклида можно легко по формуле нахождения наибольшего общего делителя.\nНОД чисел: {tyo[0]} и {tyo[1]}\n")
    case "Нет, без формулы":
      c += (f"НОД чисел: {tyo[0]} и {tyo[1]}\n")
  match tyo[3]:
    case "Пошаговое":
      i = 0
      if tyo[0] < tyo[1]:
        w = tyo[0]
        tyo[0] = tyo[1]
        tyo[1] = w
        i += 1
        c += (f"  {i})   Меняем числа местами\n")
      while tyo[0] % tyo[1] != 0:
        t = tyo[0]
        iou = tyo[1]
        tyo[1] = tyo[0] % tyo[1]
        tyo[0] = iou
        i += 1
        if tyo[0] % tyo[1] != 0:
          c += (f"    {i}) Оскаток от деления {t} на {tyo[0]} = {tyo[1]}\n")
        else:
          c += (f"  {i}) Оскаток от деления {t} на {tyo[0]} = {tyo[1]}\n")
      c += (f"Всё ответ готов {tyo[1]}\n")
    case "Для галочки":
      i = 0
      if tyo[0] < tyo[1]:
        w = tyo[0]
        tyo[0] = tyo[1]
        tyo[1] = w
        c += (f"  {i}) Меняем числа местами\n")
      while tyo[0] % tyo[1] != 0:
        iou = tyo[1]
        tyo[1] = tyo[0] % tyo[1]
        tyo[0] = iou
        if tyo[0] % tyo[1] != 0:
          c += (f"    {i}) Первое {tyo[0]} Второе{tyo[1]}\n")
        else :
          c += (f"  {i}) Первое {tyo[0]} Второе{tyo[1]}\n")
      c += (f"Всё ответ готов {tyo[1]}\n")
  return c