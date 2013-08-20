#-*- coding: utf-8 -*-

# custom validation functions for ValidatedEntry class
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
from ValidatedEntry import *
import re

def v_int_unsigned(value):
    '''
    VALID: any postive integer including zero
    PARTAL: empty or leading "-"
    INVALID: non-numeral
    '''
    v = value.strip()
    if not v or v == '-':
        return PARTIAL
    try:
        if int(value) >= 0:
            return VALID
    except:
        return INVALID

# FLOAT
def v_float_unsigned(value):
    '''
    VALID: any postive floating point with max 2 decimal points 
    PARTAL: empty or leading "-", "."
    INVALID: non-numeral
    '''
    p = re.compile(r'\..*')
    decimal = p.search(value)
    if decimal:
      points = (len(decimal.group())-1 <= 2)
      print 'points', points
    else:
      points = True

    v = value.strip()
    if not v or v in ('-', '.', '-.'):
        return PARTIAL
    try:
      if float(value) >= 0 and points:
            return VALID
    except:
        return INVALID

def my_bounded(vfunc, conv, minv=None, maxv=None):

    '''returns:
    VALID: value between minv and maxv or empty
    INVALID: if value < minv or value > maxv
    '''

    assert minv is not None or maxv is not None, \
           'One of minv/maxv must be specified'

    def F(value):

        r = vfunc(value)
        if not value:
          return VALID
        if r == VALID:
            v = conv(value)
            if minv is not None and v < minv:
                return INVALID
            if maxv is not None and v > maxv:
                return INVALID
        return r

    return F
