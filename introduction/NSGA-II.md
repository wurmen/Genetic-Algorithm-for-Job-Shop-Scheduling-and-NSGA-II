# Nondominated Sorting Genetic Algorithm II (NSGA-II) (cont.)

## :black_nib: 前言 
上一篇文章介紹了什麼是基因演算法(GA)，而本文介紹的非凌越排序基因演算法(NSGA-II)由NSGA改良而來，是K.Deb,A.Pratap, S.Agarwal,T.Meyarivan等人於2002年所提出，該演算法的架構與GA相似，但專門被用來求解具有多目標的問題，因此本篇文章將要介紹何謂NSGA-II，並在最後透過PYTHON來進行實作，求解具有雙目標的排程Jop Shop問題。

## :black_nib: "凌越(dominated)"的概念是什麼? 
一般而言，在單目標問題中，我們可以很容易的判斷什麼是最佳解，哪些解叫好，哪些叫壞，但當我們遇到多目標問題時，解的品質就不是那麼容易判斷了，尤其是目標之間具有衝突時，因此，在多目標問題中會透過"凌越"的概念來判斷一個解的好壞。<br>

我們舉一個簡單的例子來說明此概念，假設現在有四個人想跟我做朋友，他們各自的薪水及身高如左下表所示，而我的交友條件有兩個目標-身高及薪水，也就是我希望所交到的朋友身高與薪水越高越好，因此這兩個目標皆為最大化問題。從表中可以發現，A不管再身高或薪水都表現比其他人好，所以我們稱A凌越其他所有解，以數學符號表示為 A≻B、C、D，而A在該問題中又可被稱為非凌越解(non-dominated solution)，另外，B與C在身高及薪水上，各有其優勢，因此這兩個解互不凌越，D不管再身高還是薪水都劣於其他人，所以D被所有人凌越，也就是A≻D、B≻D，C≻D。<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/Picture/1.png" width="550" height="250">
</div>

由於上述問題為雙目標問題，因此將其畫成圖，可表示如右上圖的二維空間，當我們獲得的解越來越多時(在此問題中一個解表示一個人)，**一旦找到一組解，這組解彼此互不凌越，且不被任何解給凌越時，我們稱這組解為柏拉圖最佳解(Pareto-optimal solution)** ，而由這組解所形成的前緣稱為柏拉圖最佳前緣(Pareto-optimal front)，也就是如圖中的藍色線。因此，在多目標問題中，**最關鍵的地方就是找出柏拉圖最佳前緣**，前緣上的解也就是我們想要的解，所以在多目標問題中，不像單目標問題有一個唯一最佳解，一般來說是會有多組解存在。

## :black_nib: NSGA-II架構
NSGE-II的架構如下圖所示，如同前言所提，它的架構與GA相似，唯一較大的不同在於紅色框的部分，因此接下來將會放較多的重心在說明紅色框內的四個部分，並在最後進行統整說明。
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/Picture/2.png" width="550" height="350">
</div>

### :arrow_down_small: 菁英策略 (Elitism strategy) <br>
為了確保所留下來的染色體都是優秀的、可行的，在進行適應性評估前(fitness evaluation)採用了菁英策略，此策略簡單來說，就是將交配、突變前的親代與交配、突變後的子代一同保留下來，進行評選，以防止染色體會越選越糟的情形，避免損失掉找到的優質解。

### :arrow_down_small: 非凌越排序 (Nondominated sorting approach) <br>
相較於原本的NSGA，NSGA-II提出了一個更快速的非凌越排序法，並擁有較少的時間複雜度，且不需要指定分享函數(sharing function)，在此主要有五個步驟要被執行。(NSGA詳細內容可參考[原文](https://pdfs.semanticscholar.org/b39d/633524b0b2b46474d35b27c2016f3c3f764d.pdf))

#### Step 1. 計算每個解的兩個實體(Calculating two entities for each solution)：n<sub>p</sup></sub>、 S<sub>p</sup></sub> 
p為被計算解的代稱，n<sub>p</sup></sub>表示凌越解p的個數(可想像成解p被多少解霸凌)，S<sub>p</sup></sub>則為被解p凌越的解集合(也就是有誰被解p霸凌)，以上面的例子為例，可得到左下表：<br>

從右圖中可以很清楚的看到，解A凌越了所有解，因此S<sub>A</sup></sub>={B、C、D}，而n<sub>A</sup></sub>=0；B僅被A給凌越，且凌越了解D，所以n<sub>B</sup></sub>=1、S<sub>B</sup></sub>={D}，其它以此類推......
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/Picture/3.png" width="550" height="250">
</div>

#### Step 2. 找出第一組非凌越前緣的解(Finding the members of the first nondominated front)：n<sub>p</sup></sub>= 0
經由上個步驟我們可以得到每個解與其它解的凌越關係表，接著我們要將這些解進行分級，以利作為最終選擇染色體(解)的指標，其概念如下圖所示，我們會透過凌越關係表，將這些解分成不同的level，第一層的非凌越解具有最高層級(也就是柏拉圖前緣解)，而第二層具有次高層級，以此類推，層級越高具有越高的優先權被選擇成為新的人口(population)

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/Picture/4.png" width="350" height="250">
</div>

因此，一開始要先找出第一層解，也就是在上一步驟形成的表中n<sub>p</sup></sub>= 0的解，在此例中也就是解A及位於藍色線上的解，並給予這些解的排序等級為1。
#### Step 3. 

### :black_nib: Reference 
[A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II ](https://ieeexplore.ieee.org/document/996017/) <br>
[Multi-Objective Stochastic Scheduling Optimization: A Study of Auto Parts Manufacturer in Taiwan](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclcdr&s=id=%22104NCKU5621001%22.&searchmode=basic)
