import os
import asyncio
from src.menu import Main
from src.login import Login


async def deleteCache():
    try:os.remove('src/__pycache__')
    except:pass
    
async def mkdir():
    try:
        os.mkdir("data")
    except:
        pass
    try:
        os.mkdir("hasil")
    except:
        pass

    await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(mkdir())
    task2 = asyncio.create_task(deleteCache())
    
    await asyncio.gather(task1, task2)

    try:
        tokenEJ = open("data/tokenEJ", "r").read()
        tokenEG = open("data/tokenEG", "r").read()
        cookie = open("data/cookie.txt", "r").read()
    except:
        print(
            """
              Silahkan Login terlebih Dahulu!
                Untuk Masuk ke Menu.
            """
        )

        cookie = input(">> Cookie tumbal: ")
        data = Login(cookie=cookie).login()
        tokenEG = data["tokenEG"]
        tokenEJ = data["tokenEJ"]
        cookie = data["cookie"]

        if tokenEG == None:
            exit(" Cookie Invalid ")
        else:
            exit(" Login Berhasil! Silahkan jalankan ulang Script.")

    app = Main(tokenEJ=tokenEJ, tokenEG=tokenEG, cookie=cookie)

    app.MainMenu()


if __name__ == "__main__":
    asyncio.run(main())
