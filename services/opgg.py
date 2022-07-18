from dataclasses import dataclass

import requests

from .utils import BaseAPIService, ChampionsData, Providers, fetch_links


@dataclass(kw_only=True, slots=True)
class OPGG(BaseAPIService):
    def _api_call(self) -> dict:
        self.params = {
            "period": "month",
            "tier": "platinum_plus",
            "position": "",
        }

        response: requests.models.Response = self.session.get(
            fetch_links[Providers.OP_GG], headers=self.headers, params=self.params
        )
        if not response:
            raise requests.HTTPError(f"Could not fetch the data from {Providers.OP_GG}")

        self.response_data = response.json()
        return self.response_data

    def _sanitize_data(self):
        self.champions_data["Provider"] = Providers.OP_GG
        self.champions_data["Role"] = "-"

        for champion in self.response_data["data"]:
            self.champions_data["ChampionId"].append(champion["champion_id"])
            self.champions_data["ChampionName"].append(
                self.champions_names[str(champion["champion_id"])]
            )
            self.champions_data["TotalGames"].append(champion["play"])
            self.champions_data["Wins"].append(champion["win"])
            self.champions_data["Losses"].append(champion["play"] - champion["win"])
            self.champions_data["Winrate"].append(
                self.calculate_winrate_percentage(
                    str, champion["win"], champion["play"]
                )
            )

        self.complete_missing_champions_data()

    def get_stats(self) -> ChampionsData:
        self._api_call()
        self._sanitize_data()

        return self.champions_data
