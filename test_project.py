import pytest
from project import get_args, get_data_as_dataframe, export_to, plot_data
import argparse
import pandas as pd
import os
from datetime import datetime


def test_get_args():
    test1 = get_args(["op.gg", "-t", "xlsx", "--plot"])
    assert type(test1) == argparse.Namespace
    assert test1.provider == "op.gg"
    assert test1.type == "xlsx"
    assert test1.plot is True

    test2 = get_args(["op.gg", "--plot"])
    assert type(test2) == argparse.Namespace
    assert test2.provider == "op.gg"
    assert test2.type is None
    assert test2.plot is True

    test3 = get_args(["blitz.gg", "--plot", "--type", "csv"])
    assert type(test3) == argparse.Namespace
    assert test3.provider == "blitz.gg"
    assert test3.type == "csv"
    assert test3.plot is True

    test4 = get_args(["blitz.gg", "--no-plot", "--type", "json"])
    assert type(test4) == argparse.Namespace
    assert test4.provider == "blitz.gg"
    assert test4.type == "json"
    assert test4.plot is False

    test5 = get_args(["blitz.gg", "-t", "txt"])
    assert type(test5) == argparse.Namespace
    assert test5.provider == "blitz.gg"
    assert test5.type == "txt"
    assert test5.plot is None

    with pytest.raises(SystemExit) as test6:
        get_args(["blitz.gg"])
    assert test6.type == SystemExit
    assert "Please specify an export type or plot flag." in str(test6.value)
    assert "For more information run the program with -h/--help flag" in str(
        test6.value
    )
    assert "or visit the repository: https://github.com/alfawal/LoA" in str(test6.value)

    with pytest.raises(SystemExit) as test7:
        get_args(["op.gg"])
    assert test7.type == SystemExit
    assert "Please specify an export type or plot flag." in str(test7.value)
    assert "For more information run the program with -h/--help flag" in str(
        test7.value
    )
    assert "or visit the repository: https://github.com/alfawal/LoA" in str(test7.value)


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

    test1_champ_names = test1["ChampionName"].to_list()
    test1_champ_ids = test1.index.to_list()
    assert "Ezreal" in test1_champ_names
    assert 81 in test1_champ_ids

    assert "Jhin" in test1_champ_names
    assert 202 in test1_champ_ids

    assert "Lulu" in test1_champ_names
    assert 117 in test1_champ_ids

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
