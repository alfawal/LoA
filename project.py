from pprint import pprint as pp
from colorama import init
import pandas as pd
import requests

from services.blitzgg import Blitz
from services.opgg import OPGG
from services.utils import BaseAPIService

init(autoreset=True)

# # Blitz
# blitz = Blitz()
# stats = blitz.get_stats()

# df = pd.DataFrame(stats)
# print(len(df))
# df.drop_duplicates(subset=["ChampionId"], keep="first", inplace=True)
# print(len(df))

# OP.GG
opgg = OPGG()
stats = opgg.get_stats()

# pp(stats)
df = pd.DataFrame(stats)
print(len(df))
df.drop_duplicates(subset=["ChampionId"], keep="first", inplace=True)
print(len(df))
