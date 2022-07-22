# LoA: League of Archive

## Description

LoA: League of Archive is a CLI tool to scape League of Legends champions analyzed stats from OP.GG <!--, U.GG-->and BLITZ.GG into XLSX, CSV, JSON or TXT files and to visualize the gathered data.

## Video Demo

<div style="text-align: center">
<a href="https://www.youtube.com/watch?v=lDFCNSey9RI">
    <img src="https://img.shields.io/badge/YOUTUBE-WATCH%20NOW-red?logo=YOUTUBE&logoColor=red&style=for-the-badge" />
</a>

<!-- <iframe width="560" height="315" src="https://www.youtube.com/embed/lDFCNSey9RI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> -->
</div>

## Usage

```bash
python3 project.py --help
```

## Structure

1. Data gathering preferences:

   - Game patch (version): 12.13
   - Game mode: Ranked Solo/Duo
   - Champion roles: <img src="./assets/lanes/all.png" alt="all" width="15" height="15"/> All (<img src="./assets/lanes/top.png" alt="Top" width="15" height="15"/> Top, <img src="./assets/lanes/jng.png" alt="Jungle" width="15" height="15"/> Jungle, <img src="./assets/lanes/mid.png" alt="Mid" width="15" height="15"/> Mid, <img src="./assets/lanes/bot.png" alt="Bottom" width="15" height="15"/> Bot (ADC), <img src="./assets/lanes/sup.png" alt="Support" width="15" height="15"/> Support)
   - Players rank: <img src="./assets/ranks/platinum.png" alt="Platinum" width="15" height="15"/> Platinum and above (<img src="./assets/ranks/diamond.png" alt="Diamond" width="15" height="15"/> Diamond, <img src="./assets/ranks/master.png" alt="Master" width="15" height="15"/> Master, <img src="./assets/ranks/grandmaster.png" alt="Grandmaster" width="15" height="15"/> Grandmaster, <img src="./assets/ranks/challenger.png" alt="Challenger" width="15" height="15"/> Challenger)
   - Region: Global
   - Data period: Month or more

2. Data gathering methods:

   - OP.GG: API Call
   <!-- - U.GG: UI Scraping -->
   - BLITZ.GG: API Call

3. Dataframe structuring:

   - Unique value for each champion (161 champion as for patch 12.13)
   - The most played role for a champion will be selected if multiple roles are listed.
   - Champions with "not enough sample size" mark (The provider did not find enough matches to analyze) will automatically have 0 row values.
   - Columns are:

     - `ChampionId: int` - Source: Provider's response.
     - `ChampionName: str` - Source: Mapping ChampionId to ChampionName from Data Dragon's champions json response.
     - `Role: str` - Source: Provider's response.
     - `TotalGames: int` - Source: Provider's response.
     - `wins: int` - Source: Provider's response.
     - `Losses: int` - Source: Provider's response.
     - `Winrate: str | float` - Source: Formula (rounded to 2 decimal places):

       $$ Winrate \space percentage = {Wins \over Total \space games} \times 100 $$

     - `Provider: str` - Source: The data fetch source.

## Resources

- Data:

  - Champions list:

    - [Data Dragon 12.13.1 CDN](https://ddragon.leagueoflegends.com/cdn/12.13.1/data/en_US/champion.json "Data Dragon - champion")

  - Champions winrate:

    - [OP.GG - Stats](https://www.op.gg/statistics/champions)
    <!-- - [U.GG - Tier List](https://u.gg/lol/tier-list) -->
    - [BLITZ.GG - Tier List](https://blitz.gg/lol/tierlist)

  - Latest patch:
    - [BLITZ.GG](https://blitz.gg/)

- Other:

  - Icons:

    - Lanes:

      - [All](https://s-lol-web.op.gg/images/icon/icon-position-all-wh.svg)
      - [Top](https://s-lol-web.op.gg/assets/images/positions/01-icon-01-lol-icon-position-top-wh.svg)
      - [Jungle](https://s-lol-web.op.gg/assets/images/positions/01-icon-01-lol-icon-position-jng-wh.svg)
      - [Mid](https://s-lol-web.op.gg/assets/images/positions/01-icon-01-lol-icon-position-mid-wh.svg)
      - [Bot (ADC)](https://s-lol-web.op.gg/assets/images/positions/01-icon-01-lol-icon-position-bot-wh.svg)
      - [Support](https://s-lol-web.op.gg/assets/images/positions/01-icon-01-lol-icon-position-sup-wh.svg)

    - Ranks:
      - [Platinum](https://opgg-static.akamaized.net/images/medals_mini/platinum.png)
      - [Diamond](https://opgg-static.akamaized.net/images/medals_mini/diamond.png)
      - [Master](https://opgg-static.akamaized.net/images/medals_mini/master.png)
      - [Grandmaster](https://opgg-static.akamaized.net/images/medals_mini/grandmaster.png)
      - [Challenger](https://opgg-static.akamaized.net/images/medals_mini/challenger.png)

## Disclaimer

**This project is for educational purposes only and does not encourage any data usage without permission from its owner.**

<!-- **I do not own the used data. All credits go to its rightful owner.** -->