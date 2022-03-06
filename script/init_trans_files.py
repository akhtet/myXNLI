
import csv, sys

if __name__ == '__main__':

    basename = sys.argv[2]
    maxlines = int(sys.argv[3])

    with open(sys.argv[1], encoding='utf-8') as infile:
        tsv_reader = csv.reader(infile, delimiter="\t")
        rownum = 0
        fileseq = 1

        for row in tsv_reader:
                  
            if rownum % maxlines == 1:
                if rownum > 1:
                    outfile.close()
                    fileseq += 1                   
                
                outfile = open('%s_%02d.txt' % (sys.argv[2], fileseq), 'wt', encoding='utf-8')
                
            if rownum > 0:
                print (rownum)       
                outfile.writelines('\n'.join([str(rownum), row[4], '<MYANMAR UNICODE TRANSLATION HERE>', '', '']))
            
            rownum += 1

        else:
            outfile.close()
             
