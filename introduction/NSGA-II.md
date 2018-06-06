# Nondominated Sorting Genetic Algorithm II (NSGA-II) (cont.)

### :black_nib: 前言 
上一篇文章介紹了什麼是基因演算法(GA)，而本文介紹的非凌越排序基因演算法(NSGA-II)由NSGA改良而來，是K.Deb,A.Pratap, S.Agarwal,T.Meyarivan等人於2002年所提出，該演算法的架構與GA相似，但專門被用來求解具有多目標的問題，因此本篇文章將要介紹何謂NSGA-II，並在最後透過PYTHON來進行實作，求解具有雙目標的排程Jop Shop問題。

### :black_nib: "凌越(dominated)"的概念是什麼? 
一般而言，在單目標問題中，我們可以很容易的判斷什麼是最佳解，哪些解叫好，哪些叫壞，但當我們遇到多目標問題時，解的品質就不是那麼容易判斷了，尤其是目標之間具有衝突時，因此，在多目標問題中會透過"凌越"的概念來判斷一個解的好壞。<br>

我們舉一個簡單的例子來說明此概念，假設現在有四個人想跟我做朋友，他們各自的薪水及身高如左下表所示，而我的交友條件有兩個目標-身高及薪水，也就是我希望所交到的朋友身高與薪水越高越好，因此這兩個目標皆為最大化問題。從表中可以發現，A不管再身高或薪水都表現比其他人好，所以我們稱A凌越其他所有解，以數學符號表示為 A≻B、C、D，而A在該問題中又可被稱為非凌越解(non-dominated solution)，另外，B與C在身高及薪水上，各有其優勢，因此這兩個解互不凌越，D不管再身高還是薪水都劣於其他人，所以D被所有人凌越，也就是A≻D、B≻D，C≻D。<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/Picture/1.png" width="550" height="250">
</div>

由於上述問題為雙目標問題，因此將其畫成圖，可表示如右上圖的二維空間，當我們獲得的解越來越多時(在此問題中一個解表示一個人)，**一旦找到一組解，這組解彼此互不凌越，且不被任何解給凌越時，我們稱這組解為柏拉圖最佳解(Pareto-optimal solution)** ，而由這組解所形成的前緣稱為柏拉圖最佳前緣(Pareto-optimal front)，也就是如圖中的藍色線。因此，在多目標問題中，**最關鍵的地方就是找出柏拉圖最佳前緣**，前緣上的解也就是我們想要的解，所以在多目標問題中，不像單目標問題有一個唯一最佳解，一般來說是會有多組解存在。

### :black_nib: NSGA-II架構
NSGE-II的架構如下圖所示，如同前言所提，它的架構與GA相似，唯一較大的不同在於紅色框的部分，因此接下來將會放較多的重心在於說明紅色框內的四個部分，並在最後進行統整說明。
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/Picture/2.png" width="550" height="350">
</div>


### :black_nib: Reference 
[A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II ](https://ieeexplore.ieee.org/document/996017/)
