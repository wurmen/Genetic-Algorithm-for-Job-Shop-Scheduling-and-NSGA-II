# Solving Job shop scheduling problem with Nondominated Sorting Genetic Algorithm II

*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/07/15*
<br>

## :black_nib: 問題描述 <br>
本範例是一個 10x10 的 Jop shop 問題，共有10個工件與10台機台，此問題是個多目標排程問題，共有兩個目標分別為最小化總完工時間 (Makespan)及總加權提早時間及延遲時間 (Total weighted earliness and tardiness, TWET) ，工件資訊如下表所示，工件資訊是以工件的加工作業程序來呈現，每個工件都會經過10個加工作業，下表紀錄著工件在每一個加工作業程序的加工機台以及加工所需時間，另外還有每個工件的優先度及到期時間 (參考自 [Min-YouWu, 2016](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclcdr&s=id=%22104NCKU5621001%22.&searchmode=basic) )<br>

- Processing time  
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/NSGA-II/picture/1.png" width="650" height="300">
</div>
<br>
<br>

- Machine sequence 
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/NSGA-II/picture/2.png" width="650" height="300">
</div>
<br>

-  Priority and Due date
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/NSGA-II/picture/3.png" width="200" height="300">
</div>
<br>

### :arrow_down_small: 排程目標 <br>

本範例為多目標排程問題，共有兩個目標分別為最小化總完工時間 (Makespan)及總加權提早時間及延遲時間 (Total weighted earliness and tardiness, TWET) 
，此兩個目標為衝突目標， makespan 期望越早完工越好，但 TWET 則希望完工時間越符合交期越好，太早或太晚完成都會給予懲罰值，因此必須在這兩個解之間做權衡。<br>

### :arrow_down_small: 編碼與解碼  <br>
這裡的編碼方式與前面介紹 GA 求解 Job shop 問題相同，主要參考 [Gen-Tsujimura-Kubota’s Method (1994, 1997)](https://ieeexplore.ieee.org/document/400072/)所提出的 Job shop 排程問題的染色體編碼方式。<br>

此方法的概念是將染色體表示為一組工件的作業加工程序，一個基因代表一個工件的加工作業，根據工件在染色體出現的次數，來得知各個工件目前的加工作業，再來對應各工件的加工機台及加工時間，藉此來進行排程。<br>

假設現在有一個具有 N 個工件 M 台機台的 Job shop 排程問題，那一個染色體將會由 N x M 個基因所組成，因為每個工件在每台機台只會被加工一次，共要被 M 台機台加工，所以每個工件在染色體裡將會出現 M 次，這裡舉上面3 x 3的 Job shop 問題為例<br>

O<sub>ijk</sup></sub> 表示工件 i 在作業程序 j 使用第 k 台機台 

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/5.png" width="780" height="420">
</div>
<br>

## :black_nib: 程式說明 <br>

這裡主要針對程式中幾個重要區塊來說明，有些細節並無放入，如有需要請參考[完整程式碼](https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/NSGA-II/NSGA-II%20code.py)或[範例檔案](https://wurmen.github.io/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/implementation%20with%20python/NSGA-II/Example_NSGAII.html)<br>

:bulb:由於下列程式有三個主要函式，建議可自行 print 函式的輸入與輸出值，以利裡解函式的執行過程 

### :arrow_down_small: 導入所需套件 <br>

```python
'''==========Solving job shop scheduling problem by gentic algorithm in python======='''
# importing required modules
import pandas as pd
import numpy as np
import time
import copy
```

### :arrow_down_small: 初始設定 <br>
此區主要包含讀檔或是資料給定，以及一些參數上的設定
```python
''' ================= initialization setting ======================'''
num_job=10 # number of jobs
num_mc=10 # number of machines

pt_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Processing Time",index_col =[0])
ms_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Machines Sequence",index_col =[0])
job_priority_duedate_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Priority",index_col =[0])

# raw_input is used in python 2
population_size=int(input('Please input the size of population: ') or 20) # default value is 20
crossover_rate=float(input('Please input the size of Crossover Rate: ') or 0.8) # default value is 0.8
mutation_rate=float(input('Please input the size of Mutation Rate: ') or 0.3) # default value is 0.3
mutation_selection_rate=float(input('Please input the mutation selection rate: ') or 0.4)
num_mutation_jobs=round(num_job*num_mc*mutation_selection_rate)
num_iteration=int(input('Please input number of iteration: ') or 1000) # default value is 1000

# speed up the data search
# Below code can also be  written "pt = pt_tmp.as_matrix().tolist()"
pt=[list(map(int, pt_tmp.iloc[i])) for i in range(num_job)]
ms=[list(map(int,ms_tmp.iloc[i])) for i in range(num_job)]
job_priority_duedate=[list(job_priority_duedate_tmp.iloc[i]) for i in range(num_job)]
start_time = time.time()

```
### :arrow_down_small: 非凌越排序函式 <br>
- 此函式有兩個輸入-族群大小及族群內各染色體的兩個適應值 (makespan and TWET)，此兩個值紀錄於 chroms_obj_record 字典中
- 輸出各個前緣所包含的染色體 index
```python
'''-------non-dominated sorting function-------'''      
def non_dominated_sorting(population_size,chroms_obj_record):
    s,n={},{}
    front,rank={},{}
    front[0]=[]     
    for p in range(population_size*2):
        s[p]=[]
        n[p]=0
        for q in range(population_size*2):
            
            if ((chroms_obj_record[p][0]<chroms_obj_record[q][0] and chroms_obj_record[p][1]<chroms_obj_record[q][1]) or (chroms_obj_record[p][0]<=chroms_obj_record[q][0] and chroms_obj_record[p][1]<chroms_obj_record[q][1])
            or (chroms_obj_record[p][0]<chroms_obj_record[q][0] and chroms_obj_record[p][1]<=chroms_obj_record[q][1])):
                if q not in s[p]:
                    s[p].append(q)
            elif ((chroms_obj_record[p][0]>chroms_obj_record[q][0] and chroms_obj_record[p][1]>chroms_obj_record[q][1]) or (chroms_obj_record[p][0]>=chroms_obj_record[q][0] and chroms_obj_record[p][1]>chroms_obj_record[q][1])
            or (chroms_obj_record[p][0]>chroms_obj_record[q][0] and chroms_obj_record[p][1]>=chroms_obj_record[q][1])):
                n[p]=n[p]+1
        if n[p]==0:
            rank[p]=0
            if p not in front[0]:
                front[0].append(p)
    
    i=0
    while (front[i]!=[]):
        Q=[]
        for p in front[i]:
            for q in s[p]:
                n[q]=n[q]-1
                if n[q]==0:
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i=i+1
        front[i]=Q
                
    del front[len(front)-1]
    return front
```
### :arrow_down_small: 計算擁擠距離的函式 <br>
- 輸入：要被計算的前緣內含的染色體 index 、目前所有染色體的適應值 (可透過前者輸入的index去抓要被計算染色體的適應值)
- 輸出：被計算染色體的擁擠距離
```python
'''--------calculate crowding distance function---------'''
def calculate_crowding_distance(front,chroms_obj_record):
    
    distance={m:0 for m in front}
    for o in range(2):
        obj={m:chroms_obj_record[m][o] for m in front}
        sorted_keys=sorted(obj, key=obj.get)
        distance[sorted_keys[0]]=distance[sorted_keys[len(front)-1]]=999999999999
        for i in range(1,len(front)-1):
            if len(set(obj.values()))==1:
                distance[sorted_keys[i]]=distance[sorted_keys[i]]
            else:
                distance[sorted_keys[i]]=distance[sorted_keys[i]]+(obj[sorted_keys[i+1]]-obj[sorted_keys[i-1]])/(obj[sorted_keys[len(front)-1]]-obj[sorted_keys[0]])
            
    return distance 
```
### :arrow_down_small: 選擇函式 <br>
此函式內部會呼叫計算擁擠距離的函式 (calculate_crowding_distance)，因為在選擇染色體形成新族群的過程中，當剩餘要被挑選的染色體數，小於當前的凌越前緣內的染色體數時，就必須透過擁擠距離來判斷我要選擇哪一條染色體。<br>
- 輸入：族群大小、由非凌越函式得到的各前緣內含的染色體 index、要被選擇的所有染色體的適應值以及各染色體的排程結果 list
- 輸出：新的族群 list 及 族群內在原本族群 list 中的 index 
```python
'''----------selection----------'''
def selection(population_size,front,chroms_obj_record,total_chromosome):   
    N=0
    new_pop=[]
    while N < population_size:
        for i in range(len(front)):
            N=N+len(front[i])
            if N > population_size:
                distance=calculate_crowding_distance(front[i],chroms_obj_record)
                sorted_cdf=sorted(distance, key=distance.get)
                sorted_cdf.reverse()
                for j in sorted_cdf:
                    if len(new_pop)==population_size:
                        break                
                    new_pop.append(j)              
                break
            else:
                new_pop.extend(front[i])
    
    population_list=[]
    for n in new_pop:
        population_list.append(total_chromosome[n])
    
    return population_list,new_pop
```
### :arrow_down_small: 產生初始解 <br>

根據上述所設定的族群大小，透過隨機的方式，產生初始族群，每個染色體共有 10 x 10 = 100  個基因，每一個染色體由一個 list 來儲存

```python
'''----- generate initial population -----'''
best_list,best_obj=[],[]
population_list=[]
for i in range(population_size):
    nxm_random_num=list(np.random.permutation(num_job*num_mc)) # generate a random permutation of 0 to num_job*num_mc-1
    population_list.append(nxm_random_num) # add to the population_list
    for j in range(num_job*num_mc):
        population_list[i][j]=population_list[i][j]%num_job # convert to job number format, every job appears m times

```

### :arrow_down_small: 交配 <br>
這裡採用雙點交配法，一開始會先產生一組用來選擇親代染色體的隨機序列，接著從序列中，兩個兩個抓出來，根據交配率來決定是否要進行交配，如果要，則交配產生兩個子代，並取代原本的親代染色體
```python
    '''-------- two point crossover --------'''
    parent_list=copy.deepcopy(population_list)
    offspring_list=[]
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    
    for m in range(int(population_size/2)):
        
        parent_1= population_list[S[2*m]][:]
        parent_2= population_list[S[2*m+1]][:]
        child_1=parent_1[:]
        child_2=parent_2[:]
        
        cutpoint=list(np.random.choice(num_job*num_mc, 2, replace=False))
        cutpoint.sort()
    
        child_1[cutpoint[0]:cutpoint[1]]=parent_2[cutpoint[0]:cutpoint[1]]
        child_2[cutpoint[0]:cutpoint[1]]=parent_1[cutpoint[0]:cutpoint[1]]
        
        offspring_list.extend((child_1,child_2)) # append child chromosome to offspring list
```
### :arrow_down_small: 修復 <br>
本範例是一個 10 x 10 的 Job shop 問題，因此每個工件在染色體出現的次數為10次，但由於上面進行交配的動作，會導致有些染色體內的工件出現次數會小於10或大於10，而形成一個不可行的排程解，所以這裡必須針對不可行的染色體進行修復動作，使它成為一個可行排程

```python
    '''----------repairment-------------'''
    for m in range(population_size):
        job_count={}
        larger,less=[],[] # 'larger' record jobs appear in the chromosome more than m times, and 'less' records less than m times.
        for i in range(num_job):
            if i in offspring_list[m]:
                count=offspring_list[m].count(i)
                pos=offspring_list[m].index(i)
                job_count[i]=[count,pos] # store the above two values to the job_count dictionary
            else:
                count=0
                job_count[i]=[count,0]
            if count>num_mc:
                larger.append(i)
            elif count<num_mc:
                less.append(i)
                
        for k in range(len(larger)):
            chg_job=larger[k]
            while job_count[chg_job][0]>num_mc:
                for d in range(len(less)):
                    if job_count[less[d]][0]<num_mc:                    
                        offspring_list[m][job_count[chg_job][1]]=less[d]
                        job_count[chg_job][1]=offspring_list[m].index(chg_job)
                        job_count[chg_job][0]=job_count[chg_job][0]-1
                        job_count[less[d]][0]=job_count[less[d]][0]+1                    
                    if job_count[chg_job][0]==num_mc:
                        break 
```
### :arrow_down_small: 突變 <br>

這裡採用的突變方式跟 [Flow shop](https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/GA%20for%20flow%20shop%20problem.md) 的例子相同，是透過基因位移的方式進行突變，突變方式如下:<br>
1. 依據 mutation selection rate 決定染色體中有多少百分比的基因要進行突變，假設每條染色體有六個基因， mutation selection rate 為0.5，則有3個基因要進行突變。
2. 隨機選定要位移的基因，假設選定5、2、6 (在此表示該位置下的基因要進行突變)
3. 進行基因移轉，移轉方式如圖所示。
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/6.png" width="450" height="250">
</div>
<br>

```python
    '''--------mutatuon--------'''   
    for m in range(len(offspring_list)):
        mutation_prob=np.random.rand()
        if mutation_rate <= mutation_prob:
            m_chg=list(np.random.choice(num_job*num_mc, num_mutation_jobs, replace=False)) # chooses the position to mutation
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1):
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position   
  
```
### :arrow_down_small: 適應值計算 <br>
- 計算每個染色體的兩個目標值- makespan and TWET
- 這裡會將親代 (parent_list) 與子代 (offspring_list) 合併成一個大的list (total_chromosome)，後續選擇時是從這個大 list 來進行選擇，產生新族群
```python
     '''--------fitness value(calculate  makespan and TWET)-------------'''
    total_chromosome=copy.deepcopy(parent_list)+copy.deepcopy(offspring_list) # combine parent and offspring chromosomes
    chroms_obj_record={} # record each chromosome objective values as chromosome_obj_record={chromosome:[TWET,makespan]}
    for m in range(population_size*2):
        j_keys=[j for j in range(num_job)]
        key_count={key:0 for key in j_keys}
        j_count={key:0 for key in j_keys}
        m_keys=[j+1 for j in range(num_mc)]
        m_count={key:0 for key in m_keys}
        d_record={} # record jobs earliness and tardiness time as d_record={job:[earliness time,tardiness time]}
        
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
    
        for j in j_keys:
            if j_count[j]>job_priority_duedate[j][1]:
                job_tardiness=j_count[j]-job_priority_duedate[j][1]
                job_earliness=0
                d_record[j]=[job_earliness,job_tardiness]
            elif j_count[j]<job_priority_duedate[j][1]:
                job_tardiness=0
                job_earliness=job_priority_duedate[j][1]-j_count[j]
                d_record[j]=[job_earliness,job_tardiness]
            else:
                job_tardiness=0
                job_earliness=0
                d_record[j]=[job_earliness,job_tardiness]
        
        twet=sum((1/job_priority_duedate[j][0])*d_record[j][0]+job_priority_duedate[j][0]*d_record[j][1] for j in j_keys)
        makespan=max(j_count.values())
        chroms_obj_record[m]=[twet,makespan]
```
### :arrow_down_small: 非凌越排序計算  <br>
```python
    '''-------non-dominated sorting-------'''      
    front=non_dominated_sorting(population_size,chroms_obj_record
```
### :arrow_down_small: 選擇  <br>

```python
    '''----------selection----------'''
    population_list,new_pop=selection(population_size,front,chroms_obj_record,total_chromosome)
    new_pop_obj=[chroms_obj_record[k] for k in new_pop]
```

### :arrow_down_small: 比較 <br>
將此輪找到最好的那些解，與目前為止迭代中找到得最好的解進行比較
```
    '''----------comparison----------'''
	if n==0:
        best_list=copy.deepcopy(population_list)
        best_obj=copy.deepcopy(new_pop_obj)
    else:            
        total_list=copy.deepcopy(population_list)+copy.deepcopy(best_list)
        total_obj=copy.deepcopy(new_pop_obj)+copy.deepcopy(best_obj)
        
        now_best_front=non_dominated_sorting(population_size,total_obj)
        best_list,best_pop=selection(population_size,now_best_front,total_obj,total_list)
        best_obj=[total_obj[k] for k in best_pop]
```

### :arrow_down_small: 結果 <br>
最終會輸出在所有迭代過程中找到最好的解，由於這是多目標問題，所以可能會有多組解，這邊的設定是，輸出與族群大小相同數量的解
```python
'''----------result----------'''
print(best_list)
print(best_obj)
print('the elapsed time:%s'% (time.time() - start_time)
```

## :black_nib: Reference <br>
- [Wu, Min-You, Multi-Objective Stochastic Scheduling Optimization: A Study of Auto Parts Manufacturer in Taiwan](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclcdr&s=id=%22104NCKU5621001%22.&searchmode=basic)
