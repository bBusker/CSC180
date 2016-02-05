'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.
'''

import math
import os
os.chdir("C:/Users/Shichen/SkyDrive/Documents/Homework/CSC180")


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    #print(vec, sum_of_squares)
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    
    sum = 0.0
    
    if len(vec1) > len(vec2):
        for key in vec2:
            if key in vec1:
                sum += vec1[key] * vec2[key]
    else:
        for key in vec1:    
            if key in vec2:
                sum += vec1[key] * vec2[key]
    #print("---------------------------------")
    return sum/(norm(vec1)*norm(vec2))

  
def neg_dist_similarity(vec1, vec2):
    
    vecdiff = {}
    
    for i in vec1:
        if i in vec2:
            vecdiff[i] = vec1[i] - vec2[i]
        else:
            vecdiff[i] = vec1[i]
            
    for i in vec2:
        if i not in vecdiff:
            vecdiff[i] = vec2[i]

    return -norm(vecdiff)

def neg_norm_dist_similarity(vec1, vec2):
    
    vecdiff = {}
    vecx = {}
    vecy = {}
    normvec1 = norm(vec1)
    normvec2 = norm(vec2)
    
    for i in vec1:
        vecx[i] = vec1[i] / normvec1
    for i in vec2:
        vecy[i] = vec2[i] / normvec2
    
    for i in vecx:
        if i in vecy:
            vecdiff[i] = vecx[i] - vecy[i]
        else:
            vecdiff[i] = vecx[i]
            
    for i in vecy:
        if i not in vecdiff:
            vecdiff[i] = vecy[i]
    
    return -norm(vecdiff)
    
def build_semantic_descriptors(sentences):
    
    d = {}
    words_ignore = []
    
    for i in range(len(sentences)):
        if len(sentences[i]) == 1:
            continue
        for z in range(len(sentences[i])):
            word = sentences[i][z]
            if word not in words_ignore:
                if word not in d:
                    d[word] = {}
                for j in sentences[i]:
                    if j != word:
                        if j not in d[word]:
                            d[word][j] = 1
                        else:
                            d[word][j] += 1
                            
            words_ignore += [word]
        words_ignore = []
        
        
    return d

def build_semantic_descriptors_from_files(filenames):
    
    text = ""
    res = []
    
    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="utf-8-sig")
        str = f.read()
        
        L = [',', '-', '--', ':', ';', '"', "'"]
        
        for i in L:
            str = str.replace(i, " ")
            
        str = str.replace("?" , ".")
        str = str.replace("!" , ".")
            
        text += str + " "
    
    text = text.lower()
    sentences = text.split(".")
    #print(sentences)
    
    i = 0
    t = 0
    #str[i] = str[i].split() may speed this up
    while i < len(sentences):
        words = sentences[i].split()
        #print(words)
        res += [[]]
        #print(res)
        for z in range(len(words)):
            #print(z)
            #print(words)
            res[t].append(words[z])
        t += 1
        i += 1
            
    return build_semantic_descriptors(res)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    
    highest_score = -100    
    cur_word = ""
    
    if word not in semantic_descriptors:
        return choices[0]
    
    for i in range(len(choices)):
        if choices[i] in semantic_descriptors:
            #print(word, choices[i])
            score = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
            if score > highest_score:
                highest_score = score
                cur_word = choices[i]
        
        else:
            if highest_score < -1:
                highest_score = -1
                cur_word = choices[i]
    
    
    return cur_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    
    f = open(filename, "r", encoding="utf-8")
    str = f.read()
    #print(str)
    str = str.split("\n")
    #print(str)
    #list = []
    for i in range(len(str)):
        str[i] = str[i].split()
    
    correct = 0.0
    total = 0.0
    for i in range(len(str)):
        if most_similar_word(str[i][0], str[i][2:], semantic_descriptors, similarity_fn) == str[i][1]:
            correct += 1
        
        total += 1
    
    return correct/total
            



#####

man = {"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}
liver = {"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}

#print(cosine_similarity(man, liver)*(math.sqrt(130)))

#print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

# print(build_semantic_descriptors([["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"],
# ["i", "am", "an", "unattractive", "man"],
# ["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]))

#print(run_similarity_test("test2.txt", build_semantic_descriptors_from_files(["warandpeace.txt"]), cosine_similarity))

import time
t = time.clock()
d = build_semantic_descriptors_from_files(["warandpeace.txt", "swannsway.txt"])
print(time.clock() - t)
print(run_similarity_test("test2.txt", d, cosine_similarity))




