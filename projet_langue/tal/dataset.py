#import operator
from collections import OrderedDict

with open('titres-FR-2017-10-20-01.tsv', mode='r', encoding='utf-8') as datafile:
    lines = datafile.readlines()
    
    #
    # Processing
    #
    
    all_fields = {}
    title_with_column = 0
    
    for line in lines:
        id, title, typ, year, nb_authors, field, subfields = line.split('\t')
        if ':' in title:
            title_with_column += 1
        if field not in all_fields:
            all_fields[field] = 1
        else:
            all_fields[field] += 1

    #
    # Counts
    #
    
    print()
    print("Number of titles:", len(lines)) # 146 603
    print("Number of titles with ':':", title_with_column, '(', round((title_with_column / len(lines))*100, 2), '%)')
    print()
    
    #
    # Fields
    #                

    count = 0
    # Sort by name
    #for field in sorted(all_fields.keys()):
    # Sort by numbers of occurences
    sorted_fields = OrderedDict(sorted(all_fields.items(), key=lambda t: t[1], reverse=True))
    #sorted_fields = sorted(all_fields.items(), key=operator.itemgetter(0))
    for name, occ in sorted_fields.items():
        count += 1
        print("%2d.   %10s   %6d   %6.3f" % (count, name, occ, round((occ / len(lines))*100, 2)) + "%")

    # Getting fields
    import urllib.request
    s  = urllib.request.urlopen("https://api.archives-ouvertes.fr/ref/domain?q=sdv&wt=json").read()
    print(s)
    