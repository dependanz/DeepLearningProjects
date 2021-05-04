import numpy as np

def crossentropy_loss(y,yhat):
    loss = 0
    if len(yhat) != len(y):
        return

    for i in range(len(yhat)):
        if(yhat[i] < 0):
            yhat[i] = 0

    for i in range(len(yhat)):
        loss += -(y[i] * np.log(yhat[i])) - (1-y[i])*np.log(1-yhat[i])
    return loss/len(y)

def mean_squared_error(y,yhat):
    loss = 0
    #print(yhat)
    if len(yhat) != len(y):
        return

    for i in range(len(y)):
        l = 0
        for j in range(len(y[i])):
            l += (y[i][j] - yhat[i][j]) ** 2
        l = l/len(yhat[i])
        loss += l
    return loss / len(y)

def collapse_list_of_lists(l,s=False,key=None):
    collapsed = []
    for i in l:
        collapsed += i
    if(s):
        collapsed.sort(key=key)
    return collapsed

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r",off=False):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    if(off): return iterable
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()
