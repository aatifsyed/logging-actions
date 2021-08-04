# `logging-actions`
For easy configuration of `logging.Logger`s with `argparse.Action`s.

Use it like this:
```python
>>> from logging_actions import log_level_action
>>> from argparse import ArgumentParser
>>> import logging

>>> logger = logging.getLogger("foo") # Create your script's logger
>>> logger.addHandler(logging.StreamHandler())  # Don't forget to add a handler!

>>> parser = ArgumentParser()
>>> _ = parser.add_argument("--log-level", action=log_level_action(logger)) # create an action for your module's logger
>>> args = parser.parse_args() # Your logger's level will be set for you when parsing

```

## Features
### Choices are handled transparently
```text
foo.py --help

usage: foo.py [-h] [--log-level {critical,fatal,error,warn,warning,info,debug,notset}]

optional arguments:
  -h, --help            show this help message and exit
  --log-level {critical,fatal,error,warn,warning,info,debug,notset}
                        Set the logging level for foo.
```

### If you specify a default the log-level will be set accordingly
```python
parser.add_argument("-l", "--log-level", action=log_level_action(logger), default="info")
```

### Custom levels are supported
```python
logging.addLevelName(5, "TRACE")
parser.add_argument("-l", action=log_level_action(logger), default="trace")
```

## Benefits
### A better logging pattern
This replaces the following pattern for setting script log levels
```python
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "--log-level",
    default=logging.INFO,
    type=lambda x: getattr(logging, x)),
    help="Configure the logging level.",
)
args = parser.parse_args()
logging.basicConfig(level=args.log_level)
```
### Manage multiple loggers easily
```python
parser.add_argment("--foo-log-level", action=log_level_action(foo_logger))
parser.add_argment("--bar-log-level", action=log_level_action(bar_logger))
```