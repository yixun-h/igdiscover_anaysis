#!/Users/apple/anaconda3/bin/python3
#!/usr/bin/env python3
'''
Title: barcode_remove
Author:Yixun Huang
Description:
    This program will remove the barcodes & nucletide acid before barcode and
    print filtered sequence into a new fastq file. And calculate the number of sequences
    which are not printed in the output file because they do not have the barcode.
Usage:
    ./barcode_remove.py sample2.fastq filtered_sample.fastq
'''
import sys
record={}
idlist=[]
seq=[]
barcode=['TACGGG']
with open(sys.argv[1],'r') as fin:
    memory= []
    counter=1
    for line in fin:
        line=line.rstrip()
        if counter%4 == 1:
            if counter== 1:
                idlist.append(line)
            else:
                seq.append(memory)
                idlist.append(line)
                memory=[]
        else:
            memory.append(line)
        counter+=1
    seq.append(memory)
    record=dict(zip(idlist,seq))
with open(sys.argv[2],'w') as out:
    remove_seq = 0
    for id in idlist:
        seqline = record[id][0].upper() # So the barcode also matches lowercase sequence
        qualid = record[id][1]
        qualline = record[id][2]
        pos = seqline.find(barcode[0], 0, 40)

        if pos != -1:
            No_G=len(seqline[pos+6:])-len(seqline[pos+6:].lstrip('G'))
            print('{}\n{}\n{}\n{}'.format(id, seqline[pos+6:].lstrip('G'), qualid, qualline[pos+6+No_G:]), file=out, sep='')
        else:
            remove_seq+=1
    print(len(record))
    print('the number of sequences removed:{}'.format(remove_seq))




'''
        #tag = False
        #for i in range(0,40):
            if seqline[i:i+6] == barcode[0]:
                if tag == False:
                    print('{}\n{}\n{}\n{}'.format(id, seqline[i+6:], qualid, qualline[i+6:]), file=out, sep='')
                    tag = True
                    remain_seq_length+=1
    #print(len(record)-remain_seq_length)
'''
