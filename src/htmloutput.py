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
import config
import db
import webbrowser
import datetime
import osso
from gtkcommon import  *

#this modules generates all the html files to config.app directoy

def header(title):
  return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
  <html>
  <head>
      <meta http-equiv="content-type" content="text/html;charset=utf-8">
      <title>'''+title+'''</title>
      <link rel="stylesheet" href="styles.css">
  </head>
  <body>
  '''
# this functions generates entire content of store
def store(db):
  osso_c = osso.Context("mstore", "0.0.1", False)
  datum = str(datetime.date.today())
  data = header('Stav skladu '+datum)
  data += '<h3>Stav skladu '+datum+'</h3>'
  sums = db.getItemSums()
  items = db.fetchItems()
  data += '<table width=\"100%\">\n'
  data += "<tr class=\"col_caption\"><td></td><td>Nákupní cena</td><td>Prodejní cena</td><td>Počet</td></tr>\n"
  data += "<tr><td class=\"title\">Celkem</td><td class=\"sum\">"+str(roundPrice(sums[0]))+"</td><td class=\"sum\">"+str(roundPrice(sums[1]))+"</td><td class=\"sum\">"+str(sums[2])+"</td></tr>\n"
  for i in items:
    data += "<tr><td class=\"number\">"+i[1]+"</td><td class=\"number\">"+str(roundPrice(i[2]))+"</td><td class=\"number\">"+str(roundPrice(i[3]))+"</td><td class=\"number\">"+str(i[4])+"</td></tr>\n"
  data += '</table></body>'
  filename = config.appdir+'/stav_skladu_'+datum+'.html';
  fstore = open(filename, 'w')
  fstore.write(data)
  fstore.close()
  webbrowser.open(filename, context=osso_c)
  #print data

# this function generates sold items from selected period
def period(db,date_from,date_to):
  osso_c = osso.Context("mstore", "0.0.1", False)
  if date_from > date_to:
    temp = date_from
    date_from = date_to
    date_to = temp
  items = db.fetchPeriodItems(date_from,date_to)
  sums = db.getPeriodSums(date_from,date_to)
  data = header('Zisky '+date_from+' až '+date_to)
  data += '<h3>Zisky '+date_from+' až '+date_to+'</h3>'
  data += '<table width=\"100%\">\n'
  data += "<tr><td></td><td class=\"col_caption\">Nákupní suma</td><td class=\"col_caption\">Prodejní suma</td><td class=\"col_caption\">Zisk</td><td class=\"col_caption\">Počet</td></tr>\n"
  data += "<tr><td class=\"title\">Celkem</td><td class=\"sum\">"+str(roundPrice(sums[0]))+"</td><td class=\"sum\">"+str(roundPrice(sums[1]))+"</td><td class=\"sum\">"+str(roundPrice(sums[2]))+"</td><td class=\"sum\">"+str(sums[3])+"</td></tr>\n"
  for i in items:
    data += "<tr><td class=\"title\">"+i[0]+"</td><td class=\"number\">"+str(roundPrice(i[1]))+"</td><td class=\"number\">"+str(roundPrice(i[2]))+"</td><td class=\"number\">"+str(roundPrice(i[3]))+"</td><td class=\"number\">"+str(i[4])+"</td></tr>\n"
  data += '</table></body>'
  filename = config.appdir+'/zisky_'+date_from+'_'+date_to+'.html';
  fstore = open(filename, 'w')
  fstore.write(data)
  fstore.close()
  webbrowser.open(filename, context=osso_c)
  #print data

#when a cart is payed, the bill html file is generated
def bill(db):
  #osso_c = osso.Context("mstore", "0.0.1", False)
  cart = db.getLastCart()
  data = header('Účet za nákup '+cart[1])
  data += '<h3>Účet za nákup '+cart[1]+'</h3>'
  items = db.fetchCartItems(cart[0])
  sums = db.fetchCartSums(cart[0])
  data += '<table width=\"100%\">\n'
  data += "<tr class=\"col_caption\"><td>Položka</td><td>Počet</td><td>Cena</td></tr>\n"
  for i in items:
    data += "<tr><td class=\"title\">"+str(i[1])+"</td><td class=\"number\">"+str(i[4])+"</td><td class=\"number\">"+str(roundPrice(i[6]))+"</td></tr>\n"
  data += "<tr><td class=\"title\">Celkem</td><td class=\"sum\">"+str(sums[1])+"</td><td class=\"sum\">"+str(sums[0])+"</td></tr>\n"
  data += '</table></body>'
  filename = config.appdir+'/ucet_'+cart[1]+'.html';
  fstore = open(filename, 'w')
  fstore.write(data)
  fstore.close()
  #webbrowser.open(filename, context=osso_c)
