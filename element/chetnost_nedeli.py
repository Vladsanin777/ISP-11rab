import datetime

class ChetnostNedeli:
  async def is_even_week(self):
    # Получаем текущую дату
    current_date = datetime.datetime.now() + datetime.timedelta(hours=4)
    # Создаем дату с началом сентября текущего года
    september_start = datetime.datetime(current_date.year, 9, 1)
    # Вычисляем разницу в днях между текущей датой и началом сентября
    days_diff = (current_date - september_start).days

    days_diff += september_start.weekday()

    # Вычисляем количество недель
    weeks = days_diff // 7
    if weeks % 2 == 0:
      if (current_date.weekday() == 5 and current_date.hour > 15) or current_date.weekday() == 6: return [True, True]
      else: return [True, False]
    else:
      if (current_date.weekday() == 5 and current_date.hour > 15) or current_date.weekday() == 6: return [False, True]
      else: return [False, False]