from src.module import *


class Dump(object):
    def __init__(
        self,
        cookie: str = None,
        tokenEG: str = None,
        tokenEJ: str = None,
        url: str = "graph.facebook.com",
    ):
        self._url = url
        self.__tokenEG = tokenEG
        self.__tokenEJ = tokenEJ
        self._cookie = {"cookie": cookie}
        self.__data = []

    def dumpAccount(self, uid: str = None, choice: str = None) -> list:
        with requests.Session() as Session:
            if choice == "friends":
                r = Session.get(
                    f"https://{self._url}/{uid}?fields=friends.fields(name,id)&access_token={self._Dump__tokenEJ}",
                    cookies=self._cookie,
                ).json()["friends"]
            elif choice == "subscribers":
                r = Session.get(
                    f"https://{self._url}/{uid}?fields=subscribers.limit(5000)&access_token={self._Dump__tokenEG}",
                    cookies=self._cookie,
                ).json()["subscribers"]
            for x in r["data"]:
                uid, name = x["id"], x["name"]
                self._Dump__data.append(uid + "|" + name)
        return self._Dump__data

    def cekAccount(self, uid: str = None) -> dict:
        data = {}
        with requests.Session() as Session:
            try:
                r = Session.get(
                    f"https://{self._url}/{uid}?fields={'name,id,birthday' if uid == 'me' else 'name,id'}&access_token={self._Dump__tokenEG}",
                    cookies=self._cookie,
                ).json()
                uid, name = r["id"], r["name"]
                try:
                    birthday = r["birthday"]
                except:
                    birthday = None
            except:
                uid = None
                name = None
                birthday = None
            data.update({"uid": uid, "name": name, "birthday": birthday})
        return data
