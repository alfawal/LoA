import argparse
import os
from datetime import datetime

import pandas as pd
from colorama import Fore, init
from matplotlib.pyplot import savefig
from UliPlot.XLSX import auto_adjust_xlsx_column_width

from services import __app_description__, __app_name__, __repo_url__, __version__
from services.blitzgg import Blitz
from services.opgg import OPGG


def get_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"{Fore.LIGHTCYAN_EX}{__app_description__}{Fore.LIGHTMAGENTA_EX}",
        epilog=f"{Fore.LIGHTYELLOW_EX}Results will be exported under ./results{Fore.RESET}",
    )
    parser._positionals.title = f"{Fore.LIGHTGREEN_EX}Positional arguments{Fore.RESET}"
    parser._optionals.title = f"{Fore.LIGHTGREEN_EX}Optional arguments{Fore.RESET}"

    provider_arg = parser.add_argument(
        "provider",
        help=f"{Fore.LIGHTBLUE_EX}Data provider to use, options: {{op.gg, blitz.gg}}{Fore.RESET}",
        type=str.lower,
        # choices=["op.gg", "blitz.gg"], # removed due to uglifying the -h output
    )
    type_arg = parser.add_argument(
        "-t",
        "--type",
        help=f"{Fore.LIGHTBLUE_EX}Data exporting type, options: {{xlsx, csv, json, txt}}, default: xlsx{Fore.RESET}",
        type=str.lower,
        # choices=["xlsx", "csv", "json", "txt"], # removed due to uglifying the -h output
    )
    parser.add_argument(
        "--plot",
        action=argparse.BooleanOptionalAction,
        help=f"{Fore.LIGHTBLUE_EX}Visualize the data and export it as png{Fore.RESET}",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__app_name__} {__version__}",
        help=f"{Fore.LIGHTBLUE_EX}Show program's version number and exit{Fore.RESET}",
    )
    parser._actions[
        0
    ].help = f"{Fore.LIGHTBLUE_EX}Show this help message and exit{Fore.RESET}"

    args = parser.parse_args(args)

    if args.provider not in ["op.gg", "blitz.gg"]:
        raise argparse.ArgumentError(
            provider_arg,
            f'Invalid provider: "{args.provider}", options: {{op.gg, blitz.gg}}',
        )
    if not args.type and not args.plot:
        raise SystemExit(
            (
                f"\N{information source} {Fore.LIGHTCYAN_EX}Please specify an export type or plot flag."
                + f"\n{Fore.LIGHTYELLOW_EX}For more information run the program with -h/--help flag"
                + f"\nor visit the repository: {__repo_url__}"
            )
        )
    if args.type is not None and args.type not in ["xlsx", "csv", "json", "txt"]:
        raise argparse.ArgumentError(
            type_arg,
            f'Invalid type: "{args.type}", options: {{xlsx, csv, json, txt}}',
        )

    return args


def get_data_as_dataframe(provider: str) -> pd.DataFrame:
    match provider:
        case "op.gg":
            provider = OPGG()
        case "blitz.gg":
            provider = Blitz()
        case _:
            raise ValueError(f"Invalid provider: {provider}")

    data = provider.get_stats()
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=["ChampionId"], keep="first", inplace=True)
    df.sort_values("Winrate", ascending=False, inplace=True)
    df.set_index("ChampionId", inplace=True)

    return df


def export_to(
    dataframe: pd.DataFrame, date_time: str, export_type: str, path: str
) -> str:
    file_path = f"{path}/data/results_{date_time}.{export_type}"
    match export_type:
        case "xlsx":
            with pd.ExcelWriter(file_path) as writer:
                dataframe.to_excel(writer)
                auto_adjust_xlsx_column_width(
                    dataframe, writer, sheet_name="Sheet1", margin=3
                )
        case "csv":
            dataframe.to_csv(file_path)
        case "json":
            dataframe.to_json(file_path)
        case "txt":
            with open(file_path, "w") as f:
                f.write(dataframe.to_string())
        case _:
            raise ValueError(f"Invalid type: {export_type}")

    return file_path


def plot_data(dataframe: pd.DataFrame, date_time: str, path: str) -> str:
    plot_path = f"{path}/plots/plot_{date_time}.png"

    dataframe.set_index("ChampionName", inplace=True)
    dataframe["Winrate"].plot(kind="barh", figsize=(10, 75))
    savefig(plot_path)

    return plot_path


def main():
    init(autoreset=True)
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    args = get_args()

    data = get_data_as_dataframe(args.provider)

    path = f"results/{args.provider}"

    if args.type and not os.path.exists(f"{path}/data"):
        os.makedirs(f"{path}/data")
    if args.plot and not os.path.exists(f"{path}/plots"):
        os.makedirs(f"{path}/plots")

    if args.type:
        export_path = export_to(data, date_time, args.type, path)
        print(
            f"\N{bar chart} {Fore.LIGHTGREEN_EX}Exported successfully as {args.type.upper()} to: ./{export_path}"
        )

    if args.plot:
        plot_path = plot_data(data, date_time, path)
        print(
            f"\N{artist palette} {Fore.LIGHTGREEN_EX}Plotted successfully as PNG to: ./{plot_path}"
        )


if __name__ == "__main__":
    main()
