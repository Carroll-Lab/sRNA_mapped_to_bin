#!/usr/bin/python
'''
Created on 16 Mar 2016

@author: steve
'''

import csv
import argparse

def bin_output(file_name,outfile,bin_size):
    """
    Makes the start and end values 0 for better looking circos plotting.
    
    TODO:fix for accuracy - currently cuts of the sRNA in position 0 kind of
    
    Input --> sRNA, count, pos
    Output --> bin_no, start_pos, end_pos, bin_count
    
    """

    sRNA_sorted = load_mapped_sRNAs(file_name)

    sRNAs_in_bin = 0.0
    out_list=[(0,0,0,0)]
    sRNAcount=0.0
    sRNA_bin=1
    for seq in range(len(sRNA_sorted)):
        if sRNA_sorted[seq][2] < (sRNA_bin*bin_size):
            sRNAs_in_bin += abs(sRNA_sorted[seq][1])
        else:
            out = (sRNA_bin,(sRNA_bin-1)*bin_size,(sRNA_bin*bin_size)-1,
                   sRNAs_in_bin)
            out_list.append(out)
            sRNAcount +=sRNAs_in_bin
            sRNAs_in_bin = abs(sRNA_sorted[seq][1])
            sRNA_bin +=1
    out = (sRNA_bin,(sRNA_bin-1)*bin_size, sRNA_sorted[-1][2],
           sRNAs_in_bin)
    out_list.append(out)
    sRNAcount +=sRNAs_in_bin
    #add 0 count in final position
    out_list.append((sRNA_bin+1, (((sRNA_bin-1)*bin_size)+bin_size), 
                     (((sRNA_bin-1)*bin_size)+bin_size), 0))
    print 'bins = {0}'.format(sRNA_bin)
    print 'total sRNA count = {0}\n'.format(sRNAcount)
    
    write_to_file(outfile, out_list)
    


def load_mapped_sRNAs(file_name):
    """
    Load and sort mapped sRNAs from scram output file
    Input --> sRNA,pos,count
    Return ordered_by_pos [(sRNA, count, pos),] 
    """ 
    sRNA_list=[]
    sRNAmapped = open(file_name, 'rU')
    first_line=True
    for line in sRNAmapped:
        if first_line: 
            first_line=False
            pass
        else:
            line = line.strip().split(',')
            c=(line[0],float(line[2]), int(line[1]))
            sRNA_list.append(c) 
    return sorted(sRNA_list, key=lambda sRNA:sRNA[2])
    

def write_to_file(outfile, out_list):
    """
    Write bin counts to csv in correct format for circos plotting
    ['Bin','Start position','End position','sRNA count']
    """
    mycsv = csv.writer(open(outfile, 'wb'))    
    headers = ('Bin','Start position','End position','sRNA count')
    mycsv.writerow(headers)
    for i in out_list:
        row = [i[0],i[1],i[2],i[3]]
        mycsv.writerow(row)

def main():
        """
        Allow script to be run from the command line or the GUI switched on
    
        Assumptions: all flags must be filled correctly or error
    
        comline() --> list(str, str, str, int, str, int, dtr ,int, int, str)
        """
    
                
        parser = argparse.ArgumentParser("bin_output.py")
        parser.add_argument("-i", "--input_file", type=str, 
            help = "Input File Name")
        parser.add_argument("-o", "--output_file", type=str, 
            help = "Output File Name")
        parser.add_argument("-b", "--bin", type=int, 
            help = "Bin Size")
        args=parser.parse_args()
        #return [str(args.input_file),str(args.output_file),int(args.bin)]
        bin_output(args.input_file,args.output_file,args.bin)

if __name__ == "__main__":
    main()