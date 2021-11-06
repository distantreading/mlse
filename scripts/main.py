from xml_utils import get_all_xmls, get_author_statistics, move_to_dir, get_author
from os.path import join


#language_list = ['deu', 'por', 'pol', 'eng', 'hun', 'fra', 'nor', 'rom']
language_list = ["fra"]
for language in language_list:
    print("\n====== " + language + " ======")
    teipath = join("..", "..", "..", "eltec", "ELTeC-"+language, "")
    print(teipath)
    xmls = get_all_xmls(teipath)
    #xmls = get_all_xmls('/Volumes/SANDISK64GB/ELTeC-{}-*'.format(language))
    author_stats = get_author_statistics(xmls)
    for author in author_stats:
        if len(author_stats[author]) >= 3:
            print(author_stats[author])
            move_to_dir(author, author_stats, target_dir = join("..", "originals", language))
