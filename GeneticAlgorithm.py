from CNF_Creator import *
import time
import random
import numpy as np
import matplotlib.pyplot as plt
#from tqdm import tqdm
'''If you want to run the alternate main function (the one used for plotting the final graphs)
then uncomment the genetic algorithm return statement with 3 arguments'''

def fitness_function(model,sentence):
    count=0
    total=len(sentence)
    acc_list=[False for i in sentence]
    i=0
    for clause in sentence:
        for varz in clause:
            if (varz>0 and model[varz-1]==True):
                acc_list[i]=True
            elif (varz<0 and model[(-1*varz)-1]==False):
                acc_list[i]=True
        if(acc_list[i]==True):
            count+=1
        i=i+1
    return float((count/total)*100)

def random_model_gen(n=50):
    model=[False for i in range (0,50,1)]
    for i in range(0,50,1):
        random_bool_var=random.randint(0,1)
        if(random_bool_var==0):
            model[i]=False
        elif (random_bool_var==1):
            model[i]=True
    return model

def population_gen(population_size):
    all_models=[]
    for i in range (0, population_size,1):
        temp_model=random_model_gen()
        all_models.append(temp_model)
    return all_models


def weighted_by(population, sentence):
    weights=[0 for i in population]
    total=0
    i=0
    for model in population:
        weights[i]=fitness_function(model, sentence)
        total+=weights[i]
        i+=1
    i=0
    for model in population:
        weights[i]/=total
        i=i+1
    return weights
    
        

def weighted_random_choices(population, weights,n=2):
    weighted_list=random.choices(population, weights=weights,k=n)
    return weighted_list

def reproduce(parent1, parent2,parent3):
    len_parent=len(parent1)
    pivot=random.randint(0, len_parent-2)
    pivot2=random.randint(pivot+1, len_parent-1)
    child=[False for i in range (0,len_parent,1)]
    for i in range(0, pivot):
        child[i]=parent1[i]
    for i in range(pivot, pivot2):
        child[i]=parent2[i]
    for i in range(pivot2, len_parent):
        child[i]=parent3[i]
    return child
'''
def reproduce(parent1, parent2):
    len_parent=len(parent1)
    pivot=random.randint(0, len_parent-1)
    child=[False for i in range (0,len_parent,1)]
    for i in range(0, pivot):
        child[i]=parent1[i]
    for i in range(pivot, len_parent):
        child[i]=parent2[i]
    return child'''

def mutate(child, n):
    index_list=random.sample([*range(0,50,1)],n)
    new_child=child
    for random_idx in index_list:
        new_child[random_idx] = not(new_child[random_idx])
    return new_child
    

def genetic_algo(population,sentence):
    initial_time=time.perf_counter()
    now=time.perf_counter()
    best_child=population[0]
    best_child_in_loop=population[0]
    max_child_accuracy=fitness_function(best_child, sentence)
    max_child_in_loop=0
    early_stop_time=initial_time
    all_fitness=[]
    random_restarts=0
    while (now-initial_time<44 and max_child_accuracy<100 and random_restarts<5):
            weights=weighted_by(population, sentence)
            population2=[]
            max_child_in_loop=0
            for i in range(0,len(population),1):  
                [parent1,parent2,parent3]=weighted_random_choices(population, weights, 3)
                child=reproduce(parent1, parent2, parent3)
                if (random.randint(0,4)==1):
                    child=mutate(child,5)
                population2.append(child)
                fit_func=fitness_function(child, sentence)
                if(fit_func>max_child_in_loop):
                    best_child_in_loop=child
                max_child_in_loop=max(max_child_in_loop,fit_func)
                
    
            both_populations=population+population2 #implementing elitism
            both_populations=sorted(both_populations, key=lambda x: fitness_function(x,sentence), reverse=True)
            population=both_populations[0:len(population)]

            now=time.perf_counter()
            all_fitness.append(max_child_in_loop)
            if(max_child_accuracy<max_child_in_loop):
                early_stop_time=now  #finding the time of the beginning of the plateau/decline
            if(max_child_in_loop>max_child_accuracy):
                    best_child=best_child_in_loop
                    max_child_accuracy=max_child_in_loop
            if(now-early_stop_time>5):
                population=population_gen(len(population)) #random restart
                early_stop_time=now
                random_restarts+=1
                
    return best_child, max_child_accuracy, all_fitness
    #return best_child, max_child_accuracy


def main():
    initial_time=time.perf_counter()
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    #sentence = cnfC.CreateRandomSentence(m=200) # m is number of clauses in the 3-CNF sentence
    #('Random sentence : ',sentence)
    
    sentence = cnfC.ReadCNFfromCSVfile()
    print('\nSentence from CSV file : ',sentence)
    

    print('\n\n')
    print('Roll No : 2018B5A70881G')
    print('Number of clauses in CSV file : ',len(sentence))
    
    all_models=population_gen(50)
    best_child, max_child_accuracy, all_fitness= genetic_algo(all_models, sentence)
    now=time.perf_counter()
    
    print('Best model : ', best_child)
    print('Fitness value of best model :', max_child_accuracy)
    print('Time taken :', now-initial_time)
    print('\n\n')
    
    return all_fitness

if __name__=="__main__":
    all_fitness=main()
'''
def for_m(m):
    initial_time=time.perf_counter()
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    sentence = cnfC.CreateRandomSentence(m) # m is number of clauses in the 3-CNF sentence
    #print('Random sentence : ',sentence)
    
    #sentence = cnfC.ReadCNFfromCSVfile()
    #print('\nSentence from CSV file : ',sentence)
    

    #print('\n\n')
    #print('Roll No : 2018B5A70881G')
    #print('Number of clauses in CSV file : ',len(sentence))
    
    all_models=population_gen(100)
    best_child, max_child_accuracy= genetic_algo(all_models, sentence)
    now=time.perf_counter()
    
    
    
    #print('Best model : ', best_child)
    print('Fitness value of best model :', max_child_accuracy)
    #print('Time taken :', now-initial_time)
    #print('\n\n')
    return best_child, max_child_accuracy, now-initial_time

def average_for_m(count,m):
    best_model=[]
    av_accuracy=0
    total_time=0
    for i in tqdm(range(0,count,1)):
        model, accuracy, time=for_m(m)
        total_time+=time
        av_accuracy+=accuracy
        
    return av_accuracy/count, total_time/count
        
def main():
    acc=[]
    time=[]
    for i in range(100,320,20):
        max_accuracy, avg_time=average_for_m(50,i)
        acc.append(max_accuracy)
        time.append(avg_time)
        #plt.scatter(i,max_accuracy)
        #plt.show()
        #plt.pause(0.0001)
    return acc,time
        
acc,time=main()'''