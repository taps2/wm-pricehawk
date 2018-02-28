import tkinter as tk
import re
import requests
import threading
import json
import tkinter.messagebox
import os.path
import numpy as np
from tkinter import ttk
from tkinter.ttk import Progressbar

np.set_printoptions(threshold=np.nan)

window = tk.Tk()
window.title("WM PriceHawk")
window.geometry('400x200')
lbl = tk.Label(window, text="Zip code: ")
lbl.grid(column=0, row=0)
zip = tk.Entry(window,width=10)
zip.grid(column=1, row=0)
lbl = tk.Label(window, text="SKU1: ")
lbl.grid(column=0, row=2)
SKU1 = tk.Entry(window,width=10)
SKU1.grid(column=1, row=2)
lbl = tk.Label(window, text="Price point: ")
lbl.grid(column=2, row=2)
SKU1pp = tk.Entry(window,width=10)
SKU1pp.grid(column=3, row=2)
lbl = tk.Label(window, text="SKU2: ")
lbl.grid(column=0, row=3)
SKU2 = tk.Entry(window,width=10)
SKU2.grid(column=1, row=3)
lbl = tk.Label(window, text="Price point: ")
lbl.grid(column=2, row=3)
SKU2pp = tk.Entry(window,width=10)
SKU2pp.grid(column=3, row=3)
lbl = tk.Label(window, text="SKU3: ")
lbl.grid(column=0, row=4)
SKU3 = tk.Entry(window,width=10)
SKU3.grid(column=1, row=4)
lbl = tk.Label(window, text="Price point: ")
lbl.grid(column=2, row=4)
SKU3pp = tk.Entry(window,width=10)
SKU3pp.grid(column=3, row=4)
lbl = tk.Label(window, text="Timer: ")
lbl.grid(column=0, row=5)
timetowait = tk.Entry(window,width=10)
timetowait.grid(column=1, row=5)

callback = None
sec = None
timer = tk.Label(window, fg='green')
timer.grid(column=3, row=6)
storeno = None
name = None
price = None
count = None

def tick():
        global callback
        global sec
        if( sec <= 0 ):
                window.after_cancel(callback)
                start_clicked_thread(None)
        else:
                sec -= 1
                timer['text'] = sec
                callback = window.after(1000, tick)
                print(sec)

        
def clicked():
        global sec
        sec = int(timetowait.get())
        zipurl = 'http://api.walmartlabs.com/v1/stores?apiKey= ****APICODEGOESHERE**** &zip=' + zip.get() + '&format=json'
        resp2 = requests.get(zipurl)
        #dt = np.dtype([('storeno', np.unicode_, 35), ('name',  np.unicode_, 35), ('price', int), ('count', np.int16)])
        itemlist = np.empty((0,4))
        skus = []
        if len(SKU1.get()) != 0:
                skus.append(SKU1.get())
        if len(SKU2.get()) != 0:
                skus.append(SKU2.get())
        if len(SKU3.get()) != 0:
                skus.append(SKU3.get())
        
        stores = re.findall('(?<="no":)\d+', resp2.text)
        progbarlength = len(stores)
        
        for store in stores:
                print('Store # ' + store)
        for sku in skus:
                print('SKU # ' + sku)
        for store in stores:
                for sku in skus:
                        url = 'http://search.mobile.walmart.com/search?query=' + sku + '&store=' + store + ''
                        resp = requests.get(url)
                        data = json.loads(resp.text)
                        for d in data['results']:
                                try:
                                        priceincents = d['price']['priceInCents']
                                        count = d['inventory']['quantity']
                                        name = d['name']
                                except:
                                        count = None
                                        priceincents = None
                                        name = None
                        bar['value'] = ((stores.index(store)*100)/progbarlength)
                        try:
                                priceincents
                        except:
                                count = None
                                priceincents = None
                                name = None
                        if priceincents is not None and count is not None and name is not None:
                                print("store : ", int(store))
                                #print(type(store))
                                print("count : ", count)
                                #print(type(count))
                                print("name  : " + name)
                                #print(type(name))
                                print("price  : ", priceincents)
                                #print(type(priceincents))
                                itemlist = np.append(itemlist, [[store, name, priceincents, count]], axis = 0)
                                count = None
                                priceincents = None
                                name = None
                if os.path.exists("sku1.txt"):
                        file = open("sku1.txt")
                        data = file.read()
                        file.close()
                        lbl2 = tk.Label(window, text = data)
                        lbl2.grid(column=0, row=5)
        #dt = np.dtype[('storeno', np.int16), ('name', 'U25'), ('price', np.int16), ('count', np.int16)]
        #b = np.array(a, dtype=dt)
        #b = np.sort(b, order=['name', 'price', 'count'])
        print(itemlist)
        bar['value'] = 0
        tick()

def start_clicked_thread(event):
    global clicked_thread
    clicked_thread = threading.Thread(target=clicked)
    clicked_thread.daemon = True
    clicked_thread.start()
    window.after(20, check_clicked_thread)

def check_clicked_thread():
    if clicked_thread.is_alive():
        window.after(20, check_clicked_thread)
    else:
        bar.stop()

btn = tk.Button(window, text="Get Prices", bg="orange", fg="red", command = lambda:start_clicked_thread(None))
btn.grid(column=1, row=7)

 
bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')

bar.grid(column=1, row=6)

window.mainloop()

