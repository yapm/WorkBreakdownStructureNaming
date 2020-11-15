# -*-coding: utf8 -*
#Python 3 only

"""
##################         Algorithm       #########################
#      Original         |    Count   |    ID        |     len(ID)  #
#Project                |    0       |     1        |       1      #
#   HW                  |    1       |     1.1      |       3      #
#       Specification   |    2       |     1.1.1    |       5      #
#   SW                  |    1       |     1.2      |       3      #
#       Specification   |    2       |     1.2.1    |       5      #
#       Code            |    2       |     1.2.2    |       5      #
#           Validation  |    3       |     1.2.2.1  |       7      #
#   Qualification       |    1       |     1.3      |       3      #
####################################################################

"""

import os
import re
import sys

def tabCreator(nb_tab, sentence):
    """
    Function that returns a sentence with the number of tab on front
    """
    temp_sentence = sentence
    for tab in range(nb_tab):
        temp_sentence = "\t" + temp_sentence
    return temp_sentence

def calculID(count_tab, ID):
    """
    Function that gives an ID to each title depending on its level of hierarchy
    """    
    #if the level hierarchy is inferior to the previous ID then add ".1"
    if 2*count_tab+1 > len(str(ID)):
        ID = ID + ".1"
        
    #otherwise if level hierarchy is equal to the previous ID then increase last numbe
    elif 2*count_tab +1 == len(str(ID)):
        ID = ID[:-1] + str(int(ID[-1])+1)
    
    #in other cases, increase the level ID 
    else:
        ID = ID[0:count_tab*2] + str(int(ID[count_tab*2])+1)
        
    return ID

class WBS:
    """
    Class defining an object for manipulating a WBS document
    """
    def __init__(self, origin_file='WBS.txt'):
        self.original_content = open(origin_file,'r', encoding="utf8")
        self.final_file = open('GENERATED_WBS.txt','w', encoding="utf8")
        self.l_final = []
        self.count_tab = 0
        self.ID = "0"        

    def parseOrigin(self):
        """
        Function for parsing the original content
        remove \n character
        Allocate tab space to hierarchy number
        """

        for each_line in self.original_content:

            #counts how many tab are included in the sentence
            self.count_tab = each_line.count("\t")
            
            #calculate the level of hierarchy of the title
            self.ID = calculID(self.count_tab, self.ID)
            
            #removes the \n character from the line
            temp_buffer = each_line.replace('\n','')   
            
            #split each line from original list into two different lists
            temp_buffer = re.compile("\t+").split(temp_buffer)
            
            #then concatenate ID and the content of the line
            temp_buffer[-1] = self.ID + " " + temp_buffer[-1]
            
            #creates a tabulation before ID
            final_sentence = tabCreator(self.count_tab, temp_buffer[-1])

            #include it into final list
            self.l_final.append(final_sentence)

    def writeFinalFile(self):
        """
        Function to write l_final into final file
        """
        for each_line in self.l_final:
            print(each_line,file=self.final_file)

    def closeFiles(self):
        """
        Function to close all files
        """
        self.original_content.close()
        self.final_file.close()

if __name__ == '__main__':
    """Main function to call python patch_anki.py"""
    os.chdir('.')
    try:
        #sys.argv[1] allows to inclue a file as argument
        wbs = WBS(sys.argv[1])
    except IndexError :
        wbs = WBS()
    except FileNotFoundError:
        print("file not found")
        sys.exit(1)

    wbs.parseOrigin()
    wbs.writeFinalFile()
    wbs.closeFiles()
