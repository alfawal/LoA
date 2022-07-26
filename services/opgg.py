from dataclasses import dataclass

import requests
from colorama import Fore
from .utils import BaseAPIService, ChampionsData, Providers


@dataclass(kw_only=True, slots=True)
class OPGG(BaseAPIService):
    def _api_call(self) -> dict:
        self.params = {
            "period": "month",
            "tier": "platinum_plus",
            "position": "",
        }

        response: requests.models.Response = self.session.get(
            Providers.fetch_links[Providers.OP_GG],
            headers=self.headers,
            params=self.params,
        )

        print(
            f"\t\N{black question mark ornament}{Fore.LIGHTCYAN_EX} Checking for the response validation..."
        )
        if not response:
            raise requests.HTTPError(f"Could not fetch the data from {Providers.OP_GG}")

        self.response_data = response.json()
        print(
            f"\t\t{Fore.LIGHTGREEN_EX}\N{check mark} Response code and data are valid!"
        )
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
                    float, champion["win"], champion["play"]
                )
            )

        self.complete_missing_champions_data()

    def get_stats(self) -> ChampionsData:
        print(f"\N{telephone receiver} Calling the {Providers.OP_GG} API...")
        self._api_call()
        # print(f"{Fore.LIGHTGREEN_EX} Done!")

        print(f"\N{lotion bottle} Sanitizing the received data...")
        self._sanitize_data()

        return self.champions_data
