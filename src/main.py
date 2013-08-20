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
import sys
import string
import hildon
import cart
from glade import *
import store
import stats
import config
import adminstore
from db import *
import gtk
import gtk.gdk
#import xml.utils.iso8601
import time
#my modules
from common import *
import gettext
import locale

class App:
  def main_terminate(self,widget,event):
    self.db.con.commit()
    #nodes = XPath.Evaluate('descendant::kytka[@kprodeji]',storeRoot)
    #for i in nodes:
    #  i.removeAttribute("kprodeji")
    gtk.main_quit()
    return

  #toggling fulscreen
  def window_on_state_event(self,widget, event):
    if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
      self.window_in_fullscreen = True
    else:
      self.window_in_fullscreen = False
  
  #toggling fulscreen
  def window_on_key_press(self,widget, event):
    if event.keyval == gtk.keysyms.F6:
      if self.window_in_fullscreen:
        self.window.unfullscreen ()
      else:
        self.window.fullscreen ()

  #when switching tabs we update its content
  def on_switch_page_cb(self,notebook, page, page_num):
    if page_num == 0:
      self.admin.update()
    if page_num == 1:
      if self.admin.modified: #if we deleted or added category or item
        self.store.tv.homeCategory()
        self.admin.modified = False
      else:
        self.store.update()

    if page_num == 2:
      self.cart.update()
    if page_num == 3:
      self.stat.update()

  def run(self):
    config.create_appdir()
    self.window_in_fullscreen = False 

    #hildonizing
    program = hildon.Program() 
    window = hildon.Window()

    self.window = window
    program.add_window(self.window)
    tree = load_tree() #glade
    self.db = Db()
    nb = tree.get_widget("mainNotebook")
    nb.connect('switch-page',self.on_switch_page_cb)
    nb.reparent(window)
    window.set_property('name','window')
    window.set_title("mStore")
    window.connect("delete-event", self.main_terminate)
    window.connect("window-state-event", self.window_on_state_event)
    window.connect("key-press-event", self.window_on_key_press)
    self.admin = adminstore.Admin(self.db,tree)
    self.store = store.Store(self.db,tree)
    self.cart = cart.Cart(self.db,tree)
    self.stat = stats.Stat(self.db,tree)
    window.show_all()
    gtk.main()
app = App()
