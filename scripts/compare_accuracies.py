
"""
== Compare accuracies == 

This script compares predicted and empirical accuracies.

"""

# === Import statements === 

import pandas as pd
from os.path import join
import numpy as np
import re
import pygal


# === Functions === 

def get_predicted(csvfile): 
    with open(csvfile, "r", encoding="utf8") as infile: 
        predicted = pd.read_csv(infile, sep="\t", index_col=0)
        predicted = predicted.loc[:,"prediction"]
        predicted.sort_index(inplace=True)
        predicted = predicted.sort_values(ascending=False)        
        predicted = predicted.rename("predicted")
        #print(predicted)
        return predicted


def get_empirical(csvfile, lang, mfw): 
    with open(csvfile, "r", encoding="utf8") as infile: 
        empirical = pd.read_csv(infile, sep=",", index_col=0)
        empirical = empirical[empirical.index.str.contains(lang+"_")]
        empirical = empirical.loc[:,str(mfw)]
        empirical.index = empirical.index.str.replace(lang, "")
        empirical.index = empirical.index.str.replace("_", "")
        empirical = empirical.sort_values(ascending=False)
        empirical = empirical.rename("empirical")
        #print(empirical)
        return empirical


def compare_accuracies(lang, predicted, empirical): 
    matrix = np.corrcoef(predicted, empirical)
    pearsonsr = matrix[0,1]
    print(lang, pearsonsr)
    return np.round(pearsonsr, 3)


def visualize_correlation(lang, predicted, empirical, pearsonsr): 
    combined = pd.concat([predicted, empirical], axis=1)
    #print(combined.head())
    plot = pygal.XY(legend_at_bottom=True, range=(0.5,1))
    plot.title ="Predicted and empirical accuracies for " + lang + " (Pearson's R: " +str(pearsonsr)+ ")"
    plot.x_title = "Predicted accuracies"
    plot.y_title = "Empirical accuracies"
    for row in combined.iterrows(): 
        label = row[0]
        values = (np.round(row[1]["predicted"],2), np.round(row[1]["empirical"],2))
        plot.add(label, [values], dots_size=6)
    plot.render_to_file(join("..", "results", lang + "_combined.svg"))
        



# === Parameters === 

#langs = ["deu"]
langs = ["deu", "fra"]
langs = ["deu", "eng", "fra", "hun", "nor", "por", "rom"]

mfw = 1640

# === Main === 

def main(langs, mfw): 
    for lang in langs: 
        #print(lang)
        predicted_file = join("..", "hypotheses", lang+"_variability.tsv")
        empirical_file = join("..", "results", "results_authors_acc_wurzburg.csv")
        predicted = get_predicted(predicted_file)
        empirical = get_empirical(empirical_file, lang, mfw)
        pearsonsr = compare_accuracies(lang, predicted, empirical)
        visualize_correlation(lang, predicted, empirical, pearsonsr)

main(langs, mfw)
