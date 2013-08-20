#-*- coding: utf-8 -*-
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
import gtk
import sys
from db import *
from cart import *
from gtkcommon import *
import hildon
import mokoui
from ValidatedEntry import *
import re
import gobject
from glade import *
import copy
import common
import htmloutput
import datetime as dt
import calendar as cal

# this class handles widgets in stat tab
class Stat:
  def __init__(self,db,tree):
    self.db = db
    self.tree = tree
    self.date_from = hildon.DateEditor()
    replace_widget(tree.get_widget("date_from"),self.date_from)
    self.date_to = hildon.DateEditor()
    replace_widget(tree.get_widget("date_to"),self.date_to)
    tree.get_widget("store_html").connect('clicked',self.store_html_clicked)
    tree.get_widget("period_html").connect('clicked',self.store_period_clicked)

  def store_html_clicked(self,widget):
    htmloutput.store(self.db)
  # user wants to view sold items in a time period
  def store_period_clicked(self,widget):
    # we replace date_from with first day of this month and date_to replace with last day of the month
    date_from = dt.date.today()
    date_from = date_from.replace(self.date_from.get_year(),self.date_from.get_month(),self.date_from.get_day())
    date_to = dt.date.today()
    date_to = date_to.replace(self.date_to.get_year(),self.date_to.get_month(),self.date_to.get_day())
    htmloutput.period(self.db,str(date_to),str(date_from))

  #when user clicks on this tab we must update all values
  def update(self):
    date = dt.date.today()
    startmonth = date.replace(day = 1)
    endmonth = date.replace(day = cal.monthrange(date.year,date.month)[1])
    startmonth = str(startmonth)
    endmonth = str(endmonth)
    date = str(date)
    store_sums = self.db.getItemSums()
    day_sums = self.db.getPeriodSums(date,date)
    month_sums = self.db.getPeriodSums(startmonth,endmonth)
    self.tree.get_widget('buying_price_sum').set_text(str(roundPrice(store_sums[0])))
    self.tree.get_widget('selling_price_sum').set_text(str(roundPrice(store_sums[1])))
    self.tree.get_widget('count_sum').set_text(str(store_sums[2]))
    
    self.tree.get_widget('this_day_count').set_text(str(day_sums[3]))
    self.tree.get_widget('this_day_profit').set_text(str(roundPrice(day_sums[2])))

    self.tree.get_widget('this_month_count').set_text(str(month_sums[3]))
    self.tree.get_widget('this_month_profit').set_text(str(roundPrice(month_sums[2])))
