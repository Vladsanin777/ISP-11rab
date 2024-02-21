import asyncio
from cryptography.fernet import Fernet
class Code():
    async def generator_key(self):
        return Fernet.generate_key()

    async def encode_1(self, *, value):
        key = await self.generator_key()  # Generate key before encryption
        value_bytes = value.encode()  # Encode text to bytes before encryption
        return Fernet(key).encrypt(value_bytes), key

    async def decode_1(self, *, value, key):
        #value_bytes = value.encode()  # Encode text to bytes before decryption
        return Fernet(key).decrypt(value).decode()  # Decode result back to text
  
async def main():
    while True:
        run = input("Введите действие: ")
        match run:
            case "-en":
                value_to_encrypt = input("Текст который надо зашивровать: ")
                value, key = await Code().encode_1(value=value_to_encrypt)
                print(f"Зашифрованный текст: {value}\nКлюч: {key.decode()}")  # Decode key for display
            case "-de":
                value_to_decrypt = input("Текст который надо расзашивровать: ")
                key = input("Введите ключь для расшифровки: ").encode()  # Encode key before decryption
                print(await Code().decode_1(value=value_to_decrypt, key=key))
            case _:
                print("Такого действия нет")

asyncio.run(main())  # Run the main coroutine using asyncio.run()