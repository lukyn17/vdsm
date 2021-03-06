#
# Copyright 2012 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

from contextlib import contextmanager
from functools import wraps


#
# Monkey patch scope.
#
# Usage:
# ---
# from monkeypatch import MonkeyPatch
#
# def test():
#     with MonkeyPatchScope([
#         (subprocess, 'Popen', lambda x: None),
#         (os, 'chown', lambda *x: 0)
#     ])
#     logic
# ---
#
@contextmanager
def MonkeyPatchScope(what):
    old = []
    for f in what:
        module, name, that = f
        old.append((module, name, getattr(module, name)))
        setattr(module, name, that)
    try:
        yield {}
    finally:
        for f in old:
            module, name, that = f
            setattr(module, name, that)


#
# Monkey patch decoration.
#
# Usage:
# ---
# from monkeypatch import MonkeyPatch
#
# @MonkeyPatch(subprocess, 'Popen', lambda x: None)
# @MonkeyPatch(os, 'chown', lambda *x: 0)
# def test():
#     logic
# ---
#
def MonkeyPatch(module, name, that):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            with MonkeyPatchScope([(module, name, that)]):
                return f(*args, **kw)
        return wrapper
    return decorator
