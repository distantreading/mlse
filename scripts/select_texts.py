import numpy as np
from glob import glob
import xml.etree.ElementTree as ET
import shutil
from os.path import join
import os
import re



def get_all_xmls(input_path):
    """get all xmls for one ELTeC dir 
    
    Arguments
    _________
    
    input path: /path/to/language/dir/ELTEC-language-023984/ type (str)
    
    """
    xmls = os.listdir(input_path)
    xmls = [xml for xml in xmls if "xml" in xml]
    return xmls


def get_author(input_xml):
    """get the text from the author tag of one xml
    
    Arguments
    __________
    input_xml: /path/to/input/xml/file.xml (type str)
    """
    # first parse the input_xml
    xml = ET.parse(input_xml)
    root = xml.getroot()
    author = root.find('.//{http://www.tei-c.org/ns/1.0}author')
    # strip removes preceding and trailing whitespace
    author = author.text.strip()
    author = re.sub("\n", "", author)
    author = re.sub("[ ]{1,50}", " ", author)
    return author


def get_author_statistics(teipath, input_xmls):
    """
    write a dict of the following form:
    author_stats = {'Author_1': ['book0.xml', 'book1.xml', 'book2.xml'...], 
                    'Author_2': ['book0.xml', 'book1.xml', 'book2.xml'...],
                    ..., 
                    }
                    
    Arguments
    _________
    
    input_xmls = all the xmls to check for the author tag (type list)
                ['/path/to/first/xml/book0.xml', 
                 '/path/to/second/xml/book1.xml', 
                 ....]
                    
    """
    author_stats = {}
    for xml in input_xmls:
        author = get_author(join(teipath, xml))
        try:
            author_stats[author].append(xml)
        except KeyError:
            author_stats[author] = [xml]
    return author_stats


def move_to_dir(teipath, input_author, author_stats, target_dir):
    """
    move all xmls of one given author into a given src directory
    
    Arguments
    _________
    input_author: 'Castro Osório, Ana de (1839-1871)' (type str),
    author_stats: author statistics (type dict)
    target_dir: '/path/to/the/target/destination' (type str)
    
    """
    xmls = author_stats[input_author]
    if not os.path.exists(target_dir): 
        os.makedirs(target_dir)
    for xml in xmls:
        shutil.copy(join(teipath, xml), target_dir)
    
    


def main(language_list):
    for language in language_list:
        print("\n====== " + language + " ======")
        teipath = join("..", "..", "..", "eltec", "ELTeC-"+language, "level1", "")
        print(teipath)
        xmls = get_all_xmls(teipath)
        print(len(xmls), "files found")
        #print(xmls)
        author_stats = get_author_statistics(teipath, xmls)
        print(len(author_stats), "different authors found")
        threetitleauthors = []
        for author in author_stats:
            #print(author, len(author_stats[author]))
            if len(author_stats[author]) >= 3:
                threetitleauthors.append(author)
                #print("-", author)
                move_to_dir(teipath, author, author_stats, target_dir = join("..", "originals", language, ""))
        print(len(threetitleauthors), "different authors with three or more novels found")

main(["deu", "fra", "eng", "hun", "por", "pol", "nor", "rom"])

