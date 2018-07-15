# Solving Job shop scheduling problem with genetic algorithm

*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/07/14*
<br>

## :black_nib: 前言 <br>

這裡要來說明如何運用 GA 來求解 Job shop 的問題，以下將先對 Job shop 問題做個簡介，接著描述本範例的求解問題以及編碼與解碼說明，最後會根據每個程式區塊進行概念上的講解

### :arrow_down_small: 什麼是 Job shop 問題? <br>

Jop shop 問題與 Flow shop 問題最大的不同在於，不像 Flow shop 問題中，每個工件在機台的加工順序都是相同的，在 Job shop 問題裡，每個工件都有屬於自己的機台加工順序，如下圖所示：


## :black_nib: 問題描述 <br>
本範例是一個 10x10 的 Jop shop 問題，共有10個工件與10台機台，每個工件在每台機台的加工順序都不同，排程目標為最小化總完工時間 (Makespan) ，資料是以工件的加工作業順序來呈現，每個工件都會經過10個加工作業，下表紀錄著每個工件在每一個加工作業的加工機台以及加工所需時間

### :arrow_down_small: 排程目標 <br>
本範例的目標為最小化總完工時間 (Makespan)，也就是說要最小化整個排程的執行時間，以前面的例子為例，該範例的完工時間是 Job 3 在機台1的完工時間點，因為對於此排程結果來說，Job 3 是所有工件中，最後一個完成的，因此此排程的完工時間，就是Job 3 完成的時間點



### :arrow_down_small: 編碼原則  <br>


## :black_nib: 程式說明 <br>

這裡主要針對程式中幾個重要區塊來說明，有些細節並無放入，如有需要請參考[完整程式碼]或[範例檔案]

### :arrow_down_small: 導入所需套件 <br>

```python

```

### :arrow_down_small: 初始設定 <br>
此區主要包含讀檔或是資料給定，以及一些參數上的設定
```python


```

### :arrow_down_small: 產生初始解 <br>
根據上述所設定的族群大小，透過隨機的方式，產生初始族群
```python



```

### :arrow_down_small: 交配 <br>



```python

```
### :arrow_down_small: 突變 <br>

```python

```
### :arrow_down_small: 適應值計算 <br>

```python

```

### :arrow_down_small: 選擇  <br>

```python

```

### :arrow_down_small: 比較 <br>
將每一輪找到的最好的解 (Tbest_now) 跟目前找到的解 (Tbest) 進行比較，一旦這一輪的解比目前為止找到的解還要好，就替代 Tbest 並記錄該解所得到的排程結果
```python
 
```

### :arrow_down_small: 結果 <br>

```python

```

### :arrow_down_small: 甘特圖 <br>
```python

```
## :black_nib: Reference <br>
- [Wu, Min-You, Multi-Objective Stochastic Scheduling Optimization: A Study of Auto Parts Manufacturer in Taiwan](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclcdr&s=id=%22104NCKU5621001%22.&searchmode=basic)
- [Chin-Yi Tseng, Intelligent Manufacturing Systems](https://github.com/PO-LAB/Intelligent-Manufacturing-Systems)
- [
M. Gen, Y. Tsujimura, E. Kubota, Solving job-shop scheduling problem using genetic algorithms, Proc. of the 16th Int. Conf. on Computer and Industrial Engineering, Ashikaga, Japan (1994), pp. 576-579](https://ieeexplore.ieee.org/document/400072/)
- Dr. Chia-Yen Lee (2017), Meta-Heuristic Algorithms-Genetic Algorithms & Particle Swarm Optimization, Intelligent Manufacturing Systems course
