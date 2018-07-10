# Genetic Algorithm (GA)
*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/feed/?trk=nav_back_to_linkedin)*<br>

<br>

## :black_nib: GA 背景 (Background)
基因演算法(GA)的架構一開始是由John Holland教授於1975年所提出，該演算法的主要靈感來自於生物圈中的演化機制，在大自然中，生物的繁衍及遺傳是透過染色體的交配與變異，以改變不同基因的組成，來產生下一代，染色體主要是由DNA及蛋白質所組成，一段DNA片段代表著控制某一性狀的基因，因此染色體也表示是由許多基因所組成。<br>

簡單來說，基因演算法即是透過這種概念所發展，將求解問題的一個解或參數用一個染色體來表示，藉由編碼將染色體轉成字串或數值等形式，而每個數值或字串代表染色體內的基因，表示解的某個部分，接著透過突變及交配的方式，來產生下一代，也就是不同的解，最後以適者生存，不適者淘汰的觀念，將好的解進行保留，以進行下一輪的交配突變，來產生更好的解，期望未來能購跳脫局部解找到全域最佳解。<br>

基因演算法能用來求解大部分的最佳化問題，而本主題主要著重在 GA 與排程 (Scheduling)問題的結合與應用，因此以下將針對GA進行概念上的介紹，並於實作單元中說明GA如何運用於排程問題上。

## :black_nib: GA 流程 (Procedure)
下圖為GA的流程圖 (flow chart)，接著將會對每個步驟進行說明
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/1.png" width="250" height="500">
</div>
<br>

### :arrow_down_small: 編碼 (Encoding) <br>
在GA中通常一個染色體(Chromosome)代表求解問題的一個可行解，而染色體是由基因所組成，所以基因即表示解的一部份。因此在演算法開始前，必須先依照問題的屬性來進行染色體的設計，染色體編碼的形式有很多種，最常見的編碼方式為二進位編碼，也就是將數值轉換成1與0的排列字串，我們以[維基百科](https://zh.wikipedia.org/wiki/%E6%9F%93%E8%89%B2%E9%AB%94_(%E9%81%BA%E5%82%B3%E6%BC%94%E7%AE%97%E6%B3%95))內舉的例子進行說明：<br>

假設現在有一個問題是要找出介於0 ~ 255間的一個整數 x ，這個整數 x 要使得函數 f(x)=x<sup>2</sup></sub> 的值最大 (當然這是個非常簡單的問題，但這裡為了作個簡單的說明，所以不要太在意XD)。 <br>

由於0 ~ 255間的整數皆有可能為解答，為了表示這區間內的所有整數，在這可使用8位元的2進位串來表示一個解，如下圖所示，在 GA 中每一個染色體都由8個基因所組成。<br>

:bulb: 為什麼是使用8個位元?
0 ~ 255共有256個數字，因此以二進位編碼來說，8個基因剛好可表示2<sup>8</sup></sub>=256個數<br>

另外，藉由此範例順便說明解碼 (Decoding) 的意義，因為 GA 中我們是透過編碼後的染色體來代表一個解，所以當要由染色體來推得原本的解時，就必須經過解碼的步驟，就如圖所示的，將染色體轉換回它所代表的實際數值，傳換的方式就取決於當初是怎麼設計這個染色體的。<br>


<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/2.png" width="550" height="475">
</div>
<br>

當然編碼的方式還有很多種，除了二進位的編碼方式，也可以是含有字母的形式等等，又或者像在本主題實例應用的排程中，是以一個工作序列作為染色體的表示，因此在GA裡，染色體的編碼也是很重要的一環，染色體的設計的好壞，可能會影響編碼、解碼的難易度或整個GA的執行效率。

#### :unlock: 編碼中所需注意或設定的參數
- 編碼方式 (Encoding method)
- 染色體的長度 (Chromosome length)

-------------------------------------------

### :arrow_down_small: 初始族群 (Inital population) <br>

當完成染色體的設計後，將正式進入GA演算法的主體，一開始我們必須先產生一群染色體來當作初始族群，也就是所謂的初始解，如下圖所示，它們也可被稱為GA內的初始親代 (Parents)，有點像是某生物體的第一代祖先一樣，接著再透過下面步驟的交配、突變來產生子代 (Offspring)，以繁衍更多更優秀的子孫，因此在此步驟必須先決定族群大小。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/3.png" width="450" height="355">
</div>
<br>

#### :unlock: 初始族群中所需注意或設定的參數
- 族群大小 (Population size)

--------------------------------------------

### :arrow_down_small: 交配 (Crossover) <br>

### :arrow_down_small: 突變 (Mutation) <br>

## :black_nib: Reference
- Holland, J. H. (1975). Adaptation in natural and artificial systems. Ann Arbor, MI: University of Michigan Press.
- Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization and Machine Learning. Addison-Wesley Longman Publishing Co., Inc. Boston, MA.
