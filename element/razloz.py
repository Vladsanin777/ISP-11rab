async def rapk(p, lk = None):
  p = int(p)
  pi = (f"Разложим число {p}:")
  op = []
  hj = 0
  c = 1
  i = 2
  while p != 1:
    if p % i == 0:
      poi = int(p / i)
      p = poi
      op.append(i)
      match hj:
        case 0:
          hj += 1
          pi += (f"  {i}")
        case _:
          pi += (f", {i}")
      c += 1
      i = 2
    else:
      i += 1
  match lk:
    case None:
      return pi, op
    case _:
      return pi