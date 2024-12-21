#!/usr/bin/env python3

'''Define a function for runtime debugging.

This module defines the functions `debug` for writing debugging information at
runtime, `error` for reporting errors, and `note` for unconditionally writing
general information messages.

This module also sets a variable `DEBUG` that you can import to access
definitions from the environment.  This variable is a simple list of defined
debugging options.  Check for an option with `'option' in DEBUG`.

Debugging supports some simple options, controlled via the `DEBUG` environment
variable.  Set this to a comma-separated list of debugging options.  The
following are debugging options supported by this module, but you can add any
you care about.  Just be sure to document them.

debug ............. Enable debugging output.
context ........... Add context (file, line) information to every debugging
                    message.
nocolor ........... Do not try to use color in messages.
timestamp ......... Include a timestamp in every debugging message.

For example, the following is an example of running a python script with
debugging enabled and print both context and timestamps.

```python debug_test.py
#!/usr/bin/env python3

from debug import DEBUG, debug

debug("Debugging debug_test.py!")
if 'debug' in DEBUG:
    print("This block only runs when debugging is enabled.")
debug("Done!")
```

```bash
$ DEBUG=debug,context,timestamp python3 debug_test.py
DEBUG: 2023-11-13 15:07:51.267225 ...ng-solution/debug.py:93: Debugging is enabled
DEBUG: 2023-11-13 15:07:51.267350 ...tion/./debug_test.py:5: Debugging debug_test.py!
This block only runs when debugging is enabled.
DEBUG: 2023-11-13 15:07:51.267386 ...tion/./debug_test.py:8: Done!
```
'''

import sys
from os import environ
import datetime
from typing import Any


# Get the DEBUG environment variable, if it is defined.
if 'DEBUG' in environ:
    # The presence of the variable does not necessarily
    # enable debugging.  Break it into an array on commas.
    DEBUG = environ['DEBUG'].split(',')
    if '1' in DEBUG:
        DEBUG.remove('1')
        if 'debug' not in DEBUG:
            DEBUG.append('debug')
else:
    DEBUG = []


# These options are set *once*, when this module is imported.
_CONTEXT = 'context' in DEBUG
_COLOR = 'nocolor' not in DEBUG
_TIMESTAMP = 'timestamp' in DEBUG
if _CONTEXT:
    from inspect import currentframe, getframeinfo


# Enable or disable debugging.
if 'debug' in DEBUG:
    def debug(_msg: Any) -> None:
        '''Write a debugging message, if enabled.'''
        context = ''
        if _CONTEXT:
            frame = currentframe()
            if frame:
                frame = frame.f_back
                if frame:
                    info = getframeinfo(frame)
                    file = info.filename
                    if len(file) > 20:
                        file = '...'+file[-20:]
                    line = info.lineno
                    context = f'{file}:{line}: '
        timestamp = ''
        if _TIMESTAMP:
            timestamp = f'{datetime.datetime.now()} '
        if _COLOR:
            print(f"\x1b[32m\x1b[1mDEBUG\x1b[0m: {timestamp}{context}{_msg}", flush=True)
        else:
            print(f'DEBUG: {timestamp}{context}{_msg}', flush=True)
    debug("Debugging is enabled")
else:
    def debug(_msg: Any) -> None:
        '''Write a debugging message, if enabled.'''


if _COLOR:
    def error(msg: Any) -> None:
        '''Write an error message.'''
        sys.stderr.write(f"\x1b[31m\x1b[1mError\x1b[0m\x1b[1m: {msg}\x1b[0m\n")
        sys.stderr.flush()
else:
    def error(msg: Any) -> None:
        '''Write an error message.'''
        sys.stderr.write(f"Error: {msg}\n")
        sys.stderr.flush()


if _COLOR:
    def note(tag: Any, msg: Any) -> None:
        '''Write an informational message.'''
        sys.stderr.write(f"\x1b[34m\x1b[1m{tag}\x1b[0m: {msg}\x1b[0m\n")
        sys.stderr.flush()
else:
    def note(tag: Any, msg: Any) -> None:
        '''Write an informational message.'''
        sys.stderr.write(f"{tag}: {msg}\n")
        sys.stderr.flush()
