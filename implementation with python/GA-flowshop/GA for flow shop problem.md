# Solving flow shop scheduling problem with genetic algorithm

*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/07/14*
<br>

## :black_nib: 前言 <br>

這裡要來說明如何運用 GA 來求解 flow shop 的問題，以下將先對 flow shop 問題做個簡介，接著描述本範例的求解問題以及編碼原則說明，最後會根據每個程式區塊進行概念上的講解

### :arrow_down_small: 什麼是 flow shop 問題? <br>

簡單來說，flow shop 問題就是有 n 個工件以及 m 台機台，每個工件在機台的加工順序都一樣，如下圖所示，工件1先進入機台1加工，再到機台2加工，而工件2跟隨著工件1的腳步，按照同樣的機台順序加工，其他工件以此類推。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/1.png" width="450" height="180">
</div>
<br>

因此假設現在有3個工件2台機台，每個工件在每台機台的加工時間，如左下圖所示，工件的加工順序為先到機台A加工再到機台B，假設得到的排程結果為<br>
Job 1->Job 2->Job 3，因此可得到如右下圖的甘特圖

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/2.png" width="570" height="250">
</div>
<br>

## :black_nib: 問題描述 <br>
本範例是一個具有20個工件的單機台 flow shop 問題，排程目標為**最小化總加權延遲 (Total weighted tardiness)** ，工件資訊如下圖所示

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/3.png" width="650" height="180">
</div>
<br>

### :arrow_down_small: 排程目標 <br>
由於本範例的目標為最小化總加權延遲 (Total weighted tardiness)，因此除了必須知道每個工件在每台機台上的加工時間外，還必須知道每個工件的到期日及權重。<br>

:bulb: 總加權延遲時間的公式如下：<br>

<c<sub>i</sup></sub>：工件 i 的完工時間 (Completion time)、d<sub>i</sup></sub>：工件 i 的到期日 (Due date)、T<sub>i</sup></sub>：工件 i 的延遲時間 (Tardiness time)、<br>
w<sub>i</sup></sub>：工件 i 的權重(Weight) >
- 首先計算每個工件的延遲時間，如果提早做完，則延遲時間為0 <br>

**T<sub>i</sup></sub> = max {0,c<sub>i</sup></sub> - d<sub>i</sup></sub>}**

- 計算所有工件的加權延遲時間總和，從公式我們可以知道，當工件的權重越大，我們要盡可能的準時完成那些權重較大的工件，不然會導致總加權延遲時間太大，對於這樣的排程目標問題來說，這就不是一個好的排程

<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/4.png" width="80" height="60">

另外，這裡還有提供另一個版本的 flow shop 程式，跟本文主要的差別在於求解目標的不同，另一版本的目標為最小化總閒置時間 (Idle time)，也就是上面範例甘特圖中，灰色區域的部分，期望排出來的排程，可以盡可能減少總機台的閒置時間。


### :arrow_down_small: 編碼原則  <br>

這裡的編碼方式很簡單，每個染色體就表示一組排程結果，因此，如果 flow shop 的問題中，共有五個工件要排，則每個染色體就由五個基因所組成，每個基因即代表某個工件，在程式裡，會透過 list 來儲存每個染色體，如下面所示：<br>

chromosome 1 => [0,1,2,3,4] <br>
chromosome 2 => [1,2,0,3,4] <br>
chromosome 2 => [4,2,0,1,3] <br>
........<br>

## :black_nib: 程式說明 <br>

這裡主要針對程式中幾個重要區塊來說明，有些細節並無放入，如有需要請參考[完整程式碼](https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/GA_flowshop_tardyjob.py)或[範例檔案]((https://wurmen.github.io/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/implementation%20with%20python/GA-flowshop/Example.html))

### :arrow_down_small: 導入所需套件 <br>

```python
# importing required modules
import numpy as np
import time
import copy
```

### :arrow_down_small: 初始設定 <br>
此區主要包含讀檔或是資料給定，以及一些參數上的設定
```python
''' ================= initialization setting ======================'''
num_job=20 # number of jobs

p=[10,10,13,4,9,4,8,15,7,1,9,3,15,9,11,6,5,14,18,3]
d=[50,38,49,12,20,105,73,45,6,64,15,6,92,43,78,21,15,50,150,99]
w=[10,5,1,5,10,1,5,10,5,1,5,10,10,5,1,10,5,5,1,5]
# raw_input is used in python 2
population_size=int(input('Please input the size of population: ') or 30) # default value is 30
crossover_rate=float(input('Please input the size of Crossover Rate: ') or 0.8) # default value is 0.8
mutation_rate=float(input('Please input the size of Mutation Rate: ') or 0.1) # default value is 0.1
mutation_selection_rate=float(input('Please input the mutation selection rate: ') or 0.5)
num_mutation_jobs=round(num_job*mutation_selection_rate)
num_iteration=int(input('Please input number of iteration: ') or 2000) # default value is 2000


start_time = time.time()

```

### :arrow_down_small: 產生初始解 <br>
根據上述所設定的族群大小，透過隨機的方式，產生初始族群
```python
'''----- generate initial population -----'''
Tbest=999999999999999
best_list,best_obj=[],[]
population_list=[]
for i in range(population_size):
    random_num=list(np.random.permutation(num_job)) # generate a random permutation of 0 to num_job-1
    population_list.append(nxm_random_num) # add to the population_list2.

```

### :arrow_down_small: 交配 <br>

這裡的交配方式是透過指定位置的方式進行交配，執行的步驟如下：
1. 透過隨機選擇方式，將基因數一半的位置設為固定不變，以下圖為例，共有六個工件進行排序，生成兩個親代，在此選定2、5、6為工件順序不變的位置。
2. 將 Parent 1 工件不變的位置，複製產生 Child 2 ，接著 Child 2 與 Parent 2 進行比對。
3. 將 parent 2 與child2不重複的工件，依序填入 Child 2 剩餘的位置，形成新的子代。 Child 1 的形成方式如 Child 2 所示。
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/5.png" width="400" height="325">
</div>
<br>

```python
    '''-------- crossover --------'''
	parent_list=copy.deepcopy(population_list)
    offspring_list=copy.deepcopy(population_list)
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    
    for m in range(int(population_size/2)):
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob:
            parent_1= population_list[S[2*m]][:]
            parent_2= population_list[S[2*m+1]][:]
            child_1=['na' for i in range(num_job)]
            child_2=['na' for i in range(num_job)]
            fix_num=round(num_job/2)
            g_fix=list(np.random.choice(num_job, fix_num, replace=False))
            
            for g in range(fix_num):
                child_1[g_fix[g]]=parent_2[g_fix[g]]
                child_2[g_fix[g]]=parent_1[g_fix[g]]
            c1=[parent_1[i] for i in range(num_job) if parent_1[i] not in child_1]
            c2=[parent_2[i] for i in range(num_job) if parent_2[i] not in child_2]
            
            for i in range(num_job-fix_num):
                child_1[child_1.index('na')]=c1[i]
                child_2[child_2.index('na')]=c2[i]
            offspring_list[S[2*m]]=child_1[:]
            offspring_list[S[2*m+1]]=child_2[:]
```
### :arrow_down_small: 突變 <br>
此方法是透過基因位移的方式進行突變，突變方式如下:<br>
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
            m_chg=list(np.random.choice(num_job, num_mutation_jobs, replace=False)) # chooses the position to mutation
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1):
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position
```
### :arrow_down_small: 適應值計算 <br>
計算每個染色體也就是每個排程結果的總加權延遲，並將其記錄，以利後續選擇時能比較
```python
    '''--------fitness value(calculate tardiness)-------------'''
    total_chromosome=copy.deepcopy(parent_list)+copy.deepcopy(offspring_list) # parent and offspring chromosomes combination
    chrom_fitness,chrom_fit=[],[]
    total_fitness=0
    for i in range(population_size*2):
        ptime=0
        tardiness=0
        for j in range(num_job):
            ptime=ptime+p[total_chromosome[i][j]]
            tardiness=tardiness+w[total_chromosome[i][j]]*max(ptime-d[total_chromosome[i][j]],0)
        chrom_fitness.append(1/tardiness)
        chrom_fit.append(tardiness)
        total_fitness=total_fitness+chrom_fitness[i]
```

### :arrow_down_small: 選擇  <br>
這裡採用輪盤法 (Roulette wheel) 的選擇機制
```python
    '''----------selection----------'''
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
先比較每個染色體的總加權延遲 (chrom_fit) ，選出此輪找到的最好解 (Tbest_now) ，接著在跟目前為止找到的最好解 (Tbest) 進行比較，一旦這一輪的解比目前為止找到的解還要好，就替代 Tbest 並記錄該解所得到的排程結果
```python
    '''----------comparison----------'''
    for i in range(population_size*2):
        if chrom_fit[i]<Tbest_now:
            Tbest_now=chrom_fit[i]
			sequence_now=copy.deepcopy(total_chromosome[i])
    
    if Tbest_now<=Tbest:
        Tbest=Tbest_now
		sequence_best=copy.deepcopy(sequence_now)
    
    job_sequence_ptime=0
    num_tardy=0
    for k in range(num_job):
        job_sequence_ptime=job_sequence_ptime+p[sequence_best[k]]
        if job_sequence_ptime>d[sequence_best[k]]:
            num_tardy=num_tardy+1
```

### :arrow_down_small: 結果 <br>
等所有迭代次數結束後，會輸出在所有迭代中找到的最好排程結果 (sequence_best)、它的總加權延遲時間、每個工件平均加權延遲時間、有多少工件延遲以及程式執行時間
```python
'''----------result----------'''
print("optimal sequence",sequence_best)
print("optimal value:%f"%Tbest)
print("average tardiness:%f"%(Tbest/num_job))
print("number of tardy:%d"%num_tardy)
print('the elapsed time:%s'% (time.time() - start_time))
```

### :arrow_down_small: 甘特圖 <br>
```python
'''--------plot gantt chart-------'''
import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.offline as offline
import datetime

j_keys=[j for j in range(num_job)]
j_count={key:0 for key in j_keys}
m_count=0
j_record={}
for i in sequence_best:
   gen_t=int(p[i])
   j_count[i]=j_count[i]+gen_t
   m_count=m_count+gen_t
   
   if m_count<j_count[i]:
       m_count=j_count[i]
   elif m_count>j_count[i]:
       j_count[i]=m_count
   start_time=str(datetime.timedelta(seconds=j_count[i]-p[i])) # convert seconds to hours, minutes and seconds

   end_time=str(datetime.timedelta(seconds=j_count[i]))
   j_record[i]=[start_time,end_time]
       

df=[]
for j in j_keys:
   df.append(dict(Task='Machine', Start='2018-07-14 %s'%(str(j_record[j][0])), Finish='2018-07-14 %s'%(str(j_record[j][1])),Resource='Job %s'%(j+1)))

# colors={}
# for i in j_keys:
#     colors['Job %s'%(i+1)]='rgb(%s,%s,%s)'%(255/(i+1)+0*i,5+12*i,50+10*i)

fig = ff.create_gantt(df, colors=['#008B00','#FF8C00','#E3CF57','#0000CD','#7AC5CD','#ED9121','#76EE00','#6495ED','#008B8B','#A9A9A9','#A2CD5A','#9A32CD','#8FBC8F','#EEC900','#EEE685','#CDC1C5','#9AC0CD','#EEA2AD','#00FA9A','#CDB38B'], index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True)
py.iplot(fig, filename='GA_flow_shop_scheduling_tardyjob', world_readable=True)
```
## :black_nib: Reference <br>
- António Ferrolho and Manuel Crisóstomo. “Single Machine Total Weighted Tardiness Problem with Genetic Algorithms” 
- N. Liu, Mohamed A. Abdelrahman, and Snni Ramaswamy. “A Genetic Algorithm for the Single Machine Total Weighted Tardiness Problem”
