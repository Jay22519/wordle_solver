from django.shortcuts import render
from django.http import HttpResponse
# import requests 
from solver.models import English_corpus


import copy
import re
# Create your views here.
import os

word_regex = ['' , '' , '' , '' , ''] 
remove_list = set()
present_list = set()
updated_word_list = set()
count = 0 


def index(request):
    global updated_word_list 
    global word_regex
    global remove_list 
    global present_list
    global count


    my_file = open(os.path.join(os.getcwd() , 'solver/word_five.txt'), "r")
    data = my_file.read()

    data = data.split("\n")

    global updated_word_list 
    updated_word_list = set(data)

    data = {
        'length' : len(updated_word_list)
    }


    
    return render(request , "home.html" , data) 




def maintain_legth(word_set) :
    ws_copy = copy.deepcopy(word_set)

    for w in word_set :
        if(len(w) != 5) :
            ws_copy.discard(w) 

    return ws_copy



def solver_init(request) :
    global updated_word_list 
    global word_regex
    global remove_list 
    global present_list
    global count

    word_regex = ['' , '' , '' , '' , ''] 
    remove_list = set()
    present_list = set()
    updated_word_list = set()
    count = 0 



    print("Len of list in solver init : " , len(updated_word_list))


    if(len(updated_word_list) == 0) :
        my_file = open(os.path.join(os.getcwd() , 'solver/word_five.txt'), "r")
        data = my_file.read()

        data = data.split("\n")
        updated_word_list = set(data)




    word_get = request.GET['answer']
    code_get = request.GET['code']

    word_get = word_get.lower()
    code_get = code_get.lower()

    code_int = ['' , '' , '' , '', '']
    for i in range(5) :
        if(code_get[i] == 'g') :
            code_int[i] = 2

        elif(code_get[i] == 'y') :
            code_int[i] = 1

        else :
            code_int[i] = 0 


    print("Word is : " , word_get)

    a = word_get[0]
    b = word_get[1]
    c = word_get[2]
    d = word_get[3]
    e = word_get[4]



    val_a = int(code_int[0])
    val_b = int(code_int[1])
    val_c = int(code_int[2])
    val_d = int(code_int[3])
    val_e = int(code_int[4])

    if(val_a == 0 ) :
        remove_list.add(a)
    elif(val_a == 1) :
        present_list.add(a)
    else :
        word_regex[0] = a
        present_list.discard(a)
    
    
    if(val_b == 0 ) :
        remove_list.add(b)
    elif(val_b == 1) :
        present_list.add(b)
    else :
        word_regex[1] = b
        present_list.discard(b)
        
        
    if(val_c == 0 ) :
        remove_list.add(c)
    elif(val_c == 1) :
        present_list.add(c)
    else :
        word_regex[2] = c
        present_list.discard(c)
        
        
    if(val_d == 0 ) :
        remove_list.add(d)
    elif(val_d == 1) :
        present_list.add(d)
    else :
        word_regex[3] = d
        present_list.discard(d)
        
        
        
    if(val_e == 0 ) :
        remove_list.add(e)
    elif(val_e == 1) :
        present_list.add(e)
    else :
        word_regex[4] = e
        present_list.discard(e)


    ### Finding things with word_regex 
    
    updated_word_list_temp = copy.deepcopy(updated_word_list)
    updated_word_list = maintain_legth(updated_word_list)
    updated_word_list_temp = maintain_legth(updated_word_list_temp)
    for w in updated_word_list :
        for i in range(5) :
            if(word_regex[i] != '' and w[i] != word_regex[i]) :
                updated_word_list_temp.discard(w)
                break
                
                
    

    updated_word_list = copy.deepcopy(updated_word_list_temp)

    updated_word_list = maintain_legth(updated_word_list)
    updated_word_list_temp = maintain_legth(updated_word_list_temp)


    print("Len of list : " , len(updated_word_list))
    ## Removing words 
    updated_word_list_temp = copy.deepcopy(updated_word_list)
    for w in updated_word_list :
        for i in remove_list :
            for j in range(5) :
                try :
                    if(w[j] == i and word_regex[j] == '') :
                        updated_word_list_temp.discard(w)
                except :
                    print(w , "It's lengtg is : " , len(w))

                
    updated_word_list = copy.deepcopy(updated_word_list_temp)        
    
    ### Finding words that contains present_list at position where word_regex is null yet 
    new_list = set()
    for w in updated_word_list :
        
        ok_count = len(present_list) ## Word should contain all this
        temp = 0
        for i in present_list :
            for j in range(5) :
                if(w[j] == i and word_regex[j] == '') :
                    temp += 1
                    break 
        if(temp == ok_count) :
            new_list.add(w)
                    
            
            
    if(len(new_list) == 0) :
        new_list = updated_word_list
        
    print(len(new_list))
    
    count += 1 
    if(count > 1) :
        for j in new_list :
            print(j)
                    
    updated_word_list = new_list


    if(len(updated_word_list) == 0) :

        answer = "Seems like there is no words suggested based on your entry . This might happen because you have entered the word and code wrong or maybe because of some error at our end"
        link = "http://wordle-word-finder.herokuapp.com/"

        return render(request , "restart.html") 

    else :
        data = {
        "datas" : updated_word_list,
        'length' : len(updated_word_list) 
            }

        return render(request , "answer.html",data) 



def solver(request) :

    global updated_word_list 
    global word_regex
    global remove_list 
    global present_list
    global count


    

    print("Len of list : " , len(updated_word_list))



    word_get = request.GET['answer']
    code_get = request.GET['code']

    word_get = word_get.lower()
    code_get = code_get.lower()

    code_int = ['' , '' , '' , '', '']
    for i in range(5) :
        if(code_get[i] == 'g') :
            code_int[i] = 2

        elif(code_get[i] == 'y') :
            code_int[i] = 1

        else :
            code_int[i] = 0 


    print("Word is : " , word_get)

    a = word_get[0]
    b = word_get[1]
    c = word_get[2]
    d = word_get[3]
    e = word_get[4]



    val_a = int(code_int[0])
    val_b = int(code_int[1])
    val_c = int(code_int[2])
    val_d = int(code_int[3])
    val_e = int(code_int[4])

    if(val_a == 0 ) :
        remove_list.add(a)
    elif(val_a == 1) :
        present_list.add(a)
    else :
        word_regex[0] = a
        present_list.discard(a)
    
    
    if(val_b == 0 ) :
        remove_list.add(b)
    elif(val_b == 1) :
        present_list.add(b)
    else :
        word_regex[1] = b
        present_list.discard(b)
        
        
    if(val_c == 0 ) :
        remove_list.add(c)
    elif(val_c == 1) :
        present_list.add(c)
    else :
        word_regex[2] = c
        present_list.discard(c)
        
        
    if(val_d == 0 ) :
        remove_list.add(d)
    elif(val_d == 1) :
        present_list.add(d)
    else :
        word_regex[3] = d
        present_list.discard(d)
        
        
        
    if(val_e == 0 ) :
        remove_list.add(e)
    elif(val_e == 1) :
        present_list.add(e)
    else :
        word_regex[4] = e
        present_list.discard(e)


    ### Finding things with word_regex 
    
    updated_word_list_temp = copy.deepcopy(updated_word_list)
    updated_word_list = maintain_legth(updated_word_list)
    updated_word_list_temp = maintain_legth(updated_word_list_temp)
    for w in updated_word_list :
        for i in range(5) :
            if(word_regex[i] != '' and w[i] != word_regex[i]) :
                updated_word_list_temp.discard(w)
                break
                
                
    

    updated_word_list = copy.deepcopy(updated_word_list_temp)

    updated_word_list = maintain_legth(updated_word_list)
    updated_word_list_temp = maintain_legth(updated_word_list_temp)


    print("Len of list : " , len(updated_word_list))
    ## Removing words 
    updated_word_list_temp = copy.deepcopy(updated_word_list)
    for w in updated_word_list :
        for i in remove_list :
            for j in range(5) :
                try :
                    if(w[j] == i and word_regex[j] == '') :
                        updated_word_list_temp.discard(w)
                except :
                    print(w , "It's lengtg is : " , len(w))

                
    updated_word_list = copy.deepcopy(updated_word_list_temp)        
    
    ### Finding words that contains present_list at position where word_regex is null yet 
    new_list = set()
    for w in updated_word_list :
        
        ok_count = len(present_list) ## Word should contain all this
        temp = 0
        for i in present_list :
            for j in range(5) :
                if(w[j] == i and word_regex[j] == '') :
                    temp += 1
                    break 
        if(temp == ok_count) :
            new_list.add(w)
                    
            
            
    if(len(new_list) == 0) :
        new_list = updated_word_list
        
    print(len(new_list))
    
    count += 1 
    if(count > 1) :
        for j in new_list :
            print(j)
                    
    updated_word_list = new_list

    if(len(updated_word_list) == 0) :

        answer = "Seems like there is no words suggested based on your entry . This might happen because you have entered the word and code wrong or maybe because of some error at our end"
        link = "http://wordle-word-finder.herokuapp.com/"

        return render(request , "restart.html") 

    else :
        data = {
        "datas" : updated_word_list,
        'length' : len(updated_word_list) 
            }

        return render(request , "answer.html",data) 

                    






# # def loadData(request) :

#     my_file = open("C:/Users/JPG/Desktop/wordle/solver/word_five.txt", "r")
#     data = my_file.read()

#     data = data.split("\n")

#     data_dict = {}  # This data_dict will store individual word and add it to database 
#     for i in data :
#         data_dict['word'] = i 

#     data_created = English_corpus.create(**data_dict)  