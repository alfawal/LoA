import argparse
import os
from datetime import datetime

import pandas as pd
import pytest

from project import export_to, get_args, get_data_as_dataframe, plot_data


def test_get_args():
    test1_args = ["op.gg", "-t", "xlsx", "--plot"]
    test1 = get_args(test1_args)
    assert type(test1) == argparse.Namespace
    assert test1.provider == test1_args[0]
    assert test1.type == "xlsx"
    assert test1.plot is True

    test2_args = ["op.gg", "--plot"]
    test2 = get_args(test2_args)
    assert type(test2) == argparse.Namespace
    assert test2.provider == test2_args[0]
    assert test2.type is None
    assert test2.plot is True

    test3_args = ["blitz.gg", "--plot", "--type", "csv"]
    test3 = get_args(test3_args)
    assert type(test3) == argparse.Namespace
    assert test3.provider == test3_args[0]
    assert test3.type == "csv"
    assert test3.plot is True

    test4_args = ["blitz.gg", "--no-plot", "--type", "json"]
    test4 = get_args(test4_args)
    assert type(test4) == argparse.Namespace
    assert test4.provider == test4_args[0]
    assert test4.type == "json"
    assert test4.plot is False

    test5_args = ["blitz.gg", "-t", "txt"]
    test5 = get_args(test5_args)
    assert type(test5) == argparse.Namespace
    assert test5.provider == test5_args[0]
    assert test5.type == "txt"
    assert test5.plot is None

    test6_args = ["blitz.gg"]
    with pytest.raises(SystemExit) as test6:
        get_args(test6_args)
    assert test6.type == SystemExit
    assert "Please specify an export type, plot or stream flag." in str(test6.value)
    assert "For more information run the program with -h/--help flag" in str(
        test6.value
    )
    assert "or visit the repository: https://github.com/alfawal/LoA" in str(test6.value)

    test7_args = ["op.gg"]
    with pytest.raises(SystemExit) as test7:
        get_args(test7_args)
    assert test7.type == SystemExit
    assert "Please specify an export type, plot or stream flag." in str(test7.value)
    assert "For more information run the program with -h/--help flag" in str(
        test7.value
    )
    assert "or visit the repository: https://github.com/alfawal/LoA" in str(test7.value)

    test8_args = ["lol.cs50p.gg"]
    with pytest.raises(argparse.ArgumentError) as test8:
        get_args(test8_args)
    assert test8.type == argparse.ArgumentError
    assert "Invalid provider:" in str(test8.value)
    assert test8_args[0] in str(test8.value)

    test10_args = ["cs50lol.gg", "--plot"]
    with pytest.raises(argparse.ArgumentError) as test10:
        get_args(test10_args)
    assert test10.type == argparse.ArgumentError
    assert "Invalid provider:" in str(test10.value)
    assert test10_args[0] in str(test10.value)

    test11_args = ["stats.cs50p.gg", "-t", "csv"]
    with pytest.raises(argparse.ArgumentError) as test11:
        get_args(test11_args)
    assert test11.type == argparse.ArgumentError
    assert "Invalid provider:" in str(test11.value)
    assert test11_args[0] in str(test11.value)


def test_get_data_as_dataframe():
    test1 = get_data_as_dataframe("op.gg")
    assert type(test1) == pd.DataFrame
    assert test1.index.name == "ChampionId"
    assert test1.columns.tolist() == [
        "ChampionName",
        "Role",
        "TotalGames",
        "Wins",
        "Losses",
        "Winrate",
        "Provider",
    ]
    assert test1.loc[1, "Provider"] == "OP.GG"

    test1_champs_names = test1["ChampionName"].to_list()
    test1_champs_ids = test1.index.to_list()
    for test1_champ_id, test1_champ_name in (
        (202, "Jhin"),
        (81, "Ezreal"),
        (117, "Lulu"),
    ):
        assert test1_champ_id in test1_champs_ids
        assert test1_champ_name in test1_champs_names

    test2 = get_data_as_dataframe("blitz.gg")
    assert type(test2) == pd.DataFrame
    assert test2.index.name == "ChampionId"
    assert test2.columns.tolist() == [
        "ChampionName",
        "Role",
        "TotalGames",
        "Wins",
        "Losses",
        "Winrate",
        "Provider",
    ]
    assert test2.loc[1, "Provider"] == "BLITZ.GG"

    test2_champs_roles = test2["Role"].to_list()
    for test2_role in ("Top", "Jungle", "Mid", "ADC", "Support"):
        assert test2_role in test2_champs_roles

    with pytest.raises(ValueError) as test3:
        get_data_as_dataframe("invalid")
    assert test3.type == ValueError
    assert "Invalid provider" in str(test3.value)


def test_export_to():
    # op.gg data
    provider = "op.gg"
    dataframe = get_data_as_dataframe(provider)
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"test_results/{provider}"

    test1_type = "xlsx"
    test1 = export_to(dataframe, date_time, test1_type, path)
    test1_file_path = f"test_results/{provider}/data/results_{date_time}.{test1_type}"
    assert type(test1) == str
    assert test1_file_path in test1
    assert os.path.isfile(test1) == True
    assert os.path.exists(test1) == True
    assert os.path.splitext(test1)[1][1:] == test1_type

    test2_type = "csv"
    test2 = export_to(dataframe, date_time, test2_type, path)
    test2_file_path = f"test_results/{provider}/data/results_{date_time}.{test2_type}"
    assert type(test2) == str
    assert test2_file_path in test2
    assert os.path.isfile(test2) == True
    assert os.path.exists(test2) == True
    assert os.path.splitext(test2)[1][1:] == test2_type

    # blitz.gg data
    provider2 = "blitz.gg"
    dataframe2 = get_data_as_dataframe(provider2)
    date_time2 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path2 = f"test_results/{provider2}"

    test3_type = "json"
    test3 = export_to(dataframe2, date_time2, test3_type, path2)
    test3_file_path = f"test_results/{provider2}/data/results_{date_time2}.{test3_type}"
    assert type(test3) == str
    assert test3_file_path in test3
    assert os.path.isfile(test3) == True
    assert os.path.exists(test3) == True
    assert os.path.splitext(test3)[1][1:] == test3_type

    test4_type = "txt"
    test4 = export_to(dataframe2, date_time2, test4_type, path2)
    test4_file_path = f"test_results/{provider2}/data/results_{date_time2}.{test4_type}"
    assert type(test4) == str
    assert test4_file_path in test4
    assert os.path.isfile(test4) == True
    assert os.path.exists(test4) == True
    assert os.path.splitext(test4)[1][1:] == test4_type

    test5_type = "invalid"
    with pytest.raises(ValueError) as test5:
        export_to(dataframe2, date_time2, test5_type, path2)
    assert test5.type == ValueError
    assert "Invalid type" in str(test5.value)
    assert test5_type in str(test5.value).split(":")[1]

    test6_type = "playfield.py"
    with pytest.raises(ValueError) as test6:
        export_to(dataframe2, date_time2, test6_type, path2)
    assert test6.type == ValueError
    assert "Invalid type" in str(test6.value)
    assert test6_type in str(test6.value).split(":")[1]


def test_plot_data():
    # op.gg plot
    provider = "op.gg"
    dataframe = get_data_as_dataframe(provider)
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"test_results/{provider}"
    file_type = "png"

    test1 = plot_data(dataframe, date_time, path)
    assert type(test1) == str
    assert os.path.isfile(test1) == True
    assert os.path.exists(test1) == True
    assert os.path.splitext(test1)[1][1:] == file_type

    # blitz.gg plot
    provider = "blitz.gg"
    dataframe = get_data_as_dataframe(provider)
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"test_results/{provider}"
    file_type = "png"

    test2 = plot_data(dataframe, date_time, path)
    assert type(test2) == str
    assert os.path.isfile(test2) == True
    assert os.path.exists(test2) == True
    assert os.path.splitext(test2)[1][1:] == file_type
