# Solving Job shop scheduling problem with genetic algorithm

*[POLab](http://polab.imis.ncku.edu.tw/)* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/12/01*
<br>

## :black_nib: 前言 <br>

這裡要來說明如何運用 GA 來求解 Job shop 的問題，以下將先對 Job shop 問題做個簡介，接著描述本範例的求解問題以及編碼與解碼說明，最後會根據每個程式區塊進行概念上的講解

### :arrow_down_small: 什麼是 Job shop 問題? <br>

Jop shop 問題與 Flow shop 問題最大的不同在於，不像 Flow shop 問題中，每個工件在機台的加工順序都是相同的，在 Job shop 問題裡，每個工件都有屬於自己的機台加工順序，如下圖所示：<br>
此為一個3x3的 Job shop 問題
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/1.png" width="650" height="250">
</div>
<br>

## :black_nib: 問題描述 <br>
本範例是一個 10x10 的 Job shop 問題，共有10個工件與10台機台，每個工件在每台機台的加工順序都不同，排程目標為最小化總完工時間 (Makespan) ，資料是以工件的加工作業順序來呈現，每個工件都會經過10個加工作業，下表紀錄著每個工件在每一個加工作業的加工機台以及加工所需時間<br>

- Processing time  
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/2.png" width="650" height="300">
</div>
<br>
<br>

- Machine sequence 
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/3.png" width="650" height="300">
</div>
<br>

### :arrow_down_small: 排程目標 <br>
本範例的目標為最小化總完工時間 (Makespan)，也就是說要最小化整個排程的執行時間，以前面的例子為例，該範例的完工時間是 Job 3 在機台1的完工時間點，因為對於此排程結果來說，Job 3 是所有工件中，最後一個完成的，因此此排程的完工時間，就是Job 3 完成的時間點

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/4.png" width="450" height="180">
</div>
<br>

### :arrow_down_small: 編碼與解碼  <br>
這裡主要參考 [Gen-Tsujimura-Kubota’s Method (1994, 1997)](https://ieeexplore.ieee.org/document/400072/)所提出的 Job shop 排程問題的染色體編碼方式。<br>

此方法的概念是將染色體表示為一組工件的作業加工順序，一個基因代表一個工件的加工作業，根據工件在染色體出現的次數，來得知各個工件目前的加工作業，再來對應各工件的加工機台及加工時間，藉此來進行排程。<br>

假設現在有一個具有 N 個工件 M 台機台的 Job shop 排程問題，那一個染色體將會由 N x M 個基因所組成，因為每個工件在每台機台只會被加工一次，共要被 M 台機台加工，所以每個工件在染色體裡將會出現 M 次，這裡舉上面3 x 3的 Job shop 問題為例 <br>

O<sub>ijk</sup></sub> 表示工件 i 在作業程序 j 使用第 k 台機台 

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/5.png" width="780" height="420">
</div>
<br>


## :black_nib: 程式說明 <br>

這裡主要針對程式中幾個重要區塊來說明，有些細節並無放入，如有需要請參考[完整程式碼](https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/GA_jobshop_makespan.py)或[範例檔案](https://wurmen.github.io/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/implementation%20with%20python/GA-jobshop/Example1.html)

### :arrow_down_small: 導入所需套件 <br>

```python
'''==========Solving job shop scheduling problem by gentic algorithm in python======='''
# importing required modules
import pandas as pd
import numpy as np
import time
```

### :arrow_down_small: 初始設定 <br>
此區主要包含讀檔或是資料給定，以及一些參數上的設定
```python
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

```

### :arrow_down_small: 產生初始解 <br>
根據上述所設定的族群大小，透過隨機的方式，產生初始族群，每個染色體共有 10 x 10 = 100  個基因
```python
'''----- generate initial population -----'''
Tbest=999999999999999
best_list,best_obj=[],[]
population_list=[]
for i in range(population_size):
    nxm_random_num=list(np.random.permutation(num_gene)) # generate a random permutation of 0 to num_job*num_mc-1
    population_list.append(nxm_random_num) # add to the population_list
    for j in range(num_gene):
        population_list[i][j]=population_list[i][j]%num_job # convert to job number format, every job appears m times

```

### :arrow_down_small: 交配 <br>

一開始會先產生一組用來選擇親代染色體的隨機序列，接著從序列中，兩個兩個抓出來，根據交配率來決定是否要進行交配，如果要，則採用雙點交配法，產生兩個子代，並取代原本的母代染色體

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/6.png" width="450" height="300">
</div>
<br>

```python
    '''-------- two point crossover --------'''
	parent_list=copy.deepcopy(population_list) # preserve the original parent chromosomes
    offspring_list=copy.deepcopy(population_list)
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    
    for m in range(int(population_size/2)):
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob:
            parent_1= population_list[S[2*m]][:]
            parent_2= population_list[S[2*m+1]][:]
            child_1=parent_1[:]
            child_2=parent_2[:]
            cutpoint=list(np.random.choice(num_gene, 2, replace=False))
            cutpoint.sort()
        
            child_1[cutpoint[0]:cutpoint[1]]=parent_2[cutpoint[0]:cutpoint[1]]
            child_2[cutpoint[0]:cutpoint[1]]=parent_1[cutpoint[0]:cutpoint[1]]
            offspring_list[S[2*m]]=child_1[:]
            offspring_list[S[2*m+1]]=child_2[:]
```
### :arrow_down_small: 修復 <br>
本範例是一個 10 x 10 的 Job shop 問題，因此每個工件在染色體出現的次數為10次，但由於上面進行交配的動作，會導致有些染色體內的工件出現次數會小於10或大於10，而形成一個不可行的排程解，所以這裡必須針對不可行的染色體進行修復動作，使它成為一個可行排程

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/7.png" width="450" height="285">
</div>
<br>

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
        if mutation_rate >= mutation_prob:
            m_chg=list(np.random.choice(num_gene, num_mutation_jobs, replace=False)) # chooses the position to mutation
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1):
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position
  
```
### :arrow_down_small: 適應值計算 <br>

計算每個染色體所形成的排程結果的完工時間，並將其記錄，以利後續選擇時能比較<br>

:bulb: 這裡要注意的是，因為這是最小化的問題，因此每個染色體所算出的適應值，也就是完工時間，必須以倒數的方式記錄 (chrom_fitness)，這樣後面採用輪盤法時，才可以選到完工時間越小的染色體，不過這邊還是有另外紀錄每個染色體原本的完工時間 (chrom_fit)，以利最後面再篩選此輪最佳解時，可直接比較

```python
    '''--------fitness value(calculate makespan)-------------'''
    total_chromosome=copy.deepcopy(parent_list)+copy.deepcopy(offspring_list) # parent and offspring chromosomes combination
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
```

### :arrow_down_small: 選擇  <br>

這裡採用輪盤法 (Roulette wheel) 的選擇機制<br>

```python
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
			population_list[i]=copy.deepcopy(total_chromosome[0])
        else:
            for j in range(0,population_size*2-1):
                if selection_rand[i]>qk[j] and selection_rand[i]<=qk[j+1]:
					population_list[i]=copy.deepcopy(total_chromosome[j+1])
                    break
```

### :arrow_down_small: 比較 <br>
先比較每個染色體的完工時間 (chrom_fit) ，選出此輪找到的最好解 (Tbest_now) ，接著在跟目前為止找到的最好解 (Tbest) 進行比較，一旦這一輪的解比目前為止找到的解還要好，就替代 Tbest 並記錄該解所得到的排程結果
```python
     '''----------comparison----------'''
    for i in range(population_size*2):
        if chrom_fit[i]<Tbest_now:
            Tbest_now=chrom_fit[i]
            sequence_now=copy.deepcopy(total_chromosome[i])
    
    if Tbest_now<=Tbest:
        Tbest=Tbest_now
        sequence_best=copy.deepcopy(sequence_now)
```

### :arrow_down_small: 結果 <br>
等迭代結束後，輸出在所有迭代中找到的最好排程結果 (sequence_best)、該結果的完工時間以及程式執行時間

```python
'''----------result----------'''
print("optimal sequence",sequence_best)
print("optimal value:%f"%Tbest)
print('the elapsed time:%s'% (time.time() - start_time))
```
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/8.JPG" width="700" height="350">
</div>
<br>

### :arrow_down_small: 甘特圖 <br>
在此使用python plotly package 來繪製甘特圖，詳細安裝方法，可參考[Plotly官網](https://plot.ly/python/getting-started/)
```python
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
```
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-jobshop/picture/9.JPG" width="650" height="350">
</div>
<br>

## :black_nib: Reference <br>
- [Wu, Min-You, Multi-Objective Stochastic Scheduling Optimization: A Study of Auto Parts Manufacturer in Taiwan](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclcdr&s=id=%22104NCKU5621001%22.&searchmode=basic)
- [Chin-Yi Tseng, Intelligent Manufacturing Systems](https://github.com/PO-LAB/Intelligent-Manufacturing-Systems)
- [
M. Gen, Y. Tsujimura, E. Kubota, Solving job-shop scheduling problem using genetic algorithms, Proc. of the 16th Int. Conf. on Computer and Industrial Engineering, Ashikaga, Japan (1994), pp. 576-579](https://ieeexplore.ieee.org/document/400072/)
- Chia-Yen Lee (2017), Meta-Heuristic Algorithms-Genetic Algorithms & Particle Swarm Optimization, Intelligent Manufacturing Systems course
