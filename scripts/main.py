from xml_utils import get_all_xmls, get_author_statistics, move_to_dir, get_author


language_list = ['deu', 'por', 'pol', 'eng', 'hun', 'fra', 'nor', 'rom']
for language in language_list:
    xmls = get_all_xmls('/Volumes/SANDISK64GB/ELTeC-{}-*'.format(language))
    author_stats = get_author_statistics(xmls)
    for author in author_stats:
        if len(author_stats[author]) >= 3:
            move_to_dir(author, 
                        author_stats,
                        target_dir = '/Users/marte.wulff/Documents/Digital_Humanities/COST/mlse/originals/{}'.format(language))
                