import pytest

from application.config.model import Aria2Config


def test_aria2_config_supports_explicit_executable(monkeypatch):
    custom_path = r"C:\\tools\\aria2c.exe"
    monkeypatch.setenv("ARIA2C_PATH", custom_path)

    config = Aria2Config()

    assert config.executable == custom_path


def test_aria2_config_accepts_constructor_value():
    config = Aria2Config(executable=r"D:\\aria2\\bin\\aria2c.exe")

    assert config.executable == r"D:\\aria2\\bin\\aria2c.exe"
