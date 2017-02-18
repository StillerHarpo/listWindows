#!/usr/bin/env python2
from wmctrl import Window as W
from subprocess import call
import psutil
import curses

def getStrings():
    stdscr.clear()
    windows=W.list()
    keys=["f","j","d","k","s","l","a"] # keys to chose the window
    keyComb=[] # generate a key Combination for each window
    if (len(keys)<len(windows)): 
        count=0
        isBreak=False
        for i in keys:
            for j in keys:
                if (count==len(windows)):
                    break
                    isBreak=True
                keyComb.append(i+j)
                count+=1
            if isBreak:
                break
    else:
        keyComb=keys[0:len(windows)]
    actice= W.get_active() # dont show this program
    count=0
    for win in windows:
        if win == actice:
            del windows[count]
            break
        count+=1
    windowNames=[] # get the correct name for programs in terminals
    for win in windows:
        name=win.wm_name
        pids=[win.pid]
        if (name=="termite"): # TODO make it portable for other terminals
            pids=psutil.Process(pids[0]).children()
            if(len(pids)>0 ):
                name=pids[0].name()
                if  (name=="zsh"): # TODO make it portable for other shells
                    pids=pids[0].children()
                    if(len(pids)>0 ):
                        name=pids[0].name()
        windowNames.append(name)        
    ws=[x.desktop for x in windows]
    windowNumber=[0]*(max(ws)+1)
    for i in (ws):
        windowNumber[i]+=1
    count=0
    countL=0
    countWs=0
    for i in windowNumber: # print the lines
        if(i%2==0):
            middle=(i/2)
        else:
            middle=((i+1)/2)
        for j in range(i):
            if(j==middle-1):
                stdscr.addstr(countL,0,str(countWs)+"| ["+keyComb[count]+"]: "+windowNames[count])
            else:
                stdscr.addstr(countL,0," | ["+keyComb[count]+"]: "+windowNames[count])
            count+=1
            countL+=1
        if(i!=0):
            countL+=1 # print a empty line between workspaces
        countWs+=1
    stdscr.refresh()
    return keyComb , [ x.id for x in windows], ws

stdscr = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()

keyComb, winID, ws = getStrings()
savedWsFile=open("/var/tmp/notifyWindows")
savedWs=eval(savedWsFile.read())
savedWsFile.close()
savedWsFile=open("/var/tmp/notifyWindows", 'w')
while True:
    c = stdscr.getch()
    if c == ord('q'): # close this programm
        savedWsFile.write(str(savedWs))
        break
    elif c == ord('n'): # focus the next empty workspace
        for i in range(0,len(ws)):
            if not i in ws:
                call(["wmctrl","-s", str(i)])
                savedWs[0]=i+1
                savedWsFile.write(str(savedWs))
                break
        break
    elif c == ord('x'): # close the window
        count=0
        if keyComb[0]=="f":
            c = stdscr.getch()
            for i in keyComb:
                if ord(i[0])==c: 
                    call(["wmctrl","-ic", str(winID[count])])
                    keyComb, winID, ws= getStrings()
                    break
                count+=1
        else:
            c1 = stdscr.getch()
            c2 = stdscr.getch()
            for i in keyComb:
                if ord(i[0])==c1 and ord(i[1])==c2: 
                    call(["wmctrl","-ic", str(winID[count])])
                    keyComb, winID, ws= getStrings()
                    break
                count+=1
        continue
    else: # focus the window
        count=0
        isBreak=False
        if keyComb[0]=="ff":
            c1=c
            c2=stdscr.getch()
            for i in keyComb:
                if ord(i[0])==c1 and ord(i[1])==c2: 
                    call(["wmctrl","-ia", winID[count]])
                    savedWs[0]=ws[count]+1
                    savedWsFile.write(str(savedWs))
                    isBreak=True
                    break 
                count+=1
        else:
            for i in keyComb:
                if ord(i[0])==c: 
                    stdscr.refresh()
                    call(["wmctrl","-ia", winID[count]])
                    savedWs[0]=ws[count]+1
                    savedWsFile.write(str(savedWs))
                    isBreak=True
                    break 
                count+=1
        if isBreak:
            break
savedWsFile.close()
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

