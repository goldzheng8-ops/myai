from core.input.reader.csv import CsvDataReader
from core.input.source import DataSource
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType


def test_csv_reader_accepts_string_format_from_config(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("name,age\nalice,30\n", encoding="utf-8")

    source = DataSource(format="csv", path=str(csv_path))

    rows = list(CsvDataReader().read(source))

    assert rows[0].values == {"name": "alice", "age": "30"}


def test_browser_action_coerces_boolean_value_to_string():
    action = BrowserAction(
        type=BrowserActionType.FILL,
        selector="input[name='q']",
        value=True,
    )

    assert action.value == "True"
