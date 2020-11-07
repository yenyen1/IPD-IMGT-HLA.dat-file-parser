# usage: python HLA_dat_parser.py hla.dat 
# Author: yenyenwang
# created by 2020-09-09
# updated by 2020-11-07

import sys

def record_ID_length(s:list, record:dict) -> dict:
    if s[0] == 'ID':
        record['ID'] = s[1][:-1]
        record['length'] = s[7]
    return record

def record_class(s:list, record:dict) -> dict:
    if s[0] == 'KW':
        record['class'] = "".join(s[1:]).split(';')[2].split('*')[0]
    return record

def record_4_field(s:list, record:dict) -> dict:
    if s[0] == 'FT' and s[1][:8] == '/allele=':
        all = s[1][9:-2].split('*')
        record['gene'] = all[0]
        if len(all) > 1:
            digit = all[1].split(':')
            record['4_field'] = all[0] + '*' + ":".join( [digit[i] for i in range(4) if i < len(digit)])
            record['3_field'] = all[0] + '*' + ":".join( [digit[i] for i in range(3) if i < len(digit)])
            record['2_field'] = all[0] + '*' + ":".join( [digit[i] for i in range(2) if i < len(digit)])
            record['1_field'] = all[0] + '*' + digit[0]
        else:
            print(s)
            print(all)
    return record

def record_ethnic(s: list, record:dict) -> dict:
    if s[0] == 'FT' and s[1][:8] == '/ethnic=':
        tmp = ""
        if len(s) == 2:
            tmp += s[1][8:-1]
        elif len(s) == 3:
            tmp += s[1][8:]
            tmp += s[-1][:-1]
        else:
            tmp += s[1][8:]
            for i in range(2, len(s) - 1):
                tmp += ' ' + s[i]
            tmp += ' ' + s[-1][:-1]
        record['ethnic'] = tmp
    return record

def record_UTR(s:list, record:dict) -> dict:
    if s[0] == 'FT' and s[1] == 'UTR':
        pos = s[2][:-1].split('..')
        if 'UTR1_s' in record:
            record['UTR2_s'] = pos[0]
            record['UTR2_e'] = pos[1]
        else:
            record['UTR1_s'] = pos[0]
            record['UTR1_e'] = pos[1]
    return record

def record_exon(dat, s:list, record:dict) -> dict:
    if s[0] == 'FT' and s[1] == 'exon':
        pos = s[2][:-1].split('..')
        line = dat.readline()
        s2 = [i for i in line.split(' ') if i != '']
        idx = s2[1][9:-2]
        record['exon' + str(idx) + '_s'] = pos[0]
        record['exon' + str(idx) + '_e'] = pos[1]
    return record

def record_intron(dat, s:list, record:dict) -> dict:
    if s[0] == 'FT' and s[1] == 'intron':
        pos = s[2][:-1].split('..')
        line = dat.readline()
        s2 = [i for i in line.split(' ') if i != '']
        idx = s2[1][9:-2]
        record['intron' + str(idx) + '_s'] = pos[0]
        record['intron' + str(idx) + '_e'] = pos[1]
    return record

def get_record(record:dict, column:str) -> str:
    ss = ""
    cname = column.split("\t")
    for col in cname:
        ss += record.get(col, 'NA') + "\t"
    return ss[:-1] + "\n"

def main():
    out = open(sys.argv[1][:-4] +"_table.txt", 'w')
    dat = open(sys.argv[1])
    
    column = "ID\tlength\tclass\tgene\tethnic\t4_field\t3_field\t2_field\tUTR1_s\tUTR1_e\tUTR2_s\tUTR2_e"
    column += "\t" + "\t".join(["exon" + str(i+1) + "_s\texon" + str(i+1) + "_e" for i in range(8)])
    column += "\t" + "\t".join(["intron" + str(i+1) + "_s\tintron" + str(i+1) + "_e" for i in range(7)])
    out.write(column + '\n')
    
    record = {}
    while True:
        line = dat.readline()
        if len(line) > 0:
            s = [i for i in line.split(" ") if i != '']

            record = record_ID_length(s, record)
            record = record_class(s, record)
            record = record_ethnic(s, record)
            record = record_4_field(s, record)
            record = record_UTR(s, record)
            record = record_exon(dat, s, record)
            record = record_intron(dat, s, record)

            if s[0] == "//\n":
                out.write(get_record(record, column))
                record.clear()
        else:
            break

    dat.close()
    out.close()
    print("fin.")
    
if __name__ == "__main__":
    main()





