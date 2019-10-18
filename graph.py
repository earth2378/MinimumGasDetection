import matplotlib.pyplot as plt
import csv,time,ast,sys,os
import util as util
import catagorize as cat
import minimumGas as mg
from termcolor import colored
    
def createAxis(src):
    dstGas,dstCount = [],[]
    gasTmp = 0
    for txGas in src:
        if(txGas > gasTmp):
            dstGas.append(txGas)
            gasTmp = txGas
            dstCount.append(1)
        elif (txGas == gasTmp):
            dstCount[-1] += 1
        else:
            print(gasTmp, txGas)
    return dstGas, dstCount

def makeCumulative(lists):
    for l in lists:
        for i in range(len(l)):
            if(i == 0): continue
            else: l[i] += l[i-1]

def seperateTxStatus(csv_reader):
    g,s,r,i,j = [],[],[],[],[]
    for item in csv_reader:
        if(item[0] == 'G'): g.append(int(item[1]))
        elif(item[0] == 'S'): s.append(int(item[1]))
        elif(item[0] == 'R'): r.append(int(item[1]))
        elif(item[0] == 'I'): i.append(int(item[1]))
        elif(item[0] == 'J'): j.append(int(item[1]))
    return (g,s,r,i,j)

def saveGraph(cm,index,fig,dst):
    dst = dst + 'All\\'
    util.createDirectory(dst)
    fileName = str(index) + '_' + cm[0] + '_' + cm[1] + '.png'
    picDst = dst + fileName
    fig.savefig(picDst)

def saveGraphByMethod(cm,index,fig,dst):
    dst = dst + 'byMethod\\' + cm[1]
    util.createDirectory(dst)
    fileName = str(index) + '_' + cm[0] + '_' + cm[1] + '.png'
    picDst = dst + '\\' + fileName
    fig.savefig(picDst)

def saveGraphByType(cm,index,fig,dst,typee):
    dst = dst + 'byType\\' + typee
    util.createDirectory(dst)
    fileName = str(index) + '_' + cm[0] + '_' + cm[1] + '.png'
    picDst = dst + '\\' + fileName
    fig.savefig(picDst)

def plotTxStatusGraph(fig,cm,xlog=False,ylog=False,cumulative=True,split=False):
    file = 'cm\\' +  cm[0] + '_' + cm[1] + '.csv'
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')

    (g, s, r, i, j) = seperateTxStatus(csv_reader)
    gGas,gCount = createAxis(g)
    sGas,sCount = createAxis(s)
    rGas,rCount = createAxis(r)
    iGas,iCount = createAxis(i)
    jGas,jCount = createAxis(j)
    
    if(split):sCount = [0-i for i in sCount]
    if (cumulative):makeCumulative([gCount,sCount,rCount,iCount,jCount]) 
        
    fig.step(gGas, gCount, marker='.', markersize=3, linewidth=1, where='post', color='red', label="Out of gas") 
    fig.step(sGas, sCount, marker='.', markersize=3, linewidth=1, where='post', color='green', label="Success") 
    fig.step(rGas, rCount, marker='.', markersize=3, linewidth=1, where='post', color='cyan', label="Reverted")
    fig.step(iGas, iCount, marker='.', markersize=3, linewidth=1, where='post', color='black', label="Bad instruction") 
    fig.step(jGas, jCount, marker='.', markersize=3, linewidth=1, where='post', color='yellow', label="Bad jump destination")
    
    fig.grid()
    fig.legend()
    fig.set_xlabel('Gas')
    fig.set_ylabel('Count')
    fig.title.set_text('Success Rate_'+str(cm))
    if (xlog):fig.set_xscale('log')
    if (ylog and not split):fig.set_yscale('log')
    csv_file.close()  

def plotSuccessRateGraph(fig,cm,xlog=False,ylog=False):
    file = 'cm\\' +  cm[0] + '_' + cm[1] + '.csv'
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    goh,soh = mg.overheadTx(csv_reader)
    rate = mg.successFromOH(goh,soh)
    
    
    fig.grid()
    fig.scatter(goh[0], rate, s=2, alpha=1, color='#006400', label="Success rate")
    fig.legend()
    fig.set_xlabel('Gas')
    fig.set_ylabel('Success Rate (%)')
    fig.title.set_text('Success Rate_'+str(cm))
    if (xlog):fig.set_xscale('log')
    if (ylog):fig.set_yscale('log')
    csv_file.close()  

def plotTimestampGraph(fig,cm,xlog=False,ylog=False):
    file = 'cmt_filter\\' +  cm[0] + '_' + cm[1] + '.csv'
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    gg,gt,sg,st = [],[],[],[]
    for row in csv_reader:
        if(row[0] == 'S'):
            sg.append(int(row[1]))
            st.append(int(row[3]))
        elif(row[0] == 'G'):
            gg.append(int(row[1]))
            gt.append(int(row[3]))

    gc = mg.cumulativeTimpstamp(gt)
    sc = mg.cumulativeTimpstamp(st)

    lns1 = fig.scatter(gt, gg, s=2, alpha=.2, color='red', label="Out of gas") 
    lns2 = fig.scatter(st, sg, s=2, alpha=.2, color='green', label="Success") 
    fig.grid()
    fig.set_xlabel('Block Number')
    fig.set_ylabel('Gas (Scatter)')

    figR = fig.twinx()
    lns3 = figR.step([i[0] for i in gc],[i[1] for i in gc], marker='', linewidth=1, where='post', color='#FF6666', label="Out of gas")
    lns4 = figR.step([i[0] for i in sc],[i[1] for i in sc], marker='', linewidth=1, where='post', color='#32CD32', label="Success")
    figR.set_ylabel('Count (Step)')

    lns = [lns1,lns2,lns3[0],lns4[0]]
    labs =[]
    for l in lns:
        try:
            labs.append(l.get_label())
        except:
            print('??')
    fig.legend(lns, labs, loc=0)
    
    csv_file.close()


def plotAll(cm,txStatus,index,dst,xlog=False,ylog=False,cumulative=True,split=False):
    if(dst == 'cmPic2\\Step\\'):
        fig, axs = plt.subplots(1, 2,figsize=(20,10))
        plotTxStatusGraph(axs[0],cm,xlog,ylog,cumulative,split)
        plotSuccessRateGraph(axs[1],cm,xlog,ylog)
    if(dst == 'cmPic3\\Step\\'):
        fig, axs = plt.subplots(2, 2,figsize=(20,20))
        for ax in axs[1, :]:
            ax.remove()
        gs = axs[1, 1].get_gridspec()
        axs_2 = fig.add_subplot(gs[1,: ])
        plotTxStatusGraph(axs[0,0],cm,xlog,ylog,cumulative,split)
        plotSuccessRateGraph(axs[0,1],cm,xlog,ylog)
        plotTimestampGraph(axs_2,cm,xlog,ylog)
    
    
    saveGraph(cm,index,fig,dst)
    saveGraphByType(cm,index,fig,dst,cat.checkType(txStatus))
    saveGraphByMethod(cm,index,fig,dst)
    plt.clf()
    plt.close()

    return True

def cmSelect(index,data):
    counter = 0
    for cm in data:
        if(index == counter):
            print(cm,cat.checkType(data[cm]))
            for i in data[cm]:
                if(i[0] == 'G'):   print(colored(i,'red'))
                elif(i[0] == 'S'): print(colored(i,'green'))
                elif(i[0] == 'R'): print(colored(i,'cyan'))
                else: print(i)
            break
        counter += 1
    
    #interest 135, 136, 139, 420, 1000,
    