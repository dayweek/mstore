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
from validation_functions import *
import re
import gobject
from glade import *

#this class handles objects in store tab - buttons, treeview
class Store:
  # we adjust and reparent widgets from glade
  def __init__(self,db,tree):
    self.db = db
    self.tree = tree
    self.cat_id = 0
    self.path = StorePath(tree.get_widget("store_path"))
    add = tree.get_widget("store_add")
    add.connect('clicked',self.add_click_cb)
    self.add = add
    remove = tree.get_widget("store_remove")
    remove.connect('clicked',self.remove_click_cb)
    self.remove = remove
    counter = tree.get_widget("store_counter")
    parent = counter.get_parent()
    newcounter = Counter(add,remove)
    newcounter.connect_after('changed',self.on_counter_changed_cb)
    replace_widget(counter,newcounter)
    self.counter = newcounter

    mokoscroll = mokoui.FingerScroll()
    tv = tree.get_widget("store_treeview")
    up = tree.get_widget("store_up")
    up.connect('clicked',self.up_click_cb)
    home = tree.get_widget("store_home")
    home.connect('clicked',self.home_click_cb)
    newtv = CategoryBrowser(self.db,self.path)
    self.tv = newtv
    newtv.connect('category-enter', self.enter_category_cb)
    newtv.connect('category-home', self.home_category_cb)
    newtv.connect('item-selected', self.item_selected_cb)
    newtv.connect('category-selected', self.category_selected_cb)
    mokoscroll.add(newtv)
    mokoscroll.set_property('sps',40)
    replace_widget(tv,mokoscroll)

  #when user enters category
  def enter_category_cb(self,tv,title,cat_id):
    self.tree.get_widget("store_up").set_sensitive(True)
    self.tree.get_widget("store_home").set_sensitive(True)
    self.remove.set_sensitive(False)
    self.counter.set_sensitive(False)
    self.add.set_sensitive(False)

  #when user enters home category
  def home_category_cb(self,tv):
    self.tree.get_widget("store_home").set_sensitive(False)
    self.tree.get_widget("store_up").set_sensitive(False)
  
  #user click "up" button
  def up_click_cb(self,event):
    self.tv.leaveCategory()

  def category_selected_cb(self,tv,model,iter):
    self.counter.set_sensitive(False)
    self.add.set_sensitive(False)
    self.remove.set_sensitive(False)

  def item_selected_cb(self,tv,model,iter):
    row = tv.get_row()
    cart_count = self.db.getCartCount(row[0])
    self.counter.set_max(int(self.db.getItemCount(row[0])))
    self.counter.set_text(str(cart_count))
    self.counter.emit('changed')

  def home_click_cb(self,event):
    self.tv.homeCategory()

  def add_click_cb(self,event):
    cart_count = str(int(self.counter.get_text())+1)
    self.counter.set_text(cart_count)

  def remove_click_cb(self,event):
    cart_count = str(int(self.counter.get_text())-1)
    self.counter.set_text(cart_count)

  # counter displays item count in cart
  # if count changes we must handle sensitivity of other buttons
  def on_counter_changed_cb(self,event):
    row = self.tv.get_row()
    store_count = self.db.getItemCount(row[0])
    if not self.counter.get_text().strip():
      cart_count = 0
    else:
      cart_count = int(self.counter.get_text())
    row[3] = str(int(store_count)-cart_count)
    # we change value in treeview
    self.tv.modify_row(row)
    self.db.moveItemToCart(row[0],cart_count)
    if cart_count == 0 and int(store_count) == 0:
      self.add.set_sensitive(False)
      self.remove.set_sensitive(False)
      self.counter.set_sensitive(False)
    else:
      self.counter.set_sensitive(True)
      if cart_count == 0:
        self.remove.set_sensitive(False)
        self.add.set_sensitive(True)
      else:
        self.remove.set_sensitive(True)
      if cart_count == self.counter.max:
        self.add.set_sensitive(False)
        self.remove.set_sensitive(True)
      else:
        self.add.set_sensitive(True)
  def update(self):
    self.tv.update()

"""
def newListStore():
  return gtk.ListStore(int,str,str,str)

def cursor_changed(tv):
  selection = tv.get_selection()
  selection.set_mode(gtk.SELECTION_SINGLE)
  def foreachfunction(treemodel, path, iter, self):
    if  path[0] < self.categoryNum:
      self.selected_item = None
      self.enterCategory(treemodel.get_value(iter, 0), treemodel.get_value(iter, 1))
    else:
      self.selected_item = treemodel.get_value(iter, 0)
      self.updateCount()
  selection.selected_foreach(foreachfunction,self)

def changeCategory(self,category_id):
  self.cat_id = category_id
  new_ls = self.newListStore()
 #fetching data from database and inserting to liststore
  #categories
  content = self.db.fetchCategoryCategories(category_id)
  self.categoryNum = 0
  for i in content:
    print i
    #print '<b>' + i["title"] + '</b>'
    self.categoryNum+=1
    new_ls.append([i["id"],'<b>' + i["title"] + '</b>','',''])
    #new_ls.append([i["id"], i["title"],'',''])
  #items
  content = self.db.fetchCategoryItems(category_id)
  for i in content:
    print i
    print i["cart_count"]
    if(not i["cart_count"]):
      cart_count = "0"
    else:
      cart_count = i["cart_count"]
    cart_diff = int(i["count"]) - int(cart_count)
    new_ls.append([i["id"],i["title"],i["selling_price"],cart_diff])

  self.tv.set_model(new_ls)
def enterCategory(self, category_id, title):
  self.changeCategory(category_id)
  self.path.append(title)
  self.pathIds.append(category_id)
  self.updatePathLabel()
  self.upBtn.set_sensitive(True)
  self.updateCount()
def leaveCategory(self):
  if(len(self.path) is not 0):
    self.path.pop()
    self.pathIds.pop()
    if(len(self.pathIds) is not 0):
      self.changeCategory(self.pathIds[-1])
    else:
      self.changeCategory(0)
      self.upBtn.set_sensitive(False)
    self.updatePathLabel()
def on_is_min(self, widget):
  self.removeBtn.set_sensitive(False)
def on_is_not_min(self, widget):
  self.removeBtn.set_sensitive(True)
def updateCount(self):
  if self.selected_item:
    self.count.set_text(str(self.db.getCartCount(self.selected_item)))
    if int(self.count.get_text()) > 0:
      self.removeBtn.set_sensitive(True)
    self.addBtn.set_sensitive(True)
    self.infoBtn.set_sensitive(True)
    self.count.set_sensitive(True)
  else:
    self.removeBtn.set_sensitive(False)
    self.addBtn.set_sensitive(False)
    self.infoBtn.set_sensitive(False)
    self.count.set_sensitive(False)
  
def upBtnClicked(self,widget,event):
  self.leaveCategory()
def addBtnClicked(self,widget,event):
  if self.selected_item:
    count = str(int(self.count.get_text()) + 1)
    self.count.set_text(count)
    self.db.moveItemToCart(self.selected_item, count)
def removeBtnClicked(self,widget,event):
  if self.selected_item:
    count = str(int(self.count.get_text()) - 1)
    self.count.set_text(count)
    self.db.moveItemToCart(self.selected_item, count)
def keyPressed(self, widget, event):
  if(event.keyval == gtk.keysyms.F6):
    sys.stderr.write('aaaa')

def __count_focus_out_cb(self, widget, event):
  if not self.count.get_text().strip():
    #self.emit("is-min")
    self.count.set_text("0")
  if self.selected_item:
    self.db.moveItemToCart(self.selected_item, self.count.get_text())
"""
