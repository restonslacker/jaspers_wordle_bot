import pandas as pd
import numpy as np

def get_feedback(word, answer):
    """
    Gives user feedback on word

    Parameters
    ----------
    word : str
        guessed word
    answer : str
        answer to wordle

    Returns
    -------
    response : int
        the integer number of the response bin (0, 242)
    """
    
    response = 0
    recheck_idx =[]
    for index, item in enumerate(word):
        if item == answer[index]:
            response += (3**index)*2
        else:
            recheck_idx.append(index)
    alist = []
    for j in recheck_idx:
        alist.append(list(answer)[j])
    for index, item in enumerate(word):
        if (index in recheck_idx) and ( item in alist):
            response += (3**index)
            alist.remove(item)
        
    return response


def next_wordle(guess, response, wrds):
    """prints the list of words and the sizes of their largest bins
    for words that have the biggest median bin size

    Args:
        guess (str): what you said
        response (str): what they said ('0' for grey, '1' for yellow, '2' for green, e.g. '00112')
        wrds (pandas): some big stupid dataframe
    """
    bin =0 
    for idx, i in enumerate(response):
        bin += int(i)*(3**idx)
    
    round2 = wrds.query("words_x==@guess & bin==@bin").copy(deep=True).drop('words_x',1)
    round2_1 = round2.copy(deep=True)
    round2 = pd.merge(round2,round2_1, on='bin')
    round2['bin'] = round2.apply(lambda x: get_feedback(x[0],x[2]), axis=1)
    pt = round2.pivot_table(index='bin',columns='words_y_x',aggfunc=np.size)
    ptmd = pt.median()
    ptmx = pt.max()
    nxt = ptmx[ptmd==ptmd.max()]
    print(nxt)

# wrds = pd.read_csv("./words.txt")
# wrds['key'] = 1
# wrds2 = wrds.copy(deep=True)

# wrds = pd.merge(wrds, wrds2, on='key').drop('key',1)
# print(wrds.shape)

# wrds['bin']=wrds.apply(lambda x: get_feedback(x[0],x[1]), axis=1)
# wrds.to_csv("wrd_outputs.csv")
wrds = pd.read_csv("wordle/wrd_outputs.csv",index_col=0)
next_wordle('pique','00001',wrds)
