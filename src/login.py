from src.token import Token
from src.module import *


class Login(Token):
    def login(self) -> dict:
        os.system("cls||clear")
        tokenEG = self.getTokenEaag
        tokenEJ = self.getTokenEaaj
        if tokenEG != None:
            open("data/tokenEG", "a").write(tokenEG)
            open("data/tokenEJ", "a").write(tokenEJ)
            cookie = open("data/cookie.txt", "a").write(self._cookie)
        else:
            tokenEG = None
            tokenEJ = None
            cookie = None
        return {"tokenEG": tokenEG, "tokenEJ": tokenEJ, "cookie": cookie}
