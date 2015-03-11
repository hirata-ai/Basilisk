#!/usr/bin/python
# -*- coding:utf-8 -*-

def create_factor(category_file,pattern_file):
    from collections import defaultdict
    category = defaultdict(list)
    n = defaultdict(float)
    ins_pattern = {}
    ins_dic = defaultdict(list)
    pattern_dic = defaultdict(list)
    for line in open(category_file):
        line = line.strip()
        if "category" in line:
            category_no = line.split(":")[1]
        elif line != "":
            category[category_no].append(line)
    for line in open(pattern_file):
        line = line.strip()
        (words,freq) = line.rsplit("\t",1)
        (ins,pattern) = words.split("\t",1)
        freq = int(freq)
        n[pattern] += freq
        ins_pattern[words] =freq
        ins_dic[pattern].append(ins)
        pattern_dic[ins].append(pattern)
    return(category,n,ins_pattern,ins_dic,pattern_dic)

def pattern_scoring(pattern_file,category,n,ins_pattern,ins_dic,iteration):
    import math
    from collections import defaultdict
    scoring_pattern = defaultdict(dict)
    scoring_pattern_20 = defaultdict(dict)
    candidate_word = defaultdict(list)
    for i in category:
        f = defaultdict(float)
        for line in open(pattern_file):
            line = line.strip()
            (words,freq) = line.rsplit("\t",1)
            (ins,pattern) = words.split("\t",1)
            category_no = 0
            F_i = 0
            pattern_score = 0
            if ins in category[i]:
                category_no += 1
            if category_no != 0:
                f[pattern] += float(freq)
        for pattern in f:
            pattern_score = (f[pattern]/n[pattern]*math.log(f[pattern],2))
            if pattern_score != 0:
                scoring_pattern[i][pattern] = pattern_score
        for k,v in sorted(scoring_pattern[i].items(),key=lambda x:x[1],reverse=True):
            if len(candidate_word[i])<=(20+iteration):
                scoring_pattern_20[i][k] = v
                candidate_word[i].extend(ins_dic[k])
    #for i in candidate_word:
    #  for j in candidate_word[i]:
    #    print i,j
    return(candidate_word)

def word_scoring(pattern_file,candidate_word,category,pattern_dic,ins_dic):
    import math
    from collections import defaultdict
    wordscore = defaultdict(dict)
    result_word = defaultdict(list)
    for i in candidate_word:
        for word in candidate_word[i]:
            P_i = 0
            F_j = 0
            j = 0
            F_multi = 0
            word_score = 0
            maxavglog = 0
            d = 0
            P_i = len(pattern_dic[word])
            for pattern in pattern_dic[word]:
                for a in ins_dic[pattern]:
                    if a in category[i]:
                        j += 1
                F_j += math.log(j+1,2)
                for b in category:
                    j_multi = 0
                    if b != i:
                        print b
            word_score = F_j/P_i
            if word not in wordscore:
                wordscore[i][word] = word_score
        a = 0
        for k,v in sorted(wordscore[i].items(),key=lambda x:x[1],reverse=True):
            if a<5:
                print i,k,v
                result_word[i].append(k)
            a+=1
    return(result_word)

def bootstrap(category_file,pattern_file):
    (category,n,ins_pattern,ins_dic,pattern_dic) = create_factor(category_file,pattern_file)
    candidate_word = pattern_scoring(pattern_file,category,n,ins_pattern,ins_dic,1)
    word_scoring(pattern_file,candidate_word,category,pattern_dic,ins_dic)

if __name__ =="__main__":
    import sys
    bootstrap(sys.argv[1],sys.argv[2]) #1:インプットファイル 2:パターンファイル
