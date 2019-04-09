#This program will take a list of class number interest and the class line as input. For consecutive five items, if hits are less than 2, include all the five lines, then continue
#The target is to find eactly how many misses are there in each virion
#Future functions includes automatic fitting of the correct orientation
#t_h is threshold for how many matches are in 5-group, should larger than 3 at least
#By default, to determine a rotational match, we need at least 4 matches in one set

from sys import argv
import re
import random

def is_content(nr_of_item,input_star_line):
    star_tmp_line=re.split(' +', input_star_line.strip())
    if len(star_tmp_line)==nr_of_item:
        return True
    return False

def is_head(input_star_line):
    star_tmp_line=re.split(' +', input_star_line.strip())
    if cmp(star_tmp_line[0][:4], "_rln")==0:
        return True
    return False

def is_empty(input_star_line):
    if len(input_star_line.strip())==0:
        return True
    return False

def is_content(input_star_line, nr):
    star_tmp_line=re.split(' +', input_star_line.strip())
    if len(star_tmp_line)==nr:
        return True
    return False

def is_match(input_star_item,lst_line):
    lst_len=len(lst_line)
    i=0
    while 1:
        if i>=lst_len:
            break
        if int(lst_line[i])==int(input_star_item)-1:
            return True
        i=i+1
    return False

def main():
    if len(argv)!=6:
        print "Usage: python Orientation_selection.py input.star selection_value_lst key_column(starts from 1) threshold class_count"
        exit()
    my_star=open(argv[1],"r")
    my_lst=open(argv[2],"r")
    key_c=int(argv[3])
    t_h=int(argv[4])
    class_count=int(argv[5])
    star_line=my_star.readlines()
    lst_line=my_lst.readlines()
    lst_count=len(lst_line)
    check_lst=[-1 for k in range(class_count)]
    for t in range(0,lst_count):
        tmp_line=re.split(' +', lst_line[t].strip())
        l_c=len(tmp_line)
        if l_c==0:
            continue
        for k in range(0,l_c):
            check_lst[int(tmp_line[k])-1]=t
    #Write the lst file in a format of clockwise rotation
    outline=""
    i=0
    j=0
    star_count=len(star_line)
    while 1:
        if i>=star_count:
            break
        if is_empty(star_line[i]) and i<4:
            outline+="\n"
            i=i+1
            continue
        if is_head(star_line[i]):
            j=j+1
            outline+=star_line[i].strip()+"\n"
            i=i+1
            continue
        tmp_line=re.split(' +', star_line[i].strip())
        if len(tmp_line)<3 and i<4:
            outline+=star_line[i].strip()+"\n"
            i=i+1
            continue
        i=i+1
    head_count=j
    i=0
    p_b=0
    p_e=0
    c_e=5
    tmp_c=0 #Updated based on states, the last content will be treated differently
#process every 60 entries, use pointer
    flag=0
    total=0
    #print check_lst
    while 1:
        if i>=star_count:
        #if i>=800:
            break
        if is_empty(star_line[i]):
            i=i+1
            continue
        if is_head(star_line[i]):
            i=i+1
            continue
        if is_content(star_line[i],j):
            if tmp_c%60==0: #Initialize virion
                virion_bad=0
                virion_good=0
                tmp_out="" # Print a specific line for local refinement
                tmp_c=0
            if tmp_c%5==0: #Initilize rotational
                p_b=i
                match_count=0
                rot_lst=[-1 for k in range(c_e)]
            tmp_line=re.split(' +', star_line[i].strip())
            if len(tmp_line)!=head_count:
                print "Error! head_count mismatch"
                exit()
            if check_lst[int(tmp_line[key_c-1])-1]>=0:
                match_count+=1
                rot_lst[i-p_b]=check_lst[int(tmp_line[key_c-1])-1]
            if tmp_c%5==4: #summarize roational situation
                #print rot_lst
                if match_count<=t_h: #This is a bad group (Not enough determined data)
                    virion_bad+=1
                    #add center to output file (yet)
                    #Start ritational alignment
                else:
                    best_dup=-1
                    best_dup_v=0
                    best_i=0
                    for t in range(0,c_e):
                        tmp_match=0
                        for k in range(0,c_e):
                            if rot_lst[k]==k:
                                tmp_match+=1
                            #Find the record high and rotational shift
                        if tmp_match>=best_dup_v:
                            best_dup_v=tmp_match
                            best_dup=t
                        # Generate rotational list
                        tmp=rot_lst[0]
                        for k in range(0,c_e-1):
                            rot_lst[k]=rot_lst[k+1]
                        rot_lst[c_e-1]=tmp
                    #Begin to analyze                         
                    if best_dup_v<5:
                        #Failed the rotational match
                        virion_bad+=1
                    else:
                        #Find the determined polymerase position
                        tmp_out+=star_line[p_b+best_dup].strip()
                        tmp_out+="\n"
                        virion_good+=1
            if tmp_c%60==59: # Summarize the virion, all has been printed
                #print "\n"
                #print virion_bad
                total+=1
                #if virion_good==12: #all have too be good
                if virion_good>=1: #Just print
                    flag+=1
                    outline+=tmp_out
                #Can have other criteria for printing
            tmp_c+=1
        i=i+1
    #print total,flag,float(float(flag)/float(total))
    print outline[:-1]
main()
