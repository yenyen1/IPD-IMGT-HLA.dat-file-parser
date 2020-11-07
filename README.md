# IPD-IMGT-HLA.dat-file-parser 
A python program that parse HLA.dat file to generate a table (including ID, exon position, ethnic, etc.) for each reference. 

**DAT file from IPD-IMGT/HLA**
https://github.com/ANHIG/IMGTHLA/blob/Latest/Manual.md

**Table column**
1. basic info: ID, length, class, gene, ethnic
2. field name: 4_field, 3_field, 2_field
3. position (suffix "_s" means start, "_e" means end): 
    3.1  UTR1_s, UTR1_e, UTR2_s, UTR2_e
    3.2  exon1_s, exon1_e, ..., exon8_s, exon8_e
    3.3  intron1_s, intron1_e, ..., intron8_s, intron8_e
   Note: 'NA' if not exist.

**Requirement**
python 3

**Example usage**
'python HLA_dat_parser.py hla.dat '



