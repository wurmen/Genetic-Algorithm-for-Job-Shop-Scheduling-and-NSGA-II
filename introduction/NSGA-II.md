# Nondominated Sorting Genetic Algorithm II (NSGA-II) (cont.)


上一篇文章介紹了什麼是基因演算法(GA)，而本文介紹的非凌越排序基因演算法(NSGA-II)由NSGA改良而來，是K.Deb,A.Pratap, S.Agarwal,T.Meyarivan等人於2002年所提出，該演算法的架構與GA相似，但專門被用來求解具有多目標的問題，因此本篇文章將要介紹何謂NSGA-II，並在最後透過PYTHON來進行實作，求解具有雙目標的排程Jop Shop問題。

### :black_nib: "凌越(dominated)"的概念是什麼? 
一般而言，在單目標問題中，我們可以很容易的判斷什麼是好的解、什麼是不好的解，但當我們遇到多目標問題時，解的品質就不是那麼容易判斷了，尤其是解跟解之間具有衝突時，因此，在多目標問題中會透過"凌越"的概念來判斷一個解的好壞。<br>
現在我們先
假設某個問題具有兩個目標，此兩個目標都是最小化問題，也就是解越小越好，從下面左邊的圖我們可以發現




### :black_nib: Reference 
[A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II ](https://ieeexplore.ieee.org/document/996017/)
