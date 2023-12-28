import asyncio
from openai import AsyncOpenAI
import os
import textwrap
import TOKEN

class gpt():
  async def join_arguments_by_length_limit(self, args, limit):
    result = []
    res = []
    current_length = 0

    for arg in args:
      # Check if the argument itself exceeds the limit
      if len(arg) > limit:
        # Reset current_length and append the previous accumulated args (res) to the result
        current_length = 0
        if res:
          result.append('\n'.join(res))
          res = []

          # Split the argument into chunks of length 'limit' and add to the result
        result += [arg[i:i + limit] for i in range(0, len(arg), limit)]
      # Check if adding the argument exceeds the limit
      elif current_length + len(arg) > limit:
        # Append the accumulated args (res) to the result and start a new list for the current argument
        result.append('\n'.join(res))
        res = [arg]
        current_length = len(arg)
      else:
        # Add the argument to the current accumulation of args
        res.append(arg)
        current_length += len(arg)

    # Append any remaining accumulated arguments (res) to the result
    if res:
      result.append('\n'.join(res))

    # Filter and return non-empty strings from the result
    result_filtered = []
    for r in result:
      if r != None or r != "":
        result_filtered.append(r)
    return result_filtered





  async def gpt(self, message_gpt, size):
    self.api_key = TOKEN.OPENAI_API_KEY
    self.client = AsyncOpenAI(api_key=self.api_key)
    response_gpt = await self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": message_gpt
        },
      ],
    )

    if response_gpt is not None:
      response_gpt = response_gpt.choices[0].message.content
      response_gpt = response_gpt.split("\n")
      print(response_gpt)
      response_gpt = await asyncio.gather(self.join_arguments_by_length_limit(response_gpt, size))
      response_gpt = response_gpt[0]
      print(response_gpt)
      response_gpt.insert(0, message_gpt)
      print(response_gpt)
      # ... (remaining code)
    else:
      # Handle the case when response_gpt is None
      return "GPT не ответил"
    # ... (remaining code)
    return response_gpt