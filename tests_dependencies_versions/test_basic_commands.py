import json
import os
import sys
from pathlib import Path

sys.path.append(".")

from tests.test_utils import execute_in_terminal  # noqa


class TestBasicCommands:
    def test_describe(self):
        command = [
            "copernicusmarine",
            "describe",
        ]
        self.output = execute_in_terminal(command)
        assert self.output.returncode == 0
        json.loads(self.output.stdout)

    def test_subset(self, tmp_path):
        command = [
            "copernicusmarine",
            "subset",
            "-i",
            "med-hcmr-wav-rean-h",
            "-x",
            "13.723",
            "-X",
            "13.724",
            "-y",
            "38.007",
            "-Y",
            "40.028",
            "-t",
            "1993-01-01T00:00:00",
            "-T",
            "1993-01-01T06:00:00",
            "-v",
            "VHM0",
            "-o",
            f"{tmp_path}",
        ]

        self.output = execute_in_terminal(command)
        assert self.output.returncode == 0
        json.loads(self.output.stdout)

    def test_get(self, tmp_path):
        command = [
            "copernicusmarine",
            "get",
            "--dataset-id",
            "cmems_mod_glo_phy_anfc_0.083deg_P1D-m",
            "--filter",
            "*glo12_rg_1d-m_20230831-20230831_2D_hcst_R20230913*",
            "-o",
            f"{tmp_path}",
        ]
        self.output = execute_in_terminal(command)

        assert self.output.returncode == 0
        json.loads(self.output.stdout)

    def test_login(self, tmp_path):
        assert os.getenv("COPERNICUSMARINE_SERVICE_USERNAME") is not None
        assert os.getenv("COPERNICUSMARINE_SERVICE_PASSWORD") is not None

        non_existing_directory = Path(tmp_path, "i_dont_exist")
        command = [
            "copernicusmarine",
            "login",
            "--force-overwrite",
            "--configuration-file-directory",
            f"{non_existing_directory}",
            "--username",
            f"{os.getenv('COPERNICUSMARINE_SERVICE_USERNAME')}",
            "--password",
            f"{os.getenv('COPERNICUSMARINE_SERVICE_PASSWORD')}",
        ]

        self.output = execute_in_terminal(command, safe_quoting=True)
        assert self.output.returncode == 0
        assert non_existing_directory.is_dir()
