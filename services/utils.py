import json
import os
from dataclasses import dataclass, field
from typing import TypedDict

import inflect
import requests
from colorama import Fore


class Providers:
    OP_GG = "OP.GG"
    # U_GG = "U.GG"
    BLITZ_GG = "BLITZ.GG"

    fetch_links: dict[str, str] = {
        OP_GG: "https://www.op.gg/api/statistics/global/champions/ranked",
        # U_GG: "",
        BLITZ_GG: "https://league-champion-aggregate.iesdev.com/graphql",
    }


class ChampionsData(TypedDict):
    ChampionId: list[int]
    ChampionName: list[str]
    Role: list[str]
    TotalGames: list[int]
    Wins: list[int]
    Losses: list[int]
    Winrate: list[str | float]
    Provider: list[Providers] | Providers


@dataclass(slots=True)
class BaseAPIService:
    session: requests.sessions.Session = field(
        repr=False, default_factory=requests.session
    )
    headers: dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent": "Mozilla/5.0 (Windows NT 5.2; en-US; rv:1.9.0.20) Gecko/20140108 Firefox/37.0",
            "content-type": "application/json",
        }
    )
    params: dict = field(default_factory=dict)
    response_data: dict = field(repr=False, default_factory=dict)
    champions_names: dict[str, str] = field(default_factory=dict)
    champions_data: ChampionsData = field(
        repr=False,
        default_factory=lambda: {
            "ChampionId": [],
            "ChampionName": [],
            "Role": [],
            "TotalGames": [],
            "Wins": [],
            "Losses": [],
            "Winrate": [],
            "Provider": [],
        },
    )

    def __post_init__(self) -> None:
        print(f"\N{atom symbol} {Fore.LIGHTBLUE_EX}{self.__class__.__name__}")
        self.set_champions_names()

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.__dict__}"

    def __len__(self) -> int:
        return len(self.champions_data["ChampionId"])

    def __contains__(self, item: int) -> bool:
        return item in self.champions_data["ChampionId"]

    def set_champions_names(self) -> dict[str, str]:
        try:
            if not os.path.exists("assets/champions_names_by_id.json"):
                self.update_champions_assets()
            with open("assets/champions_names_by_id.json") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Something went wrong while trying to load the champions names."
            ) from e

        self.champions_names = data

    def calculate_winrate_percentage(
        self, format_type: type, wins: int, games: int, loses: int = 0
    ) -> str | float:
        percentage = round(
            wins / (wins + loses) * 100 if loses else wins / games * 100, 2
        )

        return f"{percentage}%" if format_type == str else percentage

    def complete_missing_champions_data(self) -> None:
        print(
            f"{Fore.LIGHTCYAN_EX}\t\N{black question mark ornament} Checking for missing champions."
        )
        missing_champs = []

        for champion_id, champion_name in self.champions_names.items():
            if (
                int(champion_id) not in self.champions_data["ChampionId"]
                or champion_name not in self.champions_data["ChampionName"]
            ):
                self.champions_data["ChampionId"].append(champion_id)
                self.champions_data["ChampionName"].append(champion_name)
                self.champions_data["Role"].append("-")
                self.champions_data["TotalGames"].append(0)
                self.champions_data["Wins"].append(0)
                self.champions_data["Losses"].append(0)
                self.champions_data["Winrate"].append("0%")
                missing_champs.append(champion_name)

        assert len(self.champions_data["ChampionId"]) >= len(
            self.champions_names
        ), f"Champions IDs must be equal or greater than {len(self.champions_names)}"
        assert len(self.champions_data["ChampionName"]) >= len(
            self.champions_names
        ), f"Champions names must be equal or greater than {len(self.champions_names)}"

        assert (
            len(self.champions_data["ChampionId"])
            == len(self.champions_data["ChampionName"])
            == len(self.champions_data["TotalGames"])
            == len(self.champions_data["Wins"])
            == len(self.champions_data["Losses"])
            == len(self.champions_data["Winrate"])
        ), "Champions data length doesn't match"

        if missing_champs:
            p = inflect.engine()
            print(
                f"{Fore.LIGHTCYAN_EX}\t\t\N{information source} Added {len(missing_champs)} missing champions: {p.join(missing_champs, final_sep='')}"
            )
        else:
            print(
                f"{Fore.LIGHTGREEN_EX}\t\t\N{check mark} No missing champions were found."
            )

    def update_champions_assets(self, patch: str = None) -> None:
        try:
            if not patch:
                print(
                    f"{Fore.LIGHTBLUE_EX}\t\N{information source} No patch specified."
                )
                print(
                    f"{Fore.LIGHTYELLOW_EX}\t\t\N{telephone receiver} Calling for the latest patch..."
                )
                patch_res: requests.Response = self.session.get(
                    "https://utils.iesdev.com/static/json/lol/riot/versions",
                    headers=self.headers,
                )
                patch: str = patch_res.json()[0]

            print(f"{Fore.LIGHTGREEN_EX}\t\t\t\N{check mark} Using patch {patch}")
            response: requests.Response = self.session.get(
                f"https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json"
            )

            if not response:
                raise requests.HTTPError(
                    "Couldn't fetch the champions data from Data Dragon, make sure that the provided patch is valid."
                )

            res_data: dict = response.json()
            assert (
                "data" in res_data
            ), "Couldn't fetch the champions data from Data Dragon, make sure that the provided patch is valid."

            print(
                f"{Fore.LIGHTYELLOW_EX}\t\N{hourglass} Writing champions data to champions.json"
            )
            with open("assets/champions.json", "w") as f:
                json.dump(res_data, f)

            champs_names_by_id = {
                value["key"]: value["name"] for value in res_data["data"].values()
            }

            assert len(res_data["data"].keys()) == len(
                champs_names_by_id.keys()
            ), f"{Fore.RED}Keys are not equal"
            print(
                f"{Fore.LIGHTYELLOW_EX}\t\N{hourglass} Writing mapped data to champions_names_by_id.json"
            )
            with open("assets/champions_names_by_id.json", "w") as f:
                json.dump(champs_names_by_id, f)

            print(
                f"{Fore.LIGHTGREEN_EX}\t\N{check mark} Updated champions assets successfully."
            )
        except Exception as e:
            raise Exception("Could not update the champions assets:", e) from e
