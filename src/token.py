from src.module import *


class Token(object):
    def __init__(self, cookie: str):
        self._cookie = cookie

    @property
    def getTokenEaag(self) -> str:
        try:
            # convert cookies to token
            cookies = {"cookie": self._cookie}
            res = requests.Session().get(
                "https://business.facebook.com/business_locations",
                headers={
                    "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
                    "referer": "https://www.facebook.com/",
                    "host": "business.facebook.com",
                    "origin": "https://business.facebook.com",
                    "upgrade-insecure-requests": "1",
                    "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                    "cache-control": "max-age=0",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "content-type": "text/html; charset=utf-8",
                },
                cookies=cookies,
            )
            token = re.search("(EAAG\w+)", str(res.text)).group(1)
        except:
            token = None
        finally:
            return token

    @property
    def getTokenEaaj(self) -> str:
        try:
            cookie = {"cookie": self._cookie}
            apk = "661587963994814|ffe07cc864fd1dc8fe386229dcb7a05e"
            data = {"access_token": apk, "scope": ""}
            req = (
                requests.Session()
                .post("https://graph.facebook.com/v16.0/device/login/", data=data)
                .json()
            )
            cd = req["code"]
            ucd = req["user_code"]
            url = (
                "https://graph.facebook.com/v16.0/device/login_status?method=post&code=%s&access_token=%s"
                % (cd, apk)
            )
            req = BeautifulSoup(
                requests.Session()
                .get("https://mbasic.facebook.com/device", cookies=cookie)
                .content,
                "html.parser",
            )
            raq = req.find("form", {"method": "post"})
            dat = {
                "jazoest": re.search(
                    'name="jazoest" type="hidden" value="(.*?)"', str(raq)
                ).group(1),
                "fb_dtsg": re.search(
                    'name="fb_dtsg" type="hidden" value="(.*?)"', str(req)
                ).group(1),
                "qr": "0",
                "user_code": ucd,
            }
            rel = "https://mbasic.facebook.com" + raq["action"]
            pos = BeautifulSoup(
                requests.Session().post(rel, data=dat, cookies=cookie).content,
                "html.parser",
            )
            dat = {}
            raq = pos.find("form", {"method": "post"})
            for x in raq("input", {"value": True}):
                try:
                    if x["name"] == "__CANCEL__":
                        pass
                    else:
                        dat.update({x["name"]: x["value"]})
                except:
                    pass
            rel = "https://mbasic.facebook.com" + raq["action"]
            pos = BeautifulSoup(
                requests.Session().post(rel, data=dat, cookies=cookie).content,
                "html.parser",
            )
            req = requests.Session().get(url, cookies=cookie).json()
            token = req["access_token"]
        except:
            token = None
        finally:
            return token
