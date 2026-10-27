import pytest

from ai_sast_toolkit_runner import __version__
from ai_sast_toolkit_runner.cli import main


def test_version_flag_prints_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_arguments_prints_help(capsys):
    assert main([]) == 0
    assert "usage: ai-sast-run" in capsys.readouterr().out
