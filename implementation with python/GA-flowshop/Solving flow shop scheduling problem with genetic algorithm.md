# Solving flow shop scheduling problem with genetic algorithm

*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/07*
<br>

## :black_nib: 問題描述 <br>

這裡要來說明如何運用 GA 來求解 flow shop的問題，以下將先對 flow shop 問題做個簡介，說明一下編碼原則，接著根據每個程式區塊進行說明

### :arrow_down_small: 什麼是 flow shop 問題? <br>

簡單來說，flow shop 問題就是有 n 個工件以及 m 台機台，每個工件在機台的加工順序都一樣，如下圖所示，工件1先進入機台1加工，再到機台2加工，而工件2跟隨著工件1的腳步，按照同樣的機台順序加工，其他工件以此類推。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/1.png" width="450" height="200">
</div>
<br>

因此假設現在有3個工件2台機台，每個工件在每台機台的加工時間，如左下圖所示，工件的加工順序為先到機台A加工再到機台B，假設得到的排程結果為<br>
Job 1->Job 2->Job 3，因此可得到如右下圖的甘特圖

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/2.png" width="550" height="280">
</div>
<br>

### :arrow_down_small: 本範例 flow shop 的排程目標 <br>

在本文章中所示範的 flow shop 問題，**目標為最小化總加權延遲 (Total weighted tardiness)**，因此除了必須知道每個工件在每台機台上的加工時間外，還必須知道每個工件的到期日及權重。<br>

總加權延遲時間的公式如下：<br>

<c<sub>i</sup></sub>：工件 i 的完工時間(Completion time)、d<sub>i</sup></sub>：工件 i 的到期日(Due date)、T<sub>i</sup></sub>：工件 i 的延遲時間(Tardiness time)、<br>
w<sub>i</sup></sub>：工件 i 的權重(Weight) >
- 首先計算每個工件的延遲時間，如果提早做完，則延遲時間為0 <br>

**T<sub>i</sup></sub> = max {0,c<sub>i</sup></sub> - d<sub>i</sup></sub>}**

- 計算所有工件的加權延遲時間總和，從公式我們可以知道，當工件的權重越大，我們要盡可能的準時完成那些權重較大的工件，不然會導致總加權延遲時間太大，對於這樣的排程目標問題來說，這就不是一個好的排程

<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/implementation%20with%20python/GA-flowshop/picture/3.png" width="80" height="60">

另外，這裡還有提供另一個版本的 flow shop 程式，跟本文主要的差別在於求解目標的不同，另一版本的目標為最小化總閒置時間 (Idle time)，也就是上面範例甘特圖中，灰色區域的部分，期望排出來的排程，可以盡可能減少總機台的閒置時間。
