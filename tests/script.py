# Copyright (c) 2019-2024 the skillbridge authors (Niels Buwen, Tobias Markus)
# Derived from skillbridge (https://github.com/unihd-cag/skillbridge)
# SPDX-License-Identifier: LGPL-3.0-only
from ast import literal_eval
from sys import argv
from time import sleep

from allegrobridge._kernel import Symbol, Workspace

ws = Workspace.open(direct=True)

_, variable_name, value, delay = argv

sleep(float(delay))

ws['set'](Symbol(variable_name), literal_eval(value))
