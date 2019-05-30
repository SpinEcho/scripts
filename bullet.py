#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Format selected paragraphs with bullets.
Author: prof. MS. José Antonio Meira da Rocha
mailto:joseantoniomeira@gmail.com
http://meiradarocha.jor.br
License GPL 2.0
2011-01-14b

======
Usage:
Select paragraphs at any points. Run script.
Caveats:
* Cleans all text format of text selection (font, bold, subscript, etc).
* Creates paragraph style "Bullet", if it doesn't exist.
* If there is no selection, apply bullets to all text in current frame.
"""

import sys,scribus
    
from scribus import BUTTON_OK,ICON_WARNING,ICON_INFORMATION,BUTTON_YES,BUTTON_NO

punkt=""

#############
#Välja tecken

def punktval():
    global punkt
    val=scribus.messageBox("Punktval","Standard?",ICON_INFORMATION,BUTTON_YES,BUTTON_NO)
    if val = 16384:
        punkt = "• "
    else:
        while True:
            inmatning = scribus.valueDialog("Inmatning","Skriv in hexkod: ")
            tal=int(inmatning,16)
            if tal < 128:
                break
            scribus.messageBox("Fel!","Större än 128",ICON_WARNING)
        
        punkt = chr(tal)+" "

##########################
# Get text cursor position
def getTextCursor(ram):
    '''Find position of text cursor in text frame.
    Text need to be selected.'''
    selectedFrame = scribus.getSelectedObject()
    try:
        selectedText = scribus.getText()
    except:
        scribus.messageBox(scriptWindowTitle,wrongFrameTypeErrorMsg,ICON_WARNING,BUTTON_OK)
        sys.exit()
    scribus.deselectAll()
    allText = scribus.getAllText(selectedFrame)
    
    if allText.count(unicode(selectedText)) == 1:
        cur = allText.find(unicode(selectedText))
        return cur,allText,selectedText
    else:
        scribus.messageBox(scriptWindowTitle,askSelectMoreText,ICON_WARNING,BUTTON_OK)
        sys.exit(1)

###################
def cleanBullets(t):
    '''Delete bullets.'''
    global punkt
    while t.count(punkt):
        t = t.replace(punkt,'')
    return t

######################
# Get paragraph begin
def getParagraphLimits(cur,allText,selectedText,ram):
    '''Get paragraph begin/end and delete old bullets'''
    # Get selected paragraph begin
    # (last line break position after selection, plus 1)
    begin = allText.rfind(u'\r',0,cur)+1 # Why not '\n'?
    # Get selection end
    end = cur+len(unicode(selectedText))
    scribus.selectText(begin,(end - begin),ram)
    selectedText = scribus.getText(ram)
    # Clean old bullets
    cleanedText = cleanBullets(unicode(selectedText))
    scribus.deleteText(ram)
    scribus.insertText(cleanedText,begin,ram)
    
    # Text was modified. Get all text again.
    scribus.deselectAll()
    allText = scribus.getAllText(ram)
    # Get selection new end
    end = begin+len(unicode(cleanedText))
    return begin,end,allText

############################
# Do all the job
def skrivapunkter(ram):
    '''Insert bullets in front selected paragraphs.'''
    global punkt
    cur,allText,selectedText = getTextCursor(ram)
    begin,end,allText = getParagraphLimits(cur,allText,selectedText,ram)
    # Insert bullets
    bulletsLen = 0
    bl = len(unicode(punkt)) # len() needs unicode()
    nextPoint = begin
    while True:
        scribus.insertText(punkt,begin,ram)
        bulletsLen = bulletsLen + bl  # total strings inserted lenght
        nextPoint = allText.find(u'\r',nextPoint+1,end)
        if nextPoint == -1: break
        begin = nextPoint + bulletsLen + 1

#####################
def handleSelected():
    """Handle frame selection."""
    ram = scribus.getSelectedObject()
    if ram: 
        punktval()
        skrivapunkter(ram)
        scribus.docChanged(True)
    else:
        scribus.messageBox("Fel!","Ingen ram vald",ICON_WARNING)

############### 
def main(argv):
    scribus.setRedraw(False)
    handleSelected()

#######################
def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

if __name__ == '__main__':
    main_wrapper(sys.argv)
