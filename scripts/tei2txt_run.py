"""
This file is used to adjust the settings and to run the 
extraction of plain text from XML-TEI files. 
"""

import tei2txt
from os.path import join


#=======================
# File paths (DO ADJUST)
#=======================

languages = ["deu", "fra", "eng", "hun", "nor", "pol", "por", "rom"]


#=======================
# Parameters (DO ADJUST)
#=======================

head = False # Include chapter headings?
foreign = True # Include words marked as foreign?
note = False # Include text from footnotes?
pb = False # Include page breaks?
trailer = False # Include words marked as trailer?
quote = True # Include words marked as quote?
front = False # Include front matter?
back = False # Include back matter (other than notes)?

plaintext = True # Extract and save plain text?
modernize = False # Perform spelling modifications?
counts = False # Establish and save wordcounts?



#=======================
# Run tei2txt
#=======================

for lang in languages: 
    print("\n====== " + lang + " ======") 		
    wdir = join("..")
    teipath = join(wdir, "originals", lang, "*.xml")
    txtpath = join(wdir, "plaintxt", lang, "")
    modsfile = join(wdir, "tei2txt_mods.csv")
    paths = {"teipath":teipath, "txtpath":txtpath, "modsfile":modsfile}
    params = {"note":note, "head":head, "pb":pb, "foreign":foreign, "trailer":trailer, "front":front, "back":back, "quote":quote, "modernize":modernize, "counts":counts, "plaintext":plaintext}
    tei2txt.main(paths, params)
