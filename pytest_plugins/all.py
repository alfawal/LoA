import os
import shutil

from colorama import init


def pytest_sessionstart(session):
    # Initialize colorama for autoreset
    init(autoreset=True)

    # Create temporary test results directories for plot_data and export_to
    for path in [
        "test_results/op.gg/data",
        "test_results/op.gg/plots",
        "test_results/blitz.gg/data",
        "test_results/blitz.gg/plots",
    ]:
        os.makedirs(
            path,
            exist_ok=True,
        )


def pytest_sessionfinish(session, exitstatus):
    # Remove temporary test results directories
    shutil.rmtree(
        "test_results",
        ignore_errors=True,
    )
