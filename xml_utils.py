import numpy as np
from glob import glob
import xml.etree.ElementTree as ET



def get_all_xmls(input_path):
    """get all xmls for one ELTeC dir 
    
    Arguments
    _________
    
    input path: /path/to/language/dir/ELTEC-language-023984/ type (str)
    
    """
    # rstrip('/') removes a '/' at the end if it exists
    return sorted(glob(input_path.rstrip('/')+'/level1/*.xml'))

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
    return author.text.strip()


def get_author_statistics(input_xmls,):
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
        author = get_author(xml)
        try:
            author_stats[author].append(xml)
        except KeyError:
            author_stats[author] = [xml]
    return author_stats


def move_to_dir(input_author, author_stats, target_dir):
    """
    move all xmls of one given author into a given src directory
    
    Arguments
    _________
    input_author: 'Castro Osório, Ana de (1839-1871)' (type str),
    author_stats: author statistics (type dict)
    target_dir: '/path/to/the/target/destination' (type str)
    
    """
    xmls = author_stats[input_author]
    for xml in xmls:
        shutil.move(xml, target_dir)
    
    
