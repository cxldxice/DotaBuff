import fake_useragent
import requests
import bs4

user_agent = fake_useragent.UserAgent().random


class DotaBuff(object):
    def __init__(self, player=None):
        self.player = player
        self.session = self.__new_session()

    def get_match(self, id):
        match = {}
        match_url = f"https://www.dotabuff.com/matches/{id}"

        html = self.__get_html(match_url)
        
        index = 0
        match_table = html.find_all("table", class_="match-team-table")
        for team in match_table:
            if index == 0:
                match["radiant"] = []
                team_obj = match["radiant"]
            else:
                match["dire"] = []
                team_obj = match["dire"]

            player_table = team.find("tbody").find_all("tr")
            for player in player_table:
                hero_url = self.__to_link(player.find_all("td")[0].find("a")["href"])
                hero = hero_url.replace("https://dotabuff.com/heroes/", "").replace("-", " ")
                hero = hero[0].upper() + hero[1:]
                hero_img = self.__to_link(player.find("img")["src"])
                role = player.find_all("td")[1].find("i")["title"]
                line = player.find_all("td")[2].find("i")["title"]
                line_status = player.find_all("td")[3].find("acronym", class_="lane-outcome").text

                k = self.__to_int(player.find_all("td")[5].text.replace("-", "0"))
                d = self.__to_int(player.find_all("td")[6].text.replace("-", "0"))
                a = self.__to_int(player.find_all("td")[7].text.replace("-", "0"))

                net_worth = self.__to_int(player.find_all("td")[8].text.replace("-", "0"))
                last_hit = self.__to_int(player.find_all("td")[9].text.replace("-", "0"))
                denie = self.__to_int(player.find_all("td")[11].text.replace("-", "0"))

                gpm = self.__to_int(player.find_all("td")[12].text.replace("-", "0"))
                xpm = self.__to_int(player.find_all("td")[14].text.replace("-", "0"))
                damage = self.__to_int(player.find_all("td")[15].text.replace("-", "0"))
                heal = self.__to_int( player.find_all("td")[16].text.replace("-", "0"))
                tower_damage = self.__to_int(player.find_all("td")[17].text.replace("-", "0"))
                wards_obs = self.__to_int(player.find_all("td")[18].find("span", class_="color-item-observer-ward").text.replace("-", "0"))
                wards_sentry = self.__to_int(player.find_all("td")[18].find("span", class_="color-item-sentry-ward").text.replace("-", "0"))

                items = player.find_all("td")[19].find("div", class_="player-inventory-items").find_all("div", class_="image-container")

                player_data = {
                    "hero": {
                        "name": hero,
                        "url": hero_url,
                        "image": hero_img,
                    },
                    "line": {
                        "role": role,
                        "name": line,
                        "status": line_status
                    },
                    "stats": {
                        "kills": k,
                        "deaths": d,
                        "assists": a,
                        "net_worth": net_worth,
                        "last_hit": last_hit,
                        "denie": denie,
                        "gpm": gpm,
                        "xpm": xpm,
                        "damage": damage,
                        "tower_damage": tower_damage,
                        "heal": heal
                    },
                    "wards": {
                        "observer": wards_obs,
                        "sentry": wards_sentry
                    }
                }

                player_data["items"] = {}
                player_data["items"]["inventory"] = []
                for item in items:
                    item_url = self.__to_link(item.find("a")["href"])
                    item_name = item.find("img")["title"]
                    item_image = self.__to_link(item.find("img")["src"])

                    player_data["items"]["inventory"].append({
                        "name": item_name,
                        "image": item_image,
                        "url": item_url
                    })

                try:
                    neutral_item = player.find_all("td")[19].find("div", class_="player-neutral-item").find("div", class_="image-container")
                    neutral_item_url = self.__to_link(neutral_item.find("a")["href"])
                    neutral_item_name = neutral_item.find("img")["title"]
                    neutral_item_image = self.__to_link(neutral_item.find("img")["src"])
                except:
                    neutral_item_url = None
                    neutral_item_name = None
                    neutral_item_image = None

                player_data["items"]["neutral"] = {
                    "name": neutral_item_name,
                    "image": neutral_item_image,
                    "url": neutral_item_url
                }

                team_obj.append(player_data)
                index += 1

        return match

    def __to_int(self, string: str):
        out = string

        string = string.replace(" ", "")
        try:
            return int(string)
        except:
            pass
        
        string = string.replace("k", "").replace(".", "")
        string += "00"

        try:
            return int(string)
        except:
            return out

    def __to_link(self, string: str):
        return "https://dotabuff.com" + string

    def __get_html(self, url):
        res = self.session.get(url)
        return bs4.BeautifulSoup(res.text, "html.parser")

    def __new_session(self):
        s = requests.Session()
        s.headers.update({"user-agent": user_agent})

        return s