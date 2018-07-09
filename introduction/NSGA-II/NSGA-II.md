# Nondominated Sorting Genetic Algorithm II (NSGA-II) 
*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu/)*<br>
*2018/06/12*
<br>
## :black_nib: 前言 
上一篇文章介紹了什麼是基因演算法 (GA)，而本文介紹的非凌越排序基因演算法 (NSGA-II) 由 NSGA 改良而來，是 K.Deb, A.Pratap, S.Agarwal, T.Meyarivan 於 2002 年所提出，該演算法的架構與 GA 相似，但專門被用來求解具有多目標的問題，因此本篇文章將要介紹何謂 NSGA-II ，並在最後透過 PYTHON 來進行實作，求解具有雙目標的排程 Jop Shop 問題。
<br>

## :black_nib: "凌越 (dominated) "的概念是什麼? 
一般而言，在單目標問題中，我們可以很容易的判斷什麼是最佳解，哪些解叫好，哪些叫壞，但當我們遇到多目標問題時，解的品質就不是那麼容易判斷了，尤其是目標之間具有衝突時，因此，在多目標問題中會透過"凌越"的概念來判斷一個解的好壞。<br>

我們舉一個簡單的例子來說明此概念，假設現在有四個人想跟我做朋友，他們各自的薪水及身高如左下表所示，而我的交友條件有兩個目標-身高及薪水，也就是我希望所交到的朋友身高與薪水越高越好，因此這兩個目標皆為最大化問題。從表中可以發現， A 不管再身高或薪水都表現比其他人好，所以我們稱A凌越其他所有解，以數學符號表示為 A≻B、C、D ，而A在該問題中又可被稱為非凌越解 (non-dominated solution) ，另外， B 與 C 在身高及薪水上，各有其優勢，因此這兩個解互不凌越， D 不管再身高還是薪水都劣於其他人，所以 D 被所有人凌越，也就是 A≻D、B≻D，C≻D 。<br>

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/1.png" width="550" height="250">
</div>
<br>

由於上述問題為雙目標問題，因此將其畫成圖，可表示如右上圖的二維空間，當我們獲得的解越來越多時(在此問題中一個解表示一個人)，**一旦找到一組解，這組解彼此互不凌越，且不被任何解給凌越時，我們稱這組解為柏拉圖最佳解 (Pareto-optimal solution)** ，而由這組解所形成的前緣稱為柏拉圖最佳前緣 (Pareto-optimal front) ，也就是如圖中的藍色線。因此，在多目標問題中，**最關鍵的地方就是找出柏拉圖最佳前緣**，前緣上的解也就是我們想要的解，所以在多目標問題中，不像單目標問題有一個唯一最佳解，一般來說是會有多組解存在。

## :black_nib: NSGA-II 架構
NSGE-II 的架構如下圖所示，如同前言所提，它的架構與 GA 相似，唯一較大的不同在於紅色框的部分，因此接下來將會放較多的重心在說明紅色框內的四個部分，並在最後進行統整說明。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/2.png" width="550" height="350">
</div>
<br>

### :arrow_down_small: 菁英策略 (Elitism strategy) <br>

為了確保所留下來的染色體都是優秀的、可行的，在進行適應性評估前 (fitness evaluation) 採用了菁英策略，此策略簡單來說，就是將交配、突變前的親代與交配、突變後的子代一同保留下來，進行評選，以防止染色體會越選越糟的情形，避免損失掉找到的優質解。

### :arrow_down_small: 非凌越排序 (Nondominated sorting approach) <br>

相較於原本的 NSGA ， NSGA-II 提出了一個更快速的非凌越排序法，並擁有較少的時間複雜度，且不需要指定分享函數 (sharing function) ，以下將要介紹整個非凌越排序的主要概念，並沿用上面的例子來進行說明，在此我將它分為五個執行步驟。( NSGA 詳細內容可參考[原文](https://pdfs.semanticscholar.org/b39d/633524b0b2b46474d35b27c2016f3c3f764d.pdf)) <br>

:balloon: **Step 1. 計算每個解的兩個實體 (Calculating two entities for each solution) ：n<sub>p</sup></sub>、 S<sub>p</sup></sub>** <br>

 p 為被計算解的代稱，n<sub>p</sup></sub> 表示凌越解 p 的個數(可想像成解 p 被多少解霸凌)，S<sub>p</sup></sub> 則為被解 p 凌越的解集合(也就是有誰被解 p 霸凌)，以上面的例子為例，可得到左下表：

從右圖中可以很清楚的看到，解 A 凌越了所有解，因此 S<sub>A</sup></sub>={B、C、D} ，而 n<sub>A</sup></sub>=0 ； B 僅被 A 給凌越，且凌越了解 D ，所以 n<sub>B</sup></sub>=1 、 S<sub>B</sup></sub>={D} ，其它以此類推......
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/3.png" width="600" height="300">
</div>

:balloon: **Step 2. 找出第一組非凌越前緣的成員 (Finding the members of the first nondominated front) ：n<sub>p</sup></sub>= 0** <br>

經由上個步驟我們可以得到每個解與其它解的凌越關係表，接著我們要將這些解進行分級，以利作為最終選擇染色體(解)的指標，其概念如下圖所示，我們會透過凌越關係表，將這些解分成不同的 level ，第一層的非凌越解具有最高層級(也就是柏拉圖前緣解)，而第二層具有次高層級，以此類推，層級越高具有越高的優先權被選擇成為新的人口 (population)

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/4.png" width="325" height="250">
</div>

因此，一開始要先找出第一層優先解，也就是在上一步驟形成的表中 n<sub>p</sup></sub>= 0 的解，在此例中即為解A和位於藍色線上的解，並給予這些解的排序等級為1。

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/5.png" width="300" height="175">
</div>
<br>

:balloon: **Step 3. 對於每個 n<sub>p</sup></sub>= 0 的解，去探訪這些解 S<sub>p</sup></sub> 集合內的每個解 (q) ，並將集合內解的凌越數 n<sub>p</sup></sub> 減一<br> (For each solution with n<sub>p</sup></sub>= 0, we visit each member (q) of its set S<sub>p</sup></sub> and reduce its domination count by one.)**<br>

:balloon: **Step 4. 在上一步訪問每個解的過程中，若有任何解 n<sub>p</sup></sub> 變成0，則該解即屬於第二非凌越前緣，因此賦予它排序等級為2**<br>
**(If for any member the domination count becomes zero, it belongs to the second nondominated front.)**<br>

從Step 2中我們知道 n<sub>p</sup></sub>= 0 的解只有 A，而被 A 凌越的解有 B、C、D (從 S<sub>p</sup></sub> 得知)，因此我們一一的去造訪這些解，並將其 n<sub>p</sup></sub> 減一，可得到更新的表如下，並在造訪的過程中發現，解 B 及解 C 的 n<sub>p</sup></sub> 皆變為0，所以它們為第二非凌越前緣的解，故賦予它們排序等級為2，亦即第二優先被挑選成 population 的解

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/6.png" width="300" height="175">
</div>
<br>

:balloon: **Step 5.重複執行以上步驟，直到所有前緣都被辨識出來為止**<br>
**(The above procedures are continued until all fronts are identified.)**<br>

:bulb: Pseudo code

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/7.png" width="450" height="500">
</div>

### :arrow_down_small: 擁擠距離 (Crowding-distance)

為了保持解的多樣性，以及當不同解位於同樣的非凌越層級時能做出選擇，這裡提出了擁擠距離的方法，來評估群體中每個解與其周圍解的密度關係，其概念如下圖所示，再算一個特定解的擁擠距離時，我們會循著該解位於的非凌越前緣上，在此前緣中沿著每個目標找出距離該特定解左右最近的兩個相鄰解，去計算這兩個解的平均距離，最後將每個目標算出來的距離進行加總，即得到該特定解的擁擠距離。以下圖的雙目標例子來說，第i個解在其前緣的擁擠距離，即是距離解i最近的兩個解所圍出來的長方形的平均邊長。

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/8.png" width="500" height="350">
</div>

如同上一段所提，計算擁擠距離有助於保持解的多樣性，該意思是指，當要從一群位於相同非凌越前緣的解，進行解的挑選時，**會傾向選擇擁擠距離較大的解**，因為擁擠距離越大，表示該解與其他解的差異性較大，這有助於後面演算法迭代的過程中，可以避免落入局部解的情形，而達到探索 (exploration) 的效果，以期望找到更多更好的解，而擁擠距離詳細的計算方式如下:<br>

:balloon: **Step 1.將每個目標的解由小到大遞增排序，並透過下列公式算出每個解  i 在每個目標的評估距離 distance<sub>o</sup></sub>(i)**<br>

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/9.png" width="360" height="130">
</div>

o 表示目標、 F<sub>o</sup></sub>(i) 為目標 O 排序後的第 i 個解、 F<sub>o,max</sup></sub> 為最大邊界解、 F<sub>o,min</sup></sub> 為最小邊界解 <br>

##### :zap:上述公式有進行正規化的動作，以避免不同目標解間的數值規模差異太大，因此將各目標轉換至相同尺度，以利後續進行比較 <br>
<br>

:balloon: **Step 2.將每個解在每個目標所算出來的評估距離 (distance<sub>o</sup></sub>(i)) 進行加總，即可得到每個解的總擁擠距離 CD(i)** <br>

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/10.png" width="200" height="130">
</div>

:bulb: Pseudo code

<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/11.png" width="560" height="380">
</div>

### :arrow_down_small: 選擇機制 (Selection mechanism)

經由上述的過程，最終 population 內的每條染色體(解)，皆擁有兩個屬性:
- 非凌越層級 (nondomination rank)
- 擁擠距離 (crowding distance)

最後再挑選新的 population 成員時，則會依照下列規則進行挑選:
1. 先比較每個解的非凌越層級，**有越高層級的解(數字較小)，具有越高的被優先選擇權**
2. 若兩個解的非凌越層級相同，則比較擁擠距離，**擁擠距離越大有越高的被優先選擇權**

## :black_nib: 總結
最後透過下面的 gif 圖，統整 NSGA-II 的整個流程，對於每一次迭代皆會進行下面的動作，直到所設定的條件到達為止:

1. 首先有一初始的人口(親代) P<sub>t</sup></sub> 內含 N 個染色體，經由突變及交配後產生子代 Q<sub>t</sup></sub> 。
2. 由於採用菁英策略，因此將親代與子代一同保留下來，進行挑選。
3. 接著進行非凌越排序，以得到每個解的非凌越層級 (F<sub>1</sup></sub><層級1>、F<sub>2</sup></sub><層級2>.....)。
4. 最後挑選新的 N 個染色體當成下一次迭代的人口，先依照非凌越層級高低來選擇，若發生如下圖所示的，剩餘要挑選進入新人口的染色體數小於下一個要被選擇的非凌越層級內的染色體的數，則透過擁擠距離來進行挑選，選擇擁擠距離較大者進入新的人口。
5. 最終產生新的人口 P<sub>t+1</sup></sub> ，進入下一次迭代，重複上述流程。

![](https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/NSGA-II/Picture/123.gif)

### :black_nib: Reference 
- [K.Deb, A.Pratap, S.Agarwal, T.Meyarivan, A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II,IEEE Trans. Evol. Comput.6(2)(2002)182](https://ieeexplore.ieee.org/document/996017/) <br>
- [Wu, Min-You, Multi-Objective Stochastic Scheduling Optimization: A Study of Auto Parts Manufacturer in Taiwan](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=dnclcdr&s=id=%22104NCKU5621001%22.&searchmode=basic)
