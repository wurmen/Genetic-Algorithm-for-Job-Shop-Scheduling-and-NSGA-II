# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 01:14:12 2018

@author: wu
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:24:51 2018

Author: cheng-man wu
LinkedIn: www.linkedin.com/in/chengmanwu
Github: https://github.com/wurmen

"""

'''==========Solving job shop scheduling problem by gentic algorithm in python======='''
# importing required modules
import pandas as pd
import numpy as np
import time

'''================ repairment function ====================='''
def repairment(child,partial_parent,missed_gene,exceeded_gene):
    if exceeded_gene:
        for i in exceeded_gene:
            child.remove(i)
    count=0
    while count!=len(missed_gene):
        rand_index=[j for j in range(len(child)) if child[j] !='na']
        insert_pos=int(np.random.choice(rand_index,1, replace=False))
        child.insert(insert_pos, missed_gene[count])
        count+=1
    na_index=[i for i,x in enumerate(child) if x == 'na']
    for i in range(len(na_index)):
        child[na_index[i]]=partial_parent[i]
    return child
''' ================= initialization setting ======================'''

pt_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Processing Time",index_col =[0])
ms_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Machines Sequence",index_col =[0])

dfshape=pt_tmp.shape
num_mc=dfshape[1] # number of machines
num_job=dfshape[0] # number of jobs
num_gene=num_mc*num_job # number of genes in a chromosome

pt=[list(map(int, pt_tmp.iloc[i])) for i in range(num_job)]
ms=[list(map(int,ms_tmp.iloc[i])) for i in range(num_job)]




# raw_input is used in python 2
population_size=int(input('Please input the size of population: ') or 30) # default value is 30
crossover_rate=float(input('Please input the size of Crossover Rate: ') or 0.8) # default value is 0.8
mutation_rate=float(input('Please input the size of Mutation Rate: ') or 0.2) # default value is 0.2
mutation_selection_rate=float(input('Please input the mutation selection rate: ') or 0.2)
num_mutation_jobs=round(num_gene*mutation_selection_rate)
num_iteration=int(input('Please input number of iteration: ') or 2000) # default value is 2000
    
start_time = time.time()

'''==================== main code ==============================='''
'''----- generate initial population -----'''
Tbest=999999999999999
best_list,best_obj=[],[]
population_list=[]
for i in range(population_size):
    nxm_random_num=list(np.random.permutation(num_gene)) # generate a random permutation of 0 to num_job*num_mc-1
    population_list.append(nxm_random_num) # add to the population_list
    for j in range(num_gene):
        population_list[i][j]=population_list[i][j]%num_job # convert to job number format, every job appears m times
        
for n in range(num_iteration):
    Tbest_now=99999999999           
    '''-------- crossover --------'''
    parent_list=population_list[:]
    offspring_list=population_list[:]
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    
    for m in range(int(population_size/2)):
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob:
            parent_1= population_list[S[2*m]][:]
            parent_2= population_list[S[2*m+1]][:]
            child_1=parent_1[:]
            child_2=parent_2[:]
            cutpoint=int(np.random.choice(num_gene, 1, replace=False)) # choose one position in parent 1 randomly (which is also the position of the chosen job)
            chg_job=parent_1[cutpoint] # the chosen job
            job_index=[i for i,x in enumerate(parent_1) if x == chg_job] # get all indexes for the chosen job in parent1
            job_index.sort()
            
            if cutpoint==job_index[-1]:
                start_chg=job_index[-2]
                end_chg=cutpoint
            else:
                start_chg=cutpoint
                end_chg=job_index[job_index.index(cutpoint)+1]
            partial_parent1=parent_1[start_chg:end_chg+1]
            
            p2_job_index=[i for i,x in enumerate(parent_2) if x == chg_job]
            p2_job_index.sort()
            partial_parent2=parent_2[p2_job_index[0]:p2_job_index[1]+1]
            
            # In order to make them feasible, fill NA to the genes section which is exchanged for the child, 
            # and repair them using repairment function. 
            # exchange NA and partial parent after repairment.
            na_value1=['na' for i in range(len(partial_parent2))]
            na_value2=['na' for i in range(len(partial_parent1))]                   
            child_1[start_chg:end_chg+1]=na_value1[:]
            child_2[p2_job_index[0]:p2_job_index[1]+1]=na_value2[:]
        
            '''----------repairment-------------'''
            missed_gene=partial_parent1[:]
            exceeded_gene=partial_parent2[:]
            
            for i in partial_parent1:
                if i in exceeded_gene:
                    missed_gene.remove(i)   # get the missed gene of child_1 at the end (which is the exceeded gene of child_2)
                    exceeded_gene.remove(i) # get the exceeded gene of child_1 at the end (which is the missed gene of child_2)        
    
            # exchange partial parent1 and parent2 to get child_1 and child_2
            child_1=repairment(child_1,partial_parent2,missed_gene,exceeded_gene)
            child_2=repairment(child_2,partial_parent1,exceeded_gene,missed_gene)
            
            offspring_list[S[2*m]]=child_1[:]
            offspring_list[S[2*m+1]]=child_2[:]
   
    '''--------mutatuon--------'''   
    for m in range(len(offspring_list)):
        mutation_prob=np.random.rand()
        if mutation_rate >= mutation_prob:
            m_chg=list(np.random.choice(num_gene, num_mutation_jobs, replace=False)) # chooses the position for mutation
            chg_job= [offspring_list[m][i] for i in m_chg ]
            while len(set(chg_job))==1: # avoid choosing the same job for mutation
                m_chg=list(np.random.choice(num_gene, num_mutation_jobs, replace=False)) # chooses the position for mutation
                chg_job= [offspring_list[m][i] for i in m_chg ]
                
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1):
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position
    
    '''--------fitness value(calculate makespan)-------------'''
    total_chromosome=parent_list[:]+offspring_list[:] # combine parent and offspring chromosomes
    chrom_fitness,chrom_fit=[],[]
    total_fitness=0
    for m in range(population_size*2):
        j_keys=[j for j in range(num_job)]
        key_count={key:0 for key in j_keys}
        j_count={key:0 for key in j_keys}
        m_keys=[j+1 for j in range(num_mc)]
        m_count={key:0 for key in m_keys}
        
        for i in total_chromosome[m]:
            gen_t=int(pt[i][key_count[i]])
            gen_m=int(ms[i][key_count[i]])
            j_count[i]=j_count[i]+gen_t
            m_count[gen_m]=m_count[gen_m]+gen_t
            
            if m_count[gen_m]<j_count[i]:
                m_count[gen_m]=j_count[i]
            elif m_count[gen_m]>j_count[i]:
                j_count[i]=m_count[gen_m]
            
            key_count[i]=key_count[i]+1
    
        makespan=max(j_count.values())
        chrom_fitness.append(1/makespan)
        chrom_fit.append(makespan)
        total_fitness=total_fitness+chrom_fitness[m]

    
    '''----------selection(roulette wheel approach)----------'''
    pk,qk=[],[]
    
    for i in range(population_size*2):
        pk.append(chrom_fitness[i]/total_fitness)
    for i in range(population_size*2):
        cumulative=0
        for j in range(0,i+1):
            cumulative=cumulative+pk[j]
        qk.append(cumulative)
    
    selection_rand=[np.random.rand() for i in range(population_size)]
    
    for i in range(population_size):
        if selection_rand[i]<=qk[0]:
            population_list[i][:]=total_chromosome[0][:]
            break
        else:
            for j in range(0,population_size*2-1):
                if selection_rand[i]>qk[j] and selection_rand[i]<=qk[j+1]:
                    population_list[i][:]=total_chromosome[j+1][:]
            
    '''----------comparison----------'''
    for i in range(population_size*2):
        if chrom_fit[i]<Tbest_now:
            Tbest_now=chrom_fit[i]
            sequence_now=total_chromosome[i][:]
    
    if Tbest_now<=Tbest:
        Tbest=Tbest_now
        sequence_best=sequence_now[:]
    
'''----------result----------'''
print("optimal sequence",sequence_best)
print("optimal value:%f"%Tbest)
print('the elapsed time:%s'% (time.time() - start_time))

'''--------plot gantt chart-------'''
import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff
import datetime

m_keys=[j+1 for j in range(num_mc)]
j_keys=[j for j in range(num_job)]
key_count={key:0 for key in j_keys}
j_count={key:0 for key in j_keys}
m_count={key:0 for key in m_keys}
j_record={}
for i in sequence_best:
    gen_t=int(pt[i][key_count[i]])
    gen_m=int(ms[i][key_count[i]])
    j_count[i]=j_count[i]+gen_t
    m_count[gen_m]=m_count[gen_m]+gen_t
    
    if m_count[gen_m]<j_count[i]:
        m_count[gen_m]=j_count[i]
    elif m_count[gen_m]>j_count[i]:
        j_count[i]=m_count[gen_m]
    
    start_time=str(datetime.timedelta(seconds=j_count[i]-pt[i][key_count[i]])) # convert seconds to hours, minutes and seconds
    end_time=str(datetime.timedelta(seconds=j_count[i]))
        
    j_record[(i,gen_m)]=[start_time,end_time]
    
    key_count[i]=key_count[i]+1
        

df=[]
for m in m_keys:
    for j in j_keys:
        df.append(dict(Task='Machine %s'%(m), Start='2018-07-14 %s'%(str(j_record[(j,m)][0])), Finish='2018-07-14 %s'%(str(j_record[(j,m)][1])),Resource='Job %s'%(j+1)))
    
fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True, title='Job shop Schedule')
py.iplot(fig, filename='GA_job_shop_scheduling1', world_readable=True)


 