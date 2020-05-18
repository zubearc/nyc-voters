import json
import numpy
import re
import sys
import os

data_path = '../aquire/json/'
files_path = '../aquire/fileurls.json'

fileName = '03BRONX_AD077_DEMOCRATICEnrollment.pdf.json'
fileName = '03BRONX_AD078_DEMOCRATICEnrollment.pdf.json'

if sys.argv[1]:
    fileName = sys.argv[1]

def is_file(fname):
    return os.path.isfile(fname)

if is_file(fileName + '.html'):
    exit('already done: ' + fileName + '.html')

if 'DEMOCRATIC' in fileName:
    delem = 'DEM'

# delems = [' DEM ', '  DE ', '#DEM ', '*DEM ', ' #DE ']

partyStr = [' DEM', '*DEM', '#DEM', '  DE', ' *DE', ' #DE']
DE = 'DE'
M = 'M'

with open(data_path + fileName) as f:
    j = json.loads(f.read())

NAME_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ.`();' # how tf can one have a grave char in their name?!
NUM_CHARS = '0123456789'

def reverse_until_hit_digit(line, from_offset):

    i = from_offset
    hit_char = False
    hit_digit_at = 0
    while i > 0:
        c = line[i]
        if c.isdigit():
            if not hit_char:
                hit_digit_at = i
                break
            else:
                break
        if c.isalpa():
            hit_char = True
        i -= 1

    return hit_digit_at
    # for k,c in enumerate(line):

def reverse_until_hit_name(line, from_offset):
    i = from_offset
    # hit_char = False
    hit_at = 0
    max_chances = 32
    read = ""
    while i > 0:
        c = line[i]
        if read[-2:] == ', ':
            hit_at = i
            break
        read += c
        max_chances -= 1
        if max_chances <= 0:
            break
        i -= 1

    return hit_at


def reverse_until_hit_party(line, from_offset, max_runs=20):

    i = from_offset
    hit_char = False
    hit_digit_at = 0
    read = ''
    # dem ->med
    
    while i > 0:
        max_runs-=1
        if max_runs <= 0:
            break
        c = line[i]
        for ps in partyStr:
            if read[-5:] == (ps[::-1] + ' '):
                return True
        read += c
        i -= 1

    return False

def wordprocess(line):
    first_read_at_offset = 0
    read = ""

    splitable_indexes = []

    splited = []

    for k,c in enumerate(line):
        if first_read_at_offset == 0 and c != ' ':
            first_read_at_offset = k

        if len(read) > 10:
            if read[-2:] == DE:
                if (read[-3] == '#' or read[-3] == '*' or read[-3] == ' ') and read[-4] == ' ':
                    # try:
                    if True:
                        # swd = reverse_until_hit_digit(line, k)
                        hitname = reverse_until_hit_name(line, k - 4)
                        didnthitparty = reverse_until_hit_party(line, k - 4)
                        print 'hitname, didntHitParty', hitname, didnthitparty, k - 4
                        # print 'X', read[-18:-4]
                        # w = read[-18:-4].split(' ')[::-1]
                        # found_alnum = False
                        # rs_starts_with_digit = (read[-18:-4].replace(' ', '') == '')
                        # for i in range(0, len(w)):
                        #     W = w[i]
                        #     if W.isdigit():
                        #         if not found_alnum:
                        #             rs_starts_with_digit = True
                        #         else:
                        #             break
                        #     if W.isalnum():
                        #         found_alnum = True
                        #         # break
                        # if ' DE' in read[-18:-4] or swd:#not read[-18:-4].replace(' ', '').isalnum():
                        if didnthitparty or not hitname:
                            print 'reject', json.dumps(read[:k-4])
                            read += c
                        # if line[k + 1].isalpha() or line[k + 1] == '-':
                            continue
                    # except Exception:
                    #     pass

                    if c == ' ':
                        splitable_indexes.append(k)
                        print '1Split', k
                    elif c == M:
                        splitable_indexes.append(k + 1)
                        print '2Split', k + 1
            try:
                x = int(read[-5:])
                if x > 10000 and x < 11111:
                    ruo = reverse_until_hit_name(line, k - 4)
                    if ruo and abs(ruo - k) < 30:
                        print 'XSplit', abs(ruo - k), ruo, k
                    else:
                        print 'Split', k
                        splitable_indexes.append(k + 5)
            except Exception:
                pass
            if read[-23:] == '-  - - -     -   - - - ':
                splitable_indexes.append(k)
        read += c
    
    print 'Splittable indexes', splitable_indexes

    if len(splitable_indexes) == 3:
        splited.append(line[0:splitable_indexes[0]])
        splited.append(line[splitable_indexes[0]:splitable_indexes[1]])
        splited.append(line[splitable_indexes[1]:splitable_indexes[2]])
        ls = line[splitable_indexes[2]:].strip()
        if len(ls) > 1:
            splited.append(ls)
    elif len(splitable_indexes) == 2:
        splited.append(line[0:splitable_indexes[0]])
        splited.append(line[splitable_indexes[0]:splitable_indexes[1]])

        ls = line[splitable_indexes[1]:].strip()
        if len(ls) > 1:
            splited.append(ls)
    elif len(splitable_indexes) == 1:
        splited.append(line[0:splitable_indexes[0]])
        ls = line[splitable_indexes[0]:].strip()
        if len(ls) > 1:
            splited.append(ls)
    else:
        print 'anomoly, cannot split'
        if len(splitable_indexes) != 0:
            print 'anomoly1'

    splited2 = []
    for splite in splited:
        split_at_offset = 0

        reverse_from = 0
        for k,c in enumerate(splite):
            if c == ',':
                reverse_from = k
        I = reverse_from
        got_char = False
        got_dashes = 0
        read_number = ''
        read_consec_spaces = 0
        while I >= 0:
            I -= 1
            c = splite[I]
            if c == ' ':
                read_consec_spaces += 1
                if read_consec_spaces == 6:
                    split_at_offset = I + 1
                    break
                continue
            else:
                read_consec_spaces = 0
            # if c in NAME_CHARS:
            if c.isalpha():
                got_char = True
            # if c not in NAME_CHARS and c not in NUM_CHARS:
            ok = False
            if c.isalpha():
                if c.isupper():
                    ok = True
                else:
                    ok = False
            else:
                ok = c.isalpha()
            if not ok and c not in NUM_CHARS and c not in NAME_CHARS:
                if len(read_number):
                    if c == '-' and got_dashes < 3:
                        read_number += '.'
                        got_dashes += 1
                        continue
                    else:
                        split_at_offset = I + 1
                        break
                if c == '-':
                    got_dashes += 1
                    if got_dashes > 2:
                        split_at_offset = I + 1
                        break
                    if not got_char:
                        split_at_offset = I + 1
                        break
                    else:
                        pass
                else:
                    split_at_offset = I + 1
                    break
            else:
                if c in NUM_CHARS:
                    read_number += c
                try:
                    n = int(read_number)
                    if n > 10000:
                        split_at_offset = I + 1 + len(read_number)
                        break
                except Exception:
                    pass
                pass


        # s = splite.split()

        # for k,w in enumerate(s):
        #     if w[0] == ',':
        #         split_at_offset = k - 1
        #         try:
        #             x = split_at_offset[k - 2]
        #             if x.isupper():
        #                 split_at_offset = k - 2
        #             else:
        #                 print 'not upper'
        #                 n = int(x)
        #                 split_at_offset = k - 2
        #                 print 'made exception'
        #         except Exception:
        #             pass
        if split_at_offset:
            sp1 = splite[0:split_at_offset]
            sp2 = splite[split_at_offset:]
            S1 = sp1#' '.join(sp1)
            S2 = sp2#' '.join(sp2)
            if S1.strip().replace('-', '') == '':
                S1 = ''
            elif len(S1) < 20 or len(S2) < 20 and not len(splited) < 3:
                S2 = S1 + S2
            else:
                splited2.append(S1)
            splited2.append(S2)
        else:
            splited2.append(splite)
    print splited2
    
    print splited

    return splited2
pds = []

## -----====[ REPLACEMENTS ]====-----
# These are data errors and/or case scenarios that occur infrequently enough
# that we can manually re-write the data instead of introducing new rules
# into the already spaghetti parser code

REPLACEMENTS = {
    'ELLIS 111': 'ELLIS III',
    # 'FERREIRAS---COLON': 'FERREIRAS-COLON'
    'RUIZ    SANTANA': 'RUIZ SANTANA',
    'DE LOS SANTOS    REYE': 'DE LOS SANTOS REYE',
    'MATOS    LAMBETH': 'MATOS LAMBETH',
    'THOMAS F,': 'THOMAS F', # AD65 DEM
    'CAMPBE;;': 'CAMPBE',
    '18B,C': '18B-C',
    # ',LOIS MA      DE': ',LOIS MA      DE-', # AD67 DEM
    'MOGHADASSEI_': 'MOGHADASSEI ', # AD73 DEM
    # 'FORMESS ,JESSE            DE': 'FORMESS ,JESSE            DE-', # AD75 DEM
    # 'REOGH ,BRENDAN J        DE': 'REOGH ,BRENDAN J        DE-', # AD81 DEM
    'ELDWIN, G': 'ELDWIN G', # AD82 Dem
    # 'FAMILIA ,CLARIBEL       DE': 'FAMILIA ,CLARIBEL       DE-', # AD84 DEM
    'VAUGHAN MR/,': 'VAUGHAN MR,',
    'NOONAN-MAZZEI ,M,A': 'NOONAN-MAZZEI ,M A', # AD44 ( this is a dupe entry! )
    'ECHEVARRIA / COLON': 'ECHEVARRIA COLON', # AD45
    'ROSENBLATT-----K': 'ROSENBLATT-K', # AD73
    # 'ALKUSARI ,HUSAM B      DE': 'ALKUSARI ,HUSAM B      DE-', # AD81 DEM
    '304693302': 'Lastname', # unknown person AD42 DEM
    'RASMUSSEN-EVANS ,N, J': 'RASMUSSEN-EVANS ,N J', # AD50 ( this is a dupe entry! )
    'LEDERMAN +-` ,': 'LEDERMAN ,', # ?!?! AD53
    'WILTSHIRE ,AH-SANDY B,': 'WILTSHIRE ,AH-SANDY B', # AD55
    'COLOMBATTO ,ZEPH A,': 'COLOMBATTO ,ZEPH A', # AD57
    'THOMPSON-JONES ,K, Q': 'THOMPSON-JONES ,K Q', # AD59 DEM
    'DANIEL-HAMILTON ,D,M': 'DANIEL-HAMILTON ,D M', #AD60
    
    '---': '-', # triple sequential dashes never used in titles, but one name does (wtf?)
    '- ,': ' ,', # uneeded/unused dash in name
}

if 'AD067_DEM' in fileName:
    REPLACEMENTS[',LOIS MA      DE'] = ',LOIS MA      DE-'

if 'AD075_DEM' in fileName:
    REPLACEMENTS['FORMESS ,JESSE            DE'] = 'FORMESS ,JESSE            DE-'

if 'AD081_DEM' in fileName:
    REPLACEMENTS['REOGH ,BRENDAN J        DE'] = 'REOGH ,BRENDAN J        DE-'
    REPLACEMENTS['ALKUSARI ,HUSAM B      DE'] = 'ALKUSARI ,HUSAM B      DE-'

if 'AD084_DEM' in fileName:
    REPLACEMENTS['FAMILIA ,CLARIBEL       DE'] = 'FAMILIA ,CLARIBEL       DE-'

if 'AD058_DEM' in fileName:
    REPLACEMENTS['DEM 10405'] = 'DEM X405'

if 'AD061_DEM' in fileName:
    REPLACEMENTS['HERNANDEZ ,RIOS D,'] = 'HERNANDEZ ,RIOS D'

## END REPLACEMENTS

for page in j:
    lines = page.split('\n')
    avg1s = []
    avg2s = []
    avg3s = []
    for line in lines:
        nline = line +' '
        for repl in REPLACEMENTS:
            nline = nline.replace(repl, REPLACEMENTS[repl])
        for namechar in NAME_CHARS:
            nline = nline.replace(namechar + ',', namechar + ' ,')
        mc = re.search("([0-9]+),", nline)
        if mc:
            mci = mc.group(0)
            mcii = mc.group(1)
            nline = nline.replace(mci, 'ZXZ ,')
            # nline = 
        # for delem in delems:
        #     nline = nline.replace(delem, '$')
        # n = nline.count('$')
        # if n > 0 and n != 3:
        #     print '!!! Error: '
        # elif n == 3:
        #     indices = [i for i, x in enumerate(list(nline)) if x == "$"]
        #     avg1s.append(indices[0])
        #     avg2s.append(indices[1])
        #     avg3s.append(indices[2])

        pd = wordprocess(nline)

        if len(pd) > 0 and len(pd) != 3:
            if len(pd) == 2:
                if len(nline) < 100:
                    pd.append('null')
                    print '2, <90', len(nline)
                else:
                    print '2, >90', len(nline)
                    spaces = 0
                    for c in nline:
                        if c == ' ':
                            spaces += 1
                        else:
                            break
                    if spaces < 20:
                    # cs1 = pd[0].count(' ')
                    # cs2 = pd[1].count(' ')
                    # if cs2 > cs1:
                        pd.insert(1, 'null')
                    else:
                        pd.insert(0, 'null')
            if len(pd) == 1:
                if len(nline) < 60:
                    print '1, <60', len(nline)
                    pd.append('null')
                    pd.append('null')
                elif len(nline) > 100:
                    print '1, >100'
                    pd.insert(0, 'null')
                    pd.insert(0, 'null')
                else:
                    print '2, >60', len(nline)
                    pd.insert(0, 'null')
                    pd.append('null')

        # pds.insert(0)
        pds.append(pd)

        # nline.in
        print nline.encode('ascii', 'ignore').decode('ascii')
        # s = line.split(' DE')
        # first = line[0:45]
        # print s[0]
    # print avg1s, avg2s, avg3s
    # if len(avg1s) != 0:
    #     print numpy.mean(avg1s), numpy.mean(avg2s), numpy.mean(avg3s)

html = """
<!doctype html>
<html>
<body>
<table border=1>"""

for pd in pds:
    rows = "<tr>"
    if len(pd) > 3 and 'AD058' not in fileName: #ad58 has odd street numbering, needs manual fixes
        print pd
        raise pd
    for p in pd:
        x= p.encode('ascii', 'ignore').decode('ascii').strip()
        rows += "<td>" + x + "</td>"
    rows += "</tr>"
    html += rows

html += """
</table>
</body>
</html>"""

with open(fileName + '.html', 'w') as f:
    f.write(html)