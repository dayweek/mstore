#-*- coding: utf-8 -*-

# layer between database and app

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
import sys
from sqlite3 import dbapi2 as sqlite
import datetime as dt
import config
import shutil
import sys,os
#where to store data
default_filename = 'mstore-data'
media_filename = config.appdir+'/'+ default_filename

class Db:
  # connecting to db file
  def __init__(self):
#    if not os.path.isfile(data_file):
#      print _("Neexesituje")
#    print _("Neexesituje")
    if os.path.exists(media_filename):
      self.con = sqlite.connect(media_filename)
    else:
      try:
        shutil.copy(os.path.abspath(default_filename),config.appdir)
        self.con = sqlite.connect(media_filename)
      except:
        sys.exit('Problem with mstore-data file.') 
    self.con.row_factory = sqlite.Row

  #returns items in cart
  def fetchTemp(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT items.id,items.title, (temp_items.selling_price * temp_items.count) AS sum, temp_items.count FROM temp_items, items WHERE temp_items.item_id = items.id")
      return cur
    return []
  
  #returns items in given category
  def fetchCategoryItems(self,category_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT items.id, items.title, items.selling_price, items.buying_price, items.category_id, items.rank,items.count, temp_items.count AS cart_count FROM items LEFT OUTER JOIN temp_items ON  items.id = temp_items.item_id WHERE  items.category_id =" +str(category_id)+ "  ORDER BY rank")
      return cur
    return []

  #returns categories in given category
  def fetchCategoryCategories(self,category_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT * FROM categories WHERE category_id =" +str(category_id)+ " ORDER BY rank")
      return cur
    return []

  # copies given item from store to cart and with given amount (count)
  # if the item already exists, it updates count
  def moveItemToCart(self,item_id,count):
    if(self.con):
      cur = self.con.cursor()
      if(count > 0):
        cur.execute("SELECT selling_price FROM items WHERE id = "+str(item_id)+ ";")
        selling_price = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM temp_items WHERE item_id = "+str(item_id)+ ";")
        if int(cur.fetchone()[0]) == 0:
          cur.execute("INSERT INTO temp_items(selling_price,count,item_id) VALUES ("+str(selling_price)+","+str(count)+"," +str(item_id)+ ");")
        else:
          cur.execute("UPDATE temp_items SET count = "+str(count)+" WHERE item_id =" +str(item_id)+ ";")
      elif count == 0:
          cur.execute("DELETE FROM temp_items WHERE item_id =" +str(item_id)+ ";")
    return

  #returns amount of given item in cart
  def getCartCount(self,item_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT count FROM temp_items WHERE item_id = "+str(item_id)+ ";")
      p = cur.fetchall()
      if len(p) is 0:
        return "0"
      return p[0][0]

  #returns amount of given item in store
  def getItemCount(self,item_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT count FROM items WHERE id = "+str(item_id)+ ";")
      p = cur.fetchall()
      return p[0][0]

  #returns total price of items in cart
  def getCartSum(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT SUM(selling_price * count) FROM temp_items;")
      p = cur.fetchall()
      return p[0][0]

  # when customer pays:
  # we create new sold cart
  # we move items from cart to new sold cart
  # we substract count from store
  def pay(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT item_id,count FROM temp_items;")
      p = cur.fetchall()
      for i in p:
        cur.execute("UPDATE items SET count = count - "+str(i[1])+" WHERE id = "+str(i[0])+";")
      cur.execute("INSERT INTO carts (datetime) VALUES('"+str(dt.datetime.now())+"');")
      last = cur.lastrowid
      cur.execute("INSERT INTO cart_items(title,selling_price,buying_price,count, cart_id) SELECT items.title, items.selling_price, items.buying_price, temp_items.count, "+str(last)+" FROM temp_items, items WHERE  items.id = temp_items.item_id")
      self.clearCart()

  # we remove items from cart
  def clearCart(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("DELETE FROM temp_items;")

  # we save db
  def save(self):
    if(self.con):
      self.con.commit()

  #removes given item from store
  def removeItem(self,item_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("DELETE FROM items WHERE id = "+str(item_id)+ ";")

  #removes given category from store
  def removeCategory(self,category_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("DELETE FROM categories WHERE id = "+str(category_id)+ ";")

  #returns true/false whether the given category in category contains any items
  def isCategoryEmpty(self,cat_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT COUNT(*) FROM items WHERE category_id = "+str(cat_id)+ ";")
      n1 = int(cur.fetchone()[0])
      cur.execute("SELECT COUNT(*) FROM categories WHERE category_id = "+str(cat_id)+ ";")
      n2 = int(cur.fetchone()[0])
      if n1 + n2 == 0:
        return True
      return False

  #inserts new category to store
  def newCategory(self,title,category_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("INSERT INTO categories (title,category_id,rank) VALUES('"+title+"',"+str(category_id)+",0);")

  #renames given category
  def updateCategory(self,title,category_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("UPDATE categories SET title = '"+title+"' WHERE id = "+str(category_id)+";")

  #updates guven item in store
  def updateItem(self,title,buying_price,selling_price,count,item_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("UPDATE items SET title = '"+title+"', selling_price = "+str(selling_price)+" , buying_price = "+str(buying_price)+", count = "+str(count)+"  WHERE id = "+str(item_id)+";")

  #inserts new item into the store
  def newItem(self,title,buying_price,selling_price,count,category_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("INSERT INTO items (title,buying_price,selling_price,count,rank,category_id) VALUES('"+title+"',"+str(buying_price)+","+str(selling_price)+" ,"+str(count)+",0,"+str(category_id)+");")

  #returns desired item from store
  def fetchItem(self,item_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT * FROM items WHERE id = "+str(item_id)+ ";")
      p = cur.fetchall()
      return p[0]

  #return profit 
  def getProfit(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT SUM(buying_price - selling_price) FROM cart_items;")
      p = cur.fetchall()
      if len(p) is 0:
        return "0"
      return p[0][0]

  #returns all items from store
  def fetchItems(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT * FROM items;")
      return cur

  #returns sum of item attributes in store
  def getItemSums(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT SUM(buying_price * count) AS buying_price,SUM(selling_price * count ) AS selling_price, SUM(count) AS count FROM items;")
      p = cur.fetchall()
      if len(p) is 0 or  (p[0][0] is None):
        return [0,0,0]
      return p[0]

  # returns sold items in given period
  def fetchPeriodItems(self,date_from,date_to):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT cart_items.title, SUM(cart_items.buying_price * cart_items.count) ,SUM(cart_items.selling_price * cart_items.count) , SUM((cart_items.selling_price * cart_items.count) -  (cart_items.buying_price * cart_items.count)), SUM(cart_items.count)  FROM cart_items,  carts WHERE date(carts.datetime) BETWEEN '"+date_from+"' AND '"+date_to+"' AND carts.id = cart_items.cart_id  GROUP BY cart_items.title")
      return cur

  # returns attribute sum of sold items in given period
  def getPeriodSums(self,date_from,date_to):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT  SUM(cart_items.buying_price * cart_items.count) ,SUM(cart_items.selling_price * cart_items.count) , SUM((cart_items.selling_price * cart_items.count) -  (cart_items.buying_price * cart_items.count)), SUM(cart_items.count)  FROM cart_items,  carts WHERE date(carts.datetime) BETWEEN '"+date_from+"' AND '"+date_to+"' AND carts.id = cart_items.cart_id;")
      p = cur.fetchall()
      if (len(p) is 0) or (p[0][0] is None):
        return [0,0,0,0]
      return p[0]

  #foo method
  def test(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT * FROM carts WHERE date(carts.datetime) BETWEEN '2009-04-11' AND '2009-04-11'")
      return cur

  #returns last sold cart
  def getLastCart(self):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT id,datetime(datetime) FROM carts  ORDER BY datetime LIMIT 1")
      p = cur.fetchall()
      if (len(p) is 0) or (p[0][0] is None):
        return None
      return p[0]

  # returns items from given sold cart
  def fetchCartItems(self,cart_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT *,selling_price * count AS sum  FROM cart_items WHERE cart_id = "+str(cart_id)+";")
      return cur

  #returns attribute sums of given sold cart
  def fetchCartSums(self,cart_id):
    if(self.con):
      cur = self.con.cursor()
      cur.execute("SELECT SUM(selling_price * count), SUM(cart_items.count) FROM cart_items WHERE  cart_id = "+str(cart_id)+";")
      p = cur.fetchall()
      if (len(p) is 0) or (p[0][0] is None):
        return None
      return p[0]


