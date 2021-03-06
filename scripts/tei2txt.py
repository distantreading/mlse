"""
Script to extract plain text from XML-TEI. 
Run this using tei2txt_run.py 
"""

#==============
# Imports 
#==============

import os.path
import glob
from os.path import join
from lxml import etree
import pandas as pd
import re
import csv


#==============
# Functions 
#==============



# === Getting ready

def helper(paths, params): 
    if not os.path.exists(paths["txtpath"]):
        os.makedirs(paths["txtpath"])


def get_filename(teifile): 
    filename, ext = os.path.basename(teifile).split(".")
    #print(filename)
    return filename



# === Extracting the plain text

def read_tei(teifile): 
    with open(teifile, "r", encoding="utf8") as outfile: 
        tei = etree.parse(teifile)
        return tei


def remove_tags(tei, params): 
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    etree.strip_tags(tei, "{http://www.tei-c.org/ns/1.0}hi")
    # other candidates: foreign, quote
    return tei


def remove_elements(tei, params): 
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    for param in params.items(): 
        if params[param[0]] == False: 
            etree.strip_elements(tei, "{http://www.tei-c.org/ns/1.0}"+param[0], with_tail=False)
    return tei
    

def get_text(tei, params): 
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    xpath = "//tei:text//text()"
    text = tei.xpath(xpath, namespaces=namespaces)
    text = " ".join(text)
    return text


def clean_text(text): 
    text = re.sub("[ ]{2,20}", " ", text)
    text = re.sub("\n{2,20}", "\n", text)
    text = re.sub("[ \n]{2,20}", " \n", text)
    text = re.sub("\t{1,20}", "\t", text)
    return text
    

def extract_text(tei, params):
    tei = remove_tags(tei, params)
    tei = remove_elements(tei, params)
    text = get_text(tei, params)
    text = clean_text(text)
    return text



# === Modernize the text

def get_mods(paths):
    with open(paths["modsfile"], "r", encoding="utf8", newline="\n") as infile: 
        mods = csv.reader(infile, delimiter="=")
        mods = {rows[0]:rows[1] for rows in mods}
        return mods


def modernize(text, mods): 
    for old,new in mods.items(): 
        old = "(\W)"+old+"(\W)"
        new = "\\1"+new+"\\2"
        text = re.sub(old, new, text)
    return text
    r'\bis\b'


def modernize_text(text, paths):
    mods = get_mods(paths)
    text = modernize(text, mods)
    return text



# === Get word count

def get_counts(text): 
    # tokens
    words = re.split("\W+", text)
    num_words = len(words)
    if num_words > 99999: 
        len_category = "long"
    elif num_words > 49999: 
        len_category = "medium"
    elif num_words > 9999: 
        len_category = "short"
    else: 
        len_category = "too short!"
    return num_words, len_category



# === Save results to disk

def save_text(text, paths, filename): 
    filename = join(paths["txtpath"], filename+".txt")
    with open(filename, "w", encoding="utf8") as outfile: 
        outfile.write(text)


def save_counts(len_words, len_category): 
    len_category = pd.DataFrame.from_dict(len_category, orient="index", columns=["category"])
    print(len_category.head())
    len_words = pd.DataFrame.from_dict(len_words, orient="index", columns=["words"])
    print(len_words.head())
    counts = len_category.merge(len_words, left_index=True, right_index=True).sort_index()
    print(counts.head())    
    with open("counts.csv", "w", encoding="utf8") as csvfile: 
        counts.to_csv(csvfile, sep=";")

        

#==============
# Main 
#==============

def main(paths, params): 
    helper(paths, params)
    len_category = {}
    len_words = {}
    for teifile in glob.glob(paths["teipath"]):
        filename = get_filename(teifile)
        tei = read_tei(teifile)
        text = extract_text(tei, params)
        if params["modernize"] == True: 
            text = modernize_text(text, paths)
        else: 
            pass
        if params["counts"] == True: 
            len_words[filename], len_category[filename] = get_counts(text)
        if params["plaintext"] == True: 
            save_text(text, paths, filename)
    if params["counts"] == True: 
        save_counts(len_words, len_category)
    
    

