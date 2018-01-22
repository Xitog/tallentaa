#import operator
from collections import OrderedDict

GET_FIELDS = False

with open('titres-FR-2017-10-20-01.tsv', mode='r', encoding='utf-8') as datafile:
    lines = datafile.readlines()
    
    #
    # Processing
    #
    
    all_fields = {}
    #title_with_column = 0
    #title_with_question = 0
    look_for = {'!' : 0, ':' : 0, '?' : 0, '«' : 0, '»' : 0, '"' : 0, "'" : 0}
    lengths = []
    types = {}
    three_after = {}
    guillemet_error = 0
    
    for line in lines:
        id, title, typ, year, nb_authors, field, subfields = line.split('\t')
        # length
        title = title.replace(':', ' : ')
        elems = title.split(' ')
        lengths.append(len(elems))
        # elements
        for k in look_for:
            if k in title:
                look_for[k] += 1
        if ('»' in title and '«' not in title) or ('«' in title and '»' not in title):
            # print('guillemets ERROR', title)
            guillemet_error += 1
        if ':' in title:
            if look_for[':'] < 100:
                pass
                # print(title)
            try:
                for i in range(elems.index(':')+1, elems.index(':')+4):
                    if i < len(elems) and len(elems[i]) > 0:
                        # hard lem
                        e = elems[i].lower()
                        if (e[-1] == 's' and e not in ['cas', 'vers', 'dans']) or e[-1] == ',': # attention aux virgules seules
                            e = e[:-1]
                        if len(e) > 0 and e[-1] == 'x': # enjeux, aux
                            e = e[:-1]
                        if e[0:2] in ['l’', "l'", "d'", "d’"] :
                            e = e[2:]
                        if e not in ['de', 'des', 'un', 'une', 'le', 'la', 'les', 'quel', 'quelle', 'et', 'du', 'à', 'en', 'pour', 'vers', 'sur', 'entre', 'au', 'ou', 'quelque', '«', 'aux', 'avec', 'dans']:
                            if e in three_after:
                                three_after[e] += 1
                            else:
                                three_after[e] = 0
                            if e == "nouvelle":
                                pass
                                #print(title)
            except ValueError as ve:
                print(title)
                print('ValueError', ve)
                break
            except IndexError as ie:
                print(title)
                print('IndexError', ie)
                break
        #if '?' in title:
        #    title_with_question += 1
        # fields
        if field not in all_fields:
            all_fields[field] = 1
        else:
            all_fields[field] += 1
        # types
        if typ not in types:
            types[typ] = 1
        else:
            types[typ] += 1

    #
    # Counts
    #
    moyenne = 0
    for i in lengths:
        moyenne += i
    moyenne = moyenne / len(lengths)
    print()
    print("Number of titles:", len(lines)) # 146 603
    #print("Number of titles with ':':", title_with_column, '(', round((title_with_column / len(lines))*100, 2), '%)')
    #print("Number of titles with '?':", title_with_question, '(', round((title_with_question / len(lines))*100, 2), '%)')
    for k in look_for:
        print("Number of titles with", k, look_for[k], '(', round((look_for[k] / len(lines)) * 100, 2), '%)')
    print("Longueur moyenne :", int(moyenne))
    print("Guillemets error :", guillemet_error)   
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

    if GET_FIELDS:
        # Getting fields
        import urllib.request
        s  = urllib.request.urlopen("https://api.archives-ouvertes.fr/ref/domain?q=sdv&wt=json").read()
        print(s)

    #
    # Types
    #
    print('Types ------------------------------------------')
    total = 0
    for typ, nb in types.items():
        print(typ, nb)
        total += nb
    print('total', total)

    for typ, nb in types.items():
        print(typ, round(nb / total * 100, 2))

    # 3 afters
    print('Cooccurrences -----------------------------------')
    f = open('out.csv', 'w')
    for occ in sorted(three_after, key=three_after.get, reverse=True):
        f.write(occ + ' ; ' + str(three_after[occ]) + '\n')
        if three_after[occ] < 20:
            break
    f.close()


    
