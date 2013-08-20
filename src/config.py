#-*- coding: utf-8 -*-

# configuration file

"""
    This file is part of mStore.

    mStore is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    mStore is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with mStore.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import shutil
appdir = '/media/mmc2/mstore'

def create_appdir():
  if not os.path.exists(appdir):
    os.makedirs(appdir)
  if not os.path.exists(appdir+"/styles.css"):
    shutil.copy(os.path.abspath('styles.css'),appdir+"/styles.css")
