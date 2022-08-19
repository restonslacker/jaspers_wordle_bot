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



# wrds = pd.read_csv("./words.txt")
# wrds['key'] = 1
# wrds2 = wrds.copy(deep=True)

# wrds = pd.merge(wrds, wrds2, on='key').drop('key',1)
# print(wrds.shape)

# wrds['bin']=wrds.apply(lambda x: get_feedback(x[0],x[1]), axis=1)
# wrds.to_csv("wrd_outputs.csv")
wrds = pd.read_csv("wrd_outputs.csv",index_col=0)
pt = wrds.pivot_table(index='bin',columns='words_x',aggfunc=np.size)
pt.median()

round2 = wrds.query("words_x=='pique' & bin==54").copy(deep=True).drop('words_x',1)
round2_1 = round2.copy(deep=True)
round2 = pd.merge(round2,round2_1, on='bin')
round2['bin'] = round2.apply(lambda x: get_feedback(x[0],x[2]), axis=1)
pt = round2.pivot_table(index='bin',columns='words_y_x',aggfunc=np.size)
meds = pt.median()