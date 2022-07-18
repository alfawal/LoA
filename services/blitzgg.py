from dataclasses import dataclass

import requests

from .utils import BaseAPIService, ChampionsData, Providers, fetch_links


@dataclass(kw_only=True, slots=True)
class Blitz(BaseAPIService):
    def _api_call(self) -> dict:
        self.params = "query=query%20TierList%28%24region%3ARegion%2C%24queue%3AQueue%2C%24tier%3ATier%29%7BallChampionStats%28region%3A%24region%2Cqueue%3A%24queue%2Ctier%3A%24tier%2CmostPopular%3Atrue%29%7BchampionId%20role%20patch%20wins%20games%20tierListTier%7BtierRank%20previousTierRank%20status%7D%7D%7D&variables=%7B%22queue%22%3A%22RANKED_SOLO_5X5%22%2C%22region%22%3A%22WORLD%22%2C%22tier%22%3A%22PLATINUM_PLUS%22%7D"

        response: requests.models.Response = self.session.get(
            fetch_links[Providers.BLITZ_GG], headers=self.headers, params=self.params
        )
        if not response:
            raise requests.HTTPError(
                f"Could not fetch the data from {Providers.BLITZ_GG}"
            )

        self.response_data = response.json()
        return self.response_data

    def _sanitize_data(self):
        self.champions_data["Provider"] = Providers.BLITZ_GG
        for champion in self.response_data["data"]["allChampionStats"]:
            self.champions_data["ChampionId"].append(champion["championId"])
            self.champions_data["ChampionName"].append(
                self.champions_names[str(champion["championId"])]
            )
            self.champions_data["Role"].append(
                champion["role"].upper()
                if "adc" in champion["role"].lower()
                else champion["role"].title()
            )
            self.champions_data["TotalGames"].append(champion["games"])
            self.champions_data["Wins"].append(champion["wins"])
            self.champions_data["Losses"].append(champion["games"] - champion["wins"])
            self.champions_data["Winrate"].append(
                self.calculate_winrate_percentage(
                    str, champion["wins"], champion["games"]
                )
            )

        self.complete_missing_champions_data()

    def get_stats(self) -> ChampionsData:
        self._api_call()
        self._sanitize_data()

        return self.champions_data
