#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scribus as sc
from scribus import ICON_INFORMATION,BUTTON_YES,BUTTON_NO

def hjust():
    ram = sc.getSelectedObject()
    w,h = sc.getSize(ram)

    while not sc.textOverflows(ram) and (h > 0):
        h -= 10
        sc.sizeObject(w,h,ram)
    
    while sc.textOverflows(ram):
        h += 1
        sc.sizeObject(w,h,ram)
    
def vjust():
    ram = sc.getSelectedObject()
    w,h = sc.getSize(ram)

    while not sc.textOverflows(ram) and (w > 0):
        w -= 10
        sc.sizeObject(w,h,ram)
    
    while sc.textOverflows(ram):
        w += 1
        sc.sizeObject(w,h,ram)
        
hjust()

val=sc.messageBox("Justera","Bara höjd?",ICON_INFORMATION,BUTTON_YES,BUTTON_NO)
if val == 65536:
    vjust()