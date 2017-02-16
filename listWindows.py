from wmctrl import Window as W
import psutil
windows=W.list()
windowsDict=[ x._asdict for x in windows]
keys=["f","j","d","k","s","l","a"] # keys to chose the window
keyComb=[] # generate a key Combination for each window
if (len(keys)<len(windows)): 
    count=0
    isBreak=False
    for i in keys:
        for j in keys:
            keyComb.append(i+j)
            count+=1
            if (count==len(windows)):
                break
                isBreak=True
        if isBreak:
            break
else:
    keyComb=keys[0:len(windows)]
windowNames=[] # get the correct name for programs in terminals
for win in windowsDict:
    name=win["wm_name"]
    pids=[win["pid"]]
    if (name=="termite"): # TODO make it portable for other terminals
        pids=psutil.Process(pids[0]).children()[0]
        if(ln(pids)>0 ):
            name=psutil.Process(pids[0]).name()
            if  (name=="zsh"): # TODO make it portable for other shells
                pids=psutil.Process(pids[0]).children()[0]
                if(ln(pids)>0 ):
                    name=psutil.Process(pids[0]).name()
    windowNames.append(name)        
ws=[x[desktop] for x in windowsDict]
windowNumber=[0]*(max(ws)+1)
for i in (ws):
    windowNumber[i]+=1

lines=[] # save line outputs in array
count=0
for i in windowNumber:
    if(i%2==0):
        middle=(i/2)
    else:
        middle=((i+1)/2)
    for j in range(i):
        if(j==middle):
            lines.append(i+"| ["+keyComb[count]+"]: "+windowNames[count])
        else:
            lines.append(" | ["+keyComb[count]+"]: "+windowNames[count])
        count+=1
    lines.append("")
