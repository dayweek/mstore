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

# Admin takes care of buttons and treeview in Admin tab
class Admin:
  # we adjust and reparent widgets from glade
  def __init__(self,db,tree):
    self.modified = False
    self.db = db
    self.tree = tree
    self.cat_id = 0
    self.path = StorePath(tree.get_widget("admin_path"))

    newcat = tree.get_widget("new_category")
    newcat.connect('clicked',self.new_category_click_cb)
    newitem = tree.get_widget("new_item")
    newitem.connect('clicked',self.new_item_click_cb)
    up = tree.get_widget("admin_up")
    up.connect('clicked',self.up_click_cb)
    home = tree.get_widget("admin_home")
    home.connect('clicked',self.home_click_cb)
    self.remove = tree.get_widget("admin_remove")
    self.remove.connect('clicked',self.on_remove_click_cb)
    self.edit = tree.get_widget("admin_edit")
    self.edit.connect('clicked',self.on_edit_click_cb)
    mokoscroll = mokoui.FingerScroll()
    tv = tree.get_widget("admin_treeview")
    newtv = AdminCategoryBrowser(self.db,self.path)
    self.tv = newtv
    newtv.connect('category-enter', self.enter_category_cb)
    newtv.connect('category-home', self.home_category_cb)
    newtv.connect('category-leave', self.leave_category_cb)
    newtv.connect('item-selected', self.item_selected_cb)
    newtv.connect('category-selected', self.category_selected_cb)
    mokoscroll.add(newtv)
    mokoscroll.set_property('sps',40)
    replace_widget(tv,mokoscroll)

  def enter_category_cb(self,tv,title,cat_id):
    self.tree.get_widget("admin_up").set_sensitive(True)
    self.tree.get_widget("admin_home").set_sensitive(True)
    self.remove.set_sensitive(False)
    self.edit.set_sensitive(False)

  def home_category_cb(self,tv):
    self.tree.get_widget("admin_home").set_sensitive(False)
    self.tree.get_widget("admin_up").set_sensitive(False)
    self.remove.set_sensitive(False)
    self.edit.set_sensitive(False)

  def leave_category_cb(self,tv):
    self.remove.set_sensitive(False)
    self.edit.set_sensitive(False)

  #new category dialog
  def new_category_click_cb(self,event):
    tree = dlg_load_tree()
    dlg = tree.get_widget("category_dlg")
    tree.get_widget("category_storno").connect('clicked',self.category_cancel_clicked,dlg,tree)
    tree.get_widget("category_ok").connect('clicked',self.category_ok_clicked,dlg,tree)
    r = dlg.run()
    if r == gtk.RESPONSE_OK:
      self.db.newCategory('<b>'+self.new_category_title+'</b>',self.tv.cat_id)
      self.tv.update()
      self.remove.set_sensitive(False)
      self.edit.set_sensitive(False)

  # new item dialog 
  def new_item_click_cb(self,event):
    tree = dlg_load_tree()
    self.adjust_item_dlg(tree,new = True)
    dlg = tree.get_widget("item_dlg")
    tree.get_widget("item_storno").connect('clicked',self.category_cancel_clicked,dlg,tree)
    tree.get_widget("item_ok").connect('clicked',self.item_ok_clicked,dlg,tree)
    self.data_ok = False
    r = dlg.run()
    if self.data_ok:
      i = self.item_data
      self.db.newItem(i[0],i[1],i[2],i[3],self.tv.cat_id)
      self.tv.update()
      self.remove.set_sensitive(False)
      self.edit.set_sensitive(False)
      


  # getting user input on editting items/categoer
  def on_edit_click_cb(self,event):
    tree = dlg_load_tree()
    win = self.tree.get_widget("window")
    row = self.tv.get_row()
    #category
    if self.tv.get_model().get_path(self.tv.iter)[0] < self.tv.categoryNum:
      dlg = tree.get_widget("category_dlg")
      tree.get_widget("category_title").set_text(common.strip_tags(row[1]))

      tree.get_widget("category_storno").connect('clicked',self.category_cancel_clicked,dlg,tree)
      tree.get_widget("category_ok").connect('clicked',self.category_ok_clicked,dlg,tree)
      r = dlg.run()
      if r == gtk.RESPONSE_OK:
        self.db.updateCategory(self.new_category_title,row[0])
        self.tv.modify_row([row[0],self.new_category_title,None,None])
    #item
    else:
      dlg = tree.get_widget("item_dlg")
      self.adjust_item_dlg(tree)
      i = self.db.fetchItem(row[0])
      self.item_title.set_text(common.strip_tags(row[1]))
      self.item_selling_price.set_text(str(roundPrice(i[2])))
      self.item_buying_price.set_text(str(roundPrice(i[3])))
      self.item_count.set_text(row[3])

      tree.get_widget("item_storno").connect('clicked',self.category_cancel_clicked,dlg,tree)
      tree.get_widget("item_ok").connect('clicked',self.item_ok_clicked,dlg,tree)
      self.data_ok = False
      dlg.connect('response',self.edit_item_dlg_response)
      r = dlg.run()
        
  # editing item was ok
  def edit_item_dlg_response(self,dlg,response):
    if self.data_ok:
      row = self.tv.get_row()
      i = self.item_data
      self.db.updateItem(i[0],i[1],i[2],i[3],row[0])
      self.tv.modify_row([row[0],i[0],i[2],i[3]])
  def up_click_cb(self,event):
    self.tv.leaveCategory()
  def home_click_cb(self,event):
    self.tv.homeCategory()
  
  # user wants to remove item or category
  def on_remove_click_cb(self,widget):
    win = self.tree.get_widget("window")
    row = self.tv.get_row()
    # its category
    if self.tv.get_model().get_path(self.tv.iter)[0] < self.tv.categoryNum:
      #category must be empty
      if self.db.isCategoryEmpty(row[0]):
        if confirmation(win,u"Opravdu chcete smazat kategorii '"+common.strip_tags(row[1])+"'?", "Ano", "Ne"):
          self.db.removeCategory(row[0])
          self.tv.remove_row()
          self.modified = True
          self.remove.set_sensitive(False)
          self.edit.set_sensitive(False)
      else:
        note(win,'Nemohu smazat neprázdnou kategorii.','OK')
    #its item
    else:
      #item must not be in cart
      if int(self.db.getCartCount(row[0])) > 0:
        note(win,'Nemohu položku smazat. Část jich je v košíku.','OK')
      elif confirmation(win,u"Opravdu chcete smazat položku '"+common.strip_tags(row[1])+"'?", "Ano", "Ne"):
        self.db.removeItem(row[0])
        self.tv.remove_row()
        self.modified = True
        self.remove.set_sensitive(False)
        self.edit.set_sensitive(False)
      
  # user canceled category editation
  def category_cancel_clicked(self,event,dlg,tree):
    dlg.response(gtk.RESPONSE_CANCEL)
    dlg.destroy()
  
  # user finished category editation
  def category_ok_clicked(self,event,dlg,tree):
    if tree.get_widget('category_title').get_text().strip():
      self.new_category_title = tree.get_widget('category_title').get_text().strip()
      dlg.response(gtk.RESPONSE_OK)
      dlg.destroy()
  # when user finishes item editation we validate it and store values in this class
  def item_ok_clicked(self,event,dlg,tree):
    if self.item_title.isvalid() == VALID and self.item_buying_price.isvalid() == VALID and self.item_selling_price.isvalid() == VALID and self.item_count.isvalid() == VALID:
      i = []
      i.append(self.item_title.get_text().strip())
      i.append(self.item_buying_price.get_text().strip())
      i.append(self.item_selling_price.get_text().strip())
      i.append(self.item_count.get_text().strip())
      self.item_data = i
      self.data_ok = True
      dlg.response(gtk.RESPONSE_OK)
      dlg.destroy()

  def category_selected_cb(self,tv,model,iter):
    self.remove.set_sensitive(True)
    self.edit.set_sensitive(True)

  def item_selected_cb(self,tv,model,iter):
    self.remove.set_sensitive(True)
    self.edit.set_sensitive(True)

  def update(self):
    self.tv.update()

  # dialog for editing/creating items must be adjusted to validate values
  def adjust_item_dlg(self,tree,new = False):
    if not new:
      try:
        min =  int(self.db.getCartCount(self.tv.get_row()[0]))
        if min > 0:
          tree.get_widget("item_count_label").set_text("Pocet (min. "+str(min)+")")
      except:
        min = 0
    else:
      min = 0
    
    self.item_title =  ValidatedEntry(v_nonemptystring)
    self.item_buying_price =  ValidatedEntry(v_float_unsigned)
    self.item_selling_price =  ValidatedEntry(v_float_unsigned)
    self.item_count =  ValidatedEntry(bounded(v_int, int, min, 10000))
    replace_widget(tree.get_widget("item_title"), self.item_title )
    replace_widget(tree.get_widget('item_selling_price'), self.item_selling_price)
    replace_widget(tree.get_widget('item_buying_price'),self.item_buying_price )
    replace_widget(tree.get_widget('item_count'), self.item_count )
    tree.get_widget('item_dlg').set_response_sensitive(gtk.RESPONSE_NONE,True)

