
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
import itertools


# === Functions === 

def read_csv(csvfile): 
    with open(csvfile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep="\t")
        #print(metadata.head())
        return metadata


def get_author_variability(metadata): 
    """
    For each author in the set, calculate a score that describes
    how much variability there is in the metadata of the 
    different novels by that author. 
    
    The variability will be minimal, if all three novels by a given author
    have been written in the same timeSlot / published in the same year, 
    have the same reprint count and belong to same size category / have 
    very similar lengths in words. It will be maximal if each novel 
    has a different value in each category. 
    
    The idea is that the lower that variance, the higher
    the uniformity or similarity of the novels by this one author is. 
    Consequently, this author should be relatively easy to recognize
    and the accuracy for this author should be high.
    
    Note that for novels where no year of first publication is known, 
    the value 1880 is used as a very rough approximation, as this is 
    the year that is in the middle of the overall period covered by 
    our collections, which is 1840-1920. 
    
    Variance is calculated for each category, either by looking at the
    number of different values (for the categorical values) or at the
    standard deviation of the values (for the continuous variables), then
    normalized to a range of 0-1 using a min/max scaler, and aggregated
    to a single score using an unweighted mean. 
          
    """
    author_var = {}
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
        author_var[name] = [var_yearPub, var_numWords, var_sizeCat, var_reprintCount, var_timeSlot]
    author_var = pd.DataFrame(author_var).T
    author_var.columns = ["yearPub", "numWords", "sizeCat", "reprintCount", "timeSlot"]
    # Scaling of each column to make values comparable and aggregateable
    scaler = sp.MinMaxScaler()
    author_var = pd.DataFrame(scaler.fit_transform(author_var), columns=author_var.columns, index=author_var.index)
    # Create an aggregate value, here a simple unweighted mean for each author
    author_var["aggregated"] = np.mean(author_var, axis=1)
    author_var["prediction"] = 1-author_var["aggregated"]
    author_var.sort_values("prediction", ascending=True, inplace=True)
    #print(author_var)
    return author_var


def get_colldata(lang, metadata, author_var): 

    """
    However, the variation between authors comes into play as well. 
    
    The more authors there are with a low variance, that is the 
    lower the mean variance is for an entire collection, the higher the
    accuracy for the entire collection should be. 
    
    However, this is true only if the individual value profiles of the
    authors differ from each other. This is also tested in this function.
    
    
    """
    one_coll_var = {}
    # Mean collection-level variability
    one_coll_var["mean_var"] = np.mean(author_var["aggregated"])
    
    # Degree of difference between author metadata profiles    
    metadata = metadata.groupby("authorlabel")
    means_timeSlot = []
    means_sizeCat = []
    means_reprintCount = []
    means_yearPub = []
    means_numWords = []
    for name,group in metadata: 
        #print(name)
        yearPub = []
        for year in list(group.loc[:,"firsted-yr"]):
            try: 
                year = int(re.findall("\d\d\d\d", str(year))[0])
                yearPub.append(year)
            except: 
                yearPub.append(1880)
        # Calculate means
        means_yearPub.append(np.mean(yearPub))
        means_numWords = group.loc[:,"numwords"]
        num_timeSlot, cat_timeSlot = pd.factorize(group.loc[:,"time-slot"])
        means_timeSlot.append(np.mean(num_timeSlot))
        num_sizeCat, cat_sizeCat = pd.factorize(group.loc[:,"sizeCat"])
        means_sizeCat.append(np.mean(num_sizeCat))
        num_reprintCount, cat_reprintCount = pd.factorize(group.loc[:,"reprintCount"])
        means_reprintCount.append(np.mean(num_reprintCount))
    #print(means_timeSlot)
    one_coll_var["mean_diffs_yearPub"] = np.mean([abs(e[1] - e[0]) for e in itertools.permutations(means_yearPub, 2)])   
    one_coll_var["mean_diffs_numWords"] = np.mean([abs(e[1] - e[0]) for e in itertools.permutations(means_numWords, 2)])   
    one_coll_var["mean_diffs_timeSlot"] = np.mean([abs(e[1] - e[0]) for e in itertools.permutations(means_timeSlot, 2)])   
    one_coll_var["mean_diffs_sizeCat"] = np.mean([abs(e[1] - e[0]) for e in itertools.permutations(means_sizeCat, 2)])
    one_coll_var["mean_diffs_reprintCount"] = np.mean([abs(e[1] - e[0]) for e in itertools.permutations(means_reprintCount, 2)])
    
    # Make df
    one_coll_var = pd.Series(one_coll_var, name=lang)
    #print(one_coll_var, "\n")   
    return one_coll_var  
    

def save_data(data, datafile): 
    with open(datafile, "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep="\t")


def plot_author_data(data, lang, datafile): 
    data.sort_values("prediction", ascending=False, inplace=True)
    ax = data["prediction"].plot.barh(title="Predicted attribution accuracy for ELTeC-" + lang)
    ax.set_xlabel("Predicted accuracy = 1 - mean intra-author text similarity")
    ax.set_ylabel("Author names")
    plt.savefig(datafile[:-4] + ".png", dpi=300, bbox_inches="tight", pad_inches=0.2)


def plot_coll_data(coll_var): 
    coll_var.sort_values("prediction", ascending=False, inplace=True)
    ax = coll_var["prediction"].plot.barh(title="Predicted attribution accuracy for ELTeC benchmark dataset")
    ax.set_xlabel("Predicted accuracy = mean between-author similarity")
    ax.set_ylabel("ELTeC collections")
    plt.savefig(join("..", "hypotheses", "collection-variability.png"), dpi=300, bbox_inches="tight", pad_inches=0.2)


# === Main === 

def main(langs): 
    coll_var = {}
    for lang in langs: 
        print(lang)
        metadata_file = join("..", "metadata", lang+"_metadata.tsv")
        author_variability_file = join("..", "hypotheses", lang+"_variability.tsv")
        metadata = read_csv(metadata_file)
        author_var = get_author_variability(metadata)
        save_data(author_var, author_variability_file)
        plot_author_data(author_var, lang, author_variability_file)
        coll_var[lang] = get_colldata(lang, metadata, author_var)
    coll_var = pd.DataFrame(coll_var).T
    scaler = sp.MinMaxScaler()
    coll_var = pd.DataFrame(scaler.fit_transform(coll_var), columns=coll_var.columns, index=coll_var.index)
    coll_var["aggregated"] = np.mean(coll_var, axis=1)
    coll_var["prediction"] = coll_var["aggregated"] # identical in this case
    coll_var.sort_values("prediction", ascending=True, inplace=True)
    save_data(coll_var, join("..", "hypotheses", "collection-variability.tsv"))
    plot_coll_data(coll_var)


#langs = ["deu"]
#langs = ["deu", "fra"]
langs = ["deu", "eng", "fra", "hun", "nor", "pol", "por", "rom"]

main(langs)
