#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
    Adsidera v1.0 Space gravity game
    for more info, please visit http://sourceforge.net/projects/adsidera/
 
    Copyright (C) 2013 Piotr Gołąb

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from conf import *
from functions import *


def main():
    mainloop = Mainloop(camx, camy)
    while True:
        mainloop.play()


if __name__ == '__main__':
    main()

