import pandas as pd
from os.path import join
import numpy as np



def read_csv(csvfile): 
    with open(csvfile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep="\t")
        #print(metadata.head())
        return metadata


def get_variability(metadata): 
    """
    For each author in the set, calculate a score that describes
    how much variability there is in the metadata of the 
    different novels by that author. 
    
    The variability will be minimal, if all three novels by a given author
    have been written in the same timeSlot, have the same reprint count
    and belong to same size category. It will be maximal if each novel 
    has a different value in each category. 
    
    The idea is that the lower that variance, the higher
    the uniformity or similarity of the novels by this one author is. 
    Consequently, this author should be relatively easy to recognize
    and the accuracy for this author should be high.      
    """
    variability = {}
    metadata = metadata.groupby("authorlabel")
    for name,group in metadata: 
        var_sizeCat = len(set(group.loc[:,"sizeCat"]))/3 # 3=max
        var_reprintCount = len(set(group.loc[:,"reprintCount"]))/2 #2=max
        var_timeSlot = len(set(group.loc[:,"time-slot"]))/3 # 3=max
        variability[name] = sum([var_sizeCat, var_reprintCount, var_timeSlot])
    variability = pd.Series(variability, name="var-author")
    #print(variability)
    return variability


def get_colldata(colldata): 

    """
    However, the variation between authors comes into play as well. 
    
    The more authors there are with a low variance, that is the 
    lower the mean variance is for an entire collection, the higher the
    accuracy for the entire collection should be. 
    
    However, this is true only if the individual value profiles of the
    authors differ from each other. This is tested in the next function.
    """
    print("empty")
    


def save_data(data, filename): 
    with open(filename, "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep="\t")



def main(langs): 
    colldata = {}
    for lang in langs: 
        csvfile = join("..", "metadata", lang+"_metadata.tsv")
        datafile = join("..", "hypotheses", lang+"_variability.tsv")
        metadata = read_csv(csvfile)
        variability = get_variability(metadata)
        save_data(variability, datafile)
        colldata[lang] = sum(variability) / len(variability)
    colldata = pd.Series(colldata, name="var-mean")
    save_data(colldata, join("..", "hypotheses", "collection-data.tsv"))


langs = ["eng", "fra", "hun", "nor", "por", "rom"]

main(langs)
