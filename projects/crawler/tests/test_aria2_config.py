from types import SimpleNamespace

import pytest

from application.config.model import Aria2Config
from core.request.descriptor import RequestDescriptor
from core.request.downloader.aria2.client import Aria2Client
from core.request.downloader.aria2.options import Aria2OptionsBuilder
from core.request.downloader.aria2.probe import Aria2RpcProbe
from core.request.downloader.config import Aria2DownloaderSpec
from core.request.middleware.proxy.config import ProxyConfig
from core.request.profile import RequestProfile
from core.request.typing import RequestKind, ResponseFormat


def test_aria2_config_supports_explicit_executable(monkeypatch):
    custom_path = r"C:\\tools\\aria2c.exe"
    monkeypatch.setenv("ARIA2C_PATH", custom_path)

    config = Aria2Config()

    assert config.executable == custom_path


def test_aria2_config_accepts_constructor_value():
    config = Aria2Config(executable=r"D:\\aria2\\bin\\aria2c.exe")

    assert config.executable == r"D:\\aria2\\bin\\aria2c.exe"


def test_aria2_rpc_clients_ignore_environment_proxy_settings():
    client = Aria2Client(rpc_url="http://127.0.0.1:6800/jsonrpc")
    probe = Aria2RpcProbe(rpc_url="http://127.0.0.1:6800/jsonrpc")

    assert client._client is None
    assert probe._client.trust_env is False


def test_aria2_options_builder_skips_proxy_for_localhost_targets():
    profile = RequestProfile(
        downloader=Aria2DownloaderSpec(),
        response_format=ResponseFormat.BINARY,
    )

    localhost_descriptor = RequestDescriptor(
        url="http://127.0.0.1:8000/image.jpg",
        kind=RequestKind.DOWNLOAD,
        profile=profile,
        target_spider="demo",
        proxy=ProxyConfig(url="http://proxy.example:8080"),
    )

    remote_descriptor = RequestDescriptor(
        url="https://example.com/image.jpg",
        kind=RequestKind.DOWNLOAD,
        profile=profile,
        target_spider="demo",
        proxy=ProxyConfig(url="http://proxy.example:8080"),
    )

    localhost_options = Aria2OptionsBuilder().build(
        SimpleNamespace(descriptor=localhost_descriptor),
        directory="downloads",
    )
    remote_options = Aria2OptionsBuilder().build(
        SimpleNamespace(descriptor=remote_descriptor),
        directory="downloads",
    )

    assert localhost_options.all_proxy is None
    assert remote_options.all_proxy == "http://proxy.example:8080"
