import pytest
import logging
import logging_actions as subject
import argparse
from pathlib import Path

logger = logging.getLogger(__name__)


def test_none():
    test_logger = logging.getLogger("test_logger")
    logger.info(f"{test_logger.level=}")
    assert test_logger.level == logging._nameToLevel["NOTSET"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", action=subject.log_level_action(test_logger))
    args = parser.parse_args([])

    logger.info(f"{test_logger.level=}")
    assert test_logger.level == logging._nameToLevel["NOTSET"]

    logger.info(args)
    assert args.log_level is None


def test_default():
    test_logger = logging.getLogger("test_logger")
    logger.info(f"{test_logger.level=}")
    assert test_logger.level == logging._nameToLevel["NOTSET"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level", action=subject.log_level_action(test_logger), default="info"
    )
    args = parser.parse_args([])

    logger.info(f"{test_logger.level=}")
    assert test_logger.level == logging._nameToLevel["INFO"]

    logger.info(args)
    assert args.log_level == "info"


def test_user_arg():
    test_logger = logging.getLogger("test_logger")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level", action=subject.log_level_action(test_logger), default="info"
    )
    args = parser.parse_args(["--log-level", "debug"])

    logger.info(f"{test_logger.level=}")
    assert test_logger.level == logging._nameToLevel["DEBUG"]

    logger.info(args)
    assert args.log_level == "debug"


def test_choices(capsys: pytest.CaptureFixture):
    test_logger = logging.getLogger("test_logger")
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", action=subject.log_level_action(test_logger))

    with pytest.raises(SystemExit):
        args = parser.parse_args(["--log-level", "invalid"])

    stdout, stderr = capsys.readouterr()
    logger.info(f"{stdout=}")
    logger.info(f"{stderr=}")
    assert "invalid choice" in stderr


@pytest.fixture
def tmp_file(tmp_path: Path):
    tmp_path = tmp_path / "capture.txt"
    return tmp_path


def test_custom_level(tmp_file: Path):
    logging.addLevelName(5, "TRACE")

    test_logger = logging.getLogger("test_logger")
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", action=subject.log_level_action(test_logger))

    with open(tmp_file, "w+") as p:
        parser.print_usage(p)
    usage = tmp_file.read_text()
    logger.info(f"{usage=}")
    assert "trace" in usage

    args = parser.parse_args(["--log-level", "trace"])

    logger.info(f"{test_logger.level=}")
    assert test_logger.level == logging._nameToLevel["TRACE"]

    logger.info(args)
    assert args.log_level == "trace"
