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
import htmloutput

# Cart handles widgets in cart tab
class Cart:
  # we load and adjust widgets
  def __init__(self,db,tree):
    self.db = db
    self.tree = tree
    mokoscroll = mokoui.FingerScroll()
    tv = tree.get_widget("cart_treeview")
    self.pay = tree.get_widget("cart_pay")
    self.pay.connect('clicked',self.on_pay_click_cb)
    self.clear = tree.get_widget("cart_clear")
    self.clear.connect('clicked',self.on_clear_click_cb)
    self.sum = tree.get_widget("cart_sum")
    newtv = Browser(self.db)
    mokoscroll.add(newtv)
    mokoscroll.set_property('sps',40)
    replace_widget(tv,mokoscroll)
    self.tv = newtv

  def update(self):
    self.tv.update()
    if not len(self.tv):
      self.clear.set_sensitive(False)
      self.pay.set_sensitive(False)
    else:
      self.clear.set_sensitive(True)
      self.pay.set_sensitive(True)
    sum = self.db.getCartSum()
    if not sum:
      sum = 0
    self.set_sum(sum)

  # client wants to pay his cart
  def on_pay_click_cb(self,widget):
    if confirmation(self.tree.get_widget("window"),u"Zaplatit nákup?", "Ano", "Ne"):
      self.db.pay()
      self.clear.set_sensitive(False)
      self.pay.set_sensitive(False)
      self.tv.update()
      htmloutput.bill(self.db)
      sum = self.db.getCartSum()
      if not sum:
        sum = 0
      self.set_sum(sum)

  # we empty the cart- callback
  def on_clear_click_cb(self,widget):
    if confirmation(self.tree.get_widget("window"),u"Opravdu chcete vyprázdnit košík?", "Ano", "Ne"):
      self.db.clearCart()
      self.clear.set_sensitive(False)
      self.pay.set_sensitive(False)
      self.tv.update()
      self.set_sum(0)
  #method to display total price for cart
  def set_sum(self,sum):
    self.sum.set_markup("Celkem:\n<span size=\"20000\" weight=\"bold\">" + str(roundPrice(sum)) + "</span>,-")
