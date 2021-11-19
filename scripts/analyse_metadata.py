
"""
== Analyse metadata == 

This script serves to derive information from the metadata of text 
collections that permit to predict the level of difficulty that the
text collection presents for authorship attribution. 

"""

# === Import statements === 

import pandas as pd
from os.path import join
import numpy as np
import re
from sklearn import preprocessing as sp
import matplotlib.pyplot as plt


# === Functions === 

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
    
    Note that for novels where no year of first publication is known, 
    the value 1880 is used as a very rough approximation, as this is 
    the year that is in the middle of the overall period covered by 
    our collections, which is 1840-1920. 
          
    """
    variability = {}
    metadata = metadata.groupby("authorlabel")
    for name,group in metadata: 
        #print(name)
        # Publication year data is often incomplete / inconsistent
        year_Pub = []
        for year in list(group.loc[:,"firsted-yr"]):
            try: 
                year = int(re.findall("\d\d\d\d", str(year))[0])
                year_Pub.append(year)
            except: 
                year_Pub.append(1880)
        var_yearPub = np.std(year_Pub)
        var_numWords = np.std(group.loc[:,"numwords"])
        var_sizeCat = len(set(group.loc[:,"sizeCat"]))
        var_reprintCount = len(set(group.loc[:,"reprintCount"]))
        var_timeSlot = len(set(group.loc[:,"time-slot"]))
        variability[name] = [var_yearPub, var_numWords, var_sizeCat, var_reprintCount, var_timeSlot]
    variability = pd.DataFrame(variability).T
    variability.columns = ["yearPub", "numWords", "sizeCat", "reprintCount", "timeSlot"]
    # Scaling of each column to make values comparable and aggregateable
    scaler = sp.MinMaxScaler()
    variability = pd.DataFrame(scaler.fit_transform(variability), columns=variability.columns, index=variability.index)
    # Create an aggregate value, here a simple unweighted mean for each author
    variability["aggregated"] = np.mean(variability, axis=1)
    variability.sort_values("aggregated", ascending=False, inplace=True)
    print(variability)
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
    

def save_data(data, datafile): 
    with open(datafile, "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep="\t")


def plot_data(data, lang, datafile): 
    data.sort_values("aggregated", ascending=False, inplace=True)
    ax = data["aggregated"].plot.barh(title="Intra-author text similarities for ELTeC-" + lang)
    ax.set_xlabel("Aggregated intra-author text similarity score")
    ax.set_ylabel("Author names")
    plt.savefig(datafile[:-4] + ".png", dpi=300, bbox_inches="tight", pad_inches=0.2)


# === Main === 

def main(langs): 
    colldata = {}
    for lang in langs: 
        print(lang)
        metadatafile = join("..", "metadata", lang+"_metadata.tsv")
        variabilityfile = join("..", "hypotheses", lang+"_variability.tsv")
        metadata = read_csv(metadatafile)
        variability = get_variability(metadata)
        save_data(variability, variabilityfile)
        plot_data(variability, lang, variabilityfile)
        #colldata[lang] = sum(variability) / len(variability)
    #colldata = pd.Series(colldata, name="var-mean")
    #save_data(colldata, join("..", "hypotheses", "collection-data.tsv"))


langs = ["deu"]
langs = ["deu", "eng", "fra", "hun", "nor", "pol", "por", "rom"]

main(langs)
