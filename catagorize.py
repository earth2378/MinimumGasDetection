# check that contract method is never success or not
def isNeverSuccess(cmStatus):
    for item in cmStatus:
        if(item[0] == 'S'): return False
    return True
# check that contract method contain only our of gas error or not

def isOnlyOutOfGas(cmStatus):
    for item in cmStatus:
        if(item[0] != 'G'): return False
    return True

# check that contract method has real minimum gas to run
# without out of gas error or not (no success in oog range)
def isFixMinimum(cmStatus):
    state = 1
    for item in cmStatus:
        if(item[0] == 'S' and state == 1): state = 2
        elif(item[0] == 'G' and state == 2): return False
    return True

# check that success and out of gas error have exactly same gas
def isSameGas(cmStatus):
    gas = 0
    for item in cmStatus:
        if(gas == 0):
            gas = item[1]
            continue
        if(gas != item[1]):
            return False
    return True

# No use
def isStatic(cmStatus):
    maxF = 0
    maxP = 0
    lastestP = 0
    p = 0
    for item in cmStatus:
        if(item[0] == 'G'):
            if(item[3] >= maxF):
                maxF = item[3]
                maxP = p
            lastestP = p
        p += 1
    if (maxP == lastestP): return True #static
    else: return False #dynamic
    
def checkType(cmStatus):
    if(isOnlyOutOfGas(cmStatus)): return('Only_Out_of_gas')
    elif(isNeverSuccess(cmStatus)): return('Never_Success')
    elif(isFixMinimum(cmStatus)): return('Fix_minimum')
    elif(isSameGas(cmStatus)): return('Same_gas')
    else: return('uncategorized')

def checkAllType(data):
    typee = dict()
    for row in data:
        t = checkType(data[row])
        if(not(t in typee)): typee[t] = []
        typee[t].append(row)
    for t in typee: print(t, len(typee[t]))