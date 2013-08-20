#-*- coding: utf-8 -*-

# contains helpful custom gtk classes and structures
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
import pango
import gobject
from ValidatedEntry import *
from validation_functions import *
import common
import hildon
import math
#math.round = lambda num: math.floor(num+0.5)

ROW_FONT_SIZE = 24
TITLE_LENGTH = 12 #deprecated

#rounding price to two decimal points
def roundPrice(price):
  try:
    return "%.2f" % float(price)
  except:
    return ""

#deprecated
def titleRenderFunc( column, cell, model, iter):
  title = model.get_value(iter, 1)
  cell.set_property('text', title[:TITLE_LENGTH])
  return

#roundig price in treeview column
def priceRenderFunc( column, cell, model, iter):
  price = model.get_value(iter, 2)
  cell.set_property('text', roundPrice(price))
  return


titleRenderer = gtk.CellRendererText()
titleRenderer.set_property('size',ROW_FONT_SIZE * pango.SCALE)

countRenderer = gtk.CellRendererText()
countRenderer.set_property('size',ROW_FONT_SIZE * pango.SCALE)
countRenderer.set_property('xalign',1.0)

#this replace old widget with the new 
def replace_widget(old, new):
  parent = old.get_parent()
  new.set_property('name',old.get_property('name'))
  if parent is not None:
    props = []
    for pspec in parent.list_child_properties():
      props.append(pspec.name)
      props.append(parent.child_get_property(old, pspec.name))
    parent.remove(old)
    parent.add_with_properties(new, *props)
    if old.flags() & gtk.VISIBLE:
      new.show()
    else:
      new.hide()

# subclass of gtk.Entry, displays bounded integer
# add, remove are buttons, but they are no used..
class Counter(ValidatedEntry):
  def __init__(self,add,remove):
    self.add = add
    self.remove = remove
    ValidatedEntry.__init__(self,my_bounded(v_int, int, 0, 0))

    self.set_alignment(0.5)
    font_desc = pango.FontDescription()
    font_desc.set_size(40 * pango.SCALE)
    self.modify_font(font_desc)
    self.set_max_length(5)
    self.set_width_chars(5)
    self.set_sensitive(False)

  #sets max displayed number
  def set_max(self,max):
    max = int(max)
    self.max = max
    s = self.get_property('sensitive')
    v = self.get_text()
    ValidatedEntry.__init__(self,my_bounded(v_int, int, 0, max))
    self.set_property('sensitive',s)
    self.set_text(v)

# subclass of treeview determined to browse items, without categories
class Browser(gtk.TreeView):
  def __init__(self,db):
    gtk.TreeView.__init__(self)
    self.iter = None
    self.db = db
    self.init_columns()
    self.connect('cursor-changed',self.cursor_changed)
    self.connect('row-selected',self.row_selected)
    self.showdata()

  def init_columns(self):
    tvc_title = gtk.TreeViewColumn('Nazev', titleRenderer)
    self.append_column(tvc_title)
    tvc_title.set_expand(True)
    tvc_title.add_attribute(titleRenderer, "text", 0)
    tvc_title.set_attributes(titleRenderer, markup=1)

    tvc_price = gtk.TreeViewColumn('Suma', countRenderer)
    tvc_price.add_attribute(countRenderer, "text", 2)
    tvc_price.set_cell_data_func(countRenderer,priceRenderFunc)
    self.append_column(tvc_price)

    tvc_count = gtk.TreeViewColumn('Pocet', countRenderer)
    tvc_count.add_attribute(countRenderer, "text", 3)
    self.append_column(tvc_count)
  #returns gtk.ListStore
  def new_ls(self):
    return gtk.ListStore(int,str,str,int)

  # a row is clicked we emit row-selected signal
  def cursor_changed(self,tv):
    selection = self.get_selection()
    selection.set_mode(gtk.SELECTION_SINGLE)
    def foreachfunction(treemodel, path, iter, self):
      treemodel.get_n_columns()-1
      self.emit('row-selected',treemodel,iter)
    selection.selected_foreach(foreachfunction,self)
  
  #displays data from cart
  def showdata(self):
    new_ls = self.new_ls()
    #fetching data from database and inserting to liststore

    #categories
    content = self.db.fetchTemp()
    for i in content:
      new_ls.append([i["id"],i["title"],i['sum'],i['count']])
    self.set_model(new_ls)

  def row_selected(self,tv,treemodel,iter):
    pass #we do nothing in this class
  def __len__(self):
    return len(self.get_model())
  def update(self):
    self.showdata()

#registering row-selected signal
gobject.type_register(Browser)
gobject.signal_new("row-selected", Browser, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))



# subclass of treeview determined to browse items and categories
class CategoryBrowser(Browser):
  def __init__(self,db,path):
    self.path = path
    Browser.__init__(self,db)
    self.connect('row-activated',self.row_activated)
  def init_columns(self):
    tvc_title = gtk.TreeViewColumn('Nazev', titleRenderer,markup=1)
    self.append_column(tvc_title)
    tvc_title.set_expand(True)
    tvc_title.add_attribute(titleRenderer, "text", 0)

    tvc_price = gtk.TreeViewColumn('Cena', countRenderer)
    tvc_price.add_attribute(countRenderer, "text", 2)
    tvc_price.set_cell_data_func(countRenderer,priceRenderFunc)
    self.append_column(tvc_price)

    tvc_count = gtk.TreeViewColumn('Na sklade', countRenderer)
    tvc_count.add_attribute(countRenderer, "text", 3)
    self.append_column(tvc_count)

  #returns gtk.ListStore
  def new_ls(self):
    return gtk.ListStore(int,str,str,str)

  #displays data from cart
  def showdata(self,cat_id = 0):
    self.cat_id = cat_id
    new_ls = self.new_ls()
    #fetching data from database and inserting to liststore

    #categories
    content = self.db.fetchCategoryCategories(cat_id)
    self.categoryNum = 0
    for i in content:
      self.categoryNum+=1
      new_ls.append([i["id"],'<b>' + i["title"] + '</b>','',''])
    #items
    content = self.db.fetchCategoryItems(cat_id)
    for i in content:
      if(not i["cart_count"]):
        cart_count = "0"
      else:
        cart_count = i["cart_count"]
      cart_diff = int(i["count"]) - int(cart_count)
      new_ls.append([i["id"],i["title"],i["selling_price"],cart_diff])
    self.set_model(new_ls)

  # for entering given category
  def enterCategory(self, category_id, title):
    self.showdata(category_id)
    self.path.append(title,category_id)
    self.emit('category-enter',title,category_id)

  # handles leaving category
  def leaveCategory(self):
    self.path.pop()
    if self.path:
      self.showdata(self.path.get_meta())
      self.emit('category-leave')
    else:
      self.showdata(0)
      self.emit('category-home')

  # for returning to home category
  def homeCategory(self):
    self.showdata(0)
    self.path.flush()
    self.emit('category-home')

  # updates selected row
  def modify_row(self, row = []):
    model = self.get_model()
    if len(row) == 4 and self.iter:
      for i in range(0,4):
        model.set_value(self.iter, i, row[i])
    else: 
      return False

  #returns selected row
  def get_row(self):
    row = []
    if self.iter:
      for i in range(0,4):
        row.append(self.get_model().get_value(self.iter, i))
    return row

  # when category is double clicked it enters it
  def row_activated(self,tv,path,column):
    self.iter = tv.get_model().get_iter(path)
    if path[0] < self.categoryNum:
      self.enterCategory(tv.get_model().get_value(self.iter, 0),tv.get_model().get_value(self.iter, 1))

   # when row is selected it emits appropriate signal
  def row_selected(self,tv,model,iter):
    self.iter = iter
    if model.get_path(iter)[0] >= self.categoryNum:
      self.emit('item-selected',model,iter)
    else:
      self.emit('category-selected',model,iter)

  def update(self):
    self.showdata(self.cat_id)

#registering signals
gobject.type_register(CategoryBrowser)
gobject.signal_new("category-enter", CategoryBrowser, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,gobject.TYPE_INT))
gobject.signal_new("category-leave", CategoryBrowser, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
gobject.signal_new("category-home", CategoryBrowser, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
gobject.signal_new("item-selected", Browser, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))
gobject.signal_new("category-selected", Browser, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))

#similiar to CategoryBrowser but show a little different data
class AdminCategoryBrowser(CategoryBrowser):
  def __init__(self,db,path):
    CategoryBrowser.__init__(self,db,path)
  def init_columns(self):
    #self.set_fixed_height_mode(True)
    #title column
    tvc_title = gtk.TreeViewColumn('Nazev', titleRenderer)
    self.append_column(tvc_title)
    tvc_title.set_expand(True)
    tvc_title.add_attribute(titleRenderer, "text", 0)
    tvc_title.set_attributes(titleRenderer, markup=1)

    tvc_price = gtk.TreeViewColumn('Cena', countRenderer)
    tvc_price.add_attribute(countRenderer, "text", 2)
    tvc_price.set_cell_data_func(countRenderer,priceRenderFunc)
    self.append_column(tvc_price)

    tvc_count = gtk.TreeViewColumn('Na sklade', countRenderer)
    tvc_count.add_attribute(countRenderer, "text", 3)
    self.append_column(tvc_count)
  
  # refreshes data
  def update(self):
    self.showdata(self.cat_id)

  #returns gtk.ListStore
  def new_ls(self):
    return gtk.ListStore(int,str,str,str)

  #displays data
  def showdata(self,cat_id = 0):
    self.cat_id = cat_id
    new_ls = self.new_ls()
    #fetching data from database and inserting to liststore

    #categories
    content = self.db.fetchCategoryCategories(cat_id)
    self.categoryNum = 0
    for i in content:
      self.categoryNum+=1
      new_ls.append([i["id"],'<b>' + i["title"] + '</b>','',''])
    #items
    content = self.db.fetchCategoryItems(cat_id)
    for i in content:
      if(not i["cart_count"]):
        cart_count = "0"
      else:
        cart_count = i["cart_count"]
      cart_diff = int(i["count"]) - int(cart_count)
      new_ls.append([i["id"],i["title"],i["selling_price"],i['count']])
    self.set_model(new_ls)

  # updates selected row
  def modify_row(self, row = []):
    model = self.get_model()
    if len(row) == 4 and self.iter:
      for i in range(0,4):
        model.set_value(self.iter, i, row[i])
    else: 
      return False

  # removes selected row
  def remove_row(self, row = []):
    model = self.get_model()
    model.remove(self.iter)

  #returns selected row
  def get_row(self):
    row = []
    if self.iter:
      for i in range(0,4):
        row.append(self.get_model().get_value(self.iter, i))
    return row

# gtk.Label subclass, displays path to category e.g. /category/another/
class StorePath():
  __titles = []
  __metas = []
  def __init__(self,label):
    self.__label = label
  def append(self,title = '',tuple = []):
    self.__titles.append(title)
    self.__metas.append(tuple)
    self.__update()
  def pop(self):
    self.__titles.pop()
    self.__metas.pop()
    self.__update()
  def __update(self):
    if self.__titles:
      text = ''
      for title in self.__titles:
        text +=  '/' + common.strip_tags(title)
      self.__label.set_text(text)
    else:
      self.__label.set_text('')
  def flush(self):
    while self.__titles:
      self.__titles.pop()
      self.__metas.pop()
    self.__update()
  def get_meta(self):
    if self.__metas:
      return self.__metas[-1]
  def get_title(self):
    if self.__titles:
      return self.__titles[-1]
  def __len__(self):
    if self.__titles:
      return True
    return False


#dialog for asking yes/no questions
def confirmation(window,text,yes,no):
  dialog = hildon.Note ("confirmation", (window, text, gtk.STOCK_DIALOG_WARNING) )
  dialog.set_button_texts (yes, no)
  response = dialog.run()
  dialog.destroy()
  if response == gtk.RESPONSE_OK:
    return True
  return False

# simple information dialog
def note(window,text,ok):
  dialog = hildon.Note ("information", (window, text, gtk.STOCK_DIALOG_WARNING) )
  dialog.set_button_text(ok)
  dialog.run()
  dialog.destroy()
