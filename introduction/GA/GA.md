# Genetic Algorithm (GA)
*[POLab](http://polab.imis.ncku.edu.tw/)* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/12/01*
<br>

## :black_nib: GA 背景 (Background)
基因演算法 (GA) 的架構一開始是**由 John Holland 教授於1975年**所提出，該演算法的**主要靈感來自於生物圈中的演化機制**，在大自然中，**生物的繁衍及遺傳是透過染色體的交配與變異，以改變不同基因的組成**，來產生下一代，染色體主要是由 DNA 及蛋白質所組成，一段 DNA 片段代表著控制某一性狀的基因，因此染色體也表示是由許多基因所組成。<br>

簡單來說，基因演算法即是透過這種概念所發展，將求解問題的一個潛在解或參數用一個染色體來表示，藉由編碼將染色體轉成字串或數值等形式，而每個數值或字串代表染色體內的基因，表示解的某個部分，接著透過突變及交配的方式，來產生下一代，也就是不同的潛在解，最後以適者生存，不適者淘汰的觀念，將好的解進行保留，以進行下一輪的交配突變，來產生更好的解，直到所設定的停止條件到達為止，期望未來能夠跳脫局部解找到全域最佳解。<br>

基因演算法能用來求解大部分的最佳化問題，而本主題主要著重在 GA 與排程 (Scheduling) 問題的結合與應用，因此以下將針對 GA 進行概念上的介紹，並於實作單元中說明GA如何運用於排程問題上。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/12.png" width="425" height="300">
</div>
<br>

<p align="center">圖文擷取自：南一課本</p>

## :black_nib: GA 流程 (Procedure)
下圖為GA的流程圖 (flow chart)，接著將會對每個步驟進行說明

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/14.png" width="600" height="500">
</div>
<br>

### :arrow_down_small: 編碼 (Encoding) <br>

在 GA 整個執行的過程中，會在所謂的 **編碼空間 (Coding space)** 與 **解空間 (Solution space)** 內交替運行，而在編碼空間裡主要在執行基因操作，像突變和交配的動作，在解空間中，則執行評估及選擇，如下圖所示：

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/11.png" width="700" height="300">
</div>
<br>

在編碼空間中，會**以編碼的形式來代表一個解**，就如背景介紹所提，**在 GA 通常一個染色體 (Chromosome) 代表求解問題的一個潛在解 (Potential solution)** ，而染色體是由基因所組成，所以基因即表示解的一部份。因此在演算法開始前，必須先依照問題的屬性來進行染色體的設計。<br>
<br>
染色體編碼的方式有很多種，最常見的編碼方式為二元編碼 (Binary encoding)，也就是將解轉換成用1與0的排列字串表示，這樣的方式也最常使用在當你的解為數值形式時，如下圖所示：<br>

:bulb: 在排程中，通常以工件加工序列來當作一個染色體<br>

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/13.png" width="450" height="150">
</div>
<br>

我們以[維基百科](https://zh.wikipedia.org/wiki/%E6%9F%93%E8%89%B2%E9%AB%94_(%E9%81%BA%E5%82%B3%E6%BC%94%E7%AE%97%E6%B3%95))內舉的例子進行簡單的編碼說明：<br>

**Example**<br>
假設現在有一個問題是要找出介於0 ~ 255間的一個整數 x ，這個整數 x 要使得函數 f(x)=x<sup>2</sup></sub> 的值最大 (當然這是個非常簡單的問題，但這裡為了作個簡單的說明，所以不要太在意XD)。 <br>

由於0 ~ 255間的整數皆有可能為解答，為了表示這區間內的所有整數，在這可使用8位元的2進位串來表示一個解，如下圖所示，在 GA 中每一個染色體都由8個基因所組成。<br>

:bulb: 為什麼是使用8個位元 ?
 0 ~ 255共有256個數字，因此以二進位編碼來說，8個基因剛好可表示2<sup>8</sup></sub>=256個數<br>

:bulb: 另外，藉由此範例順便說明解碼 (Decoding) 的意義，因為 GA 中我們是透過編碼後的染色體來代表一個解，因此當要進行評估及選擇時，則必須將染色體推回原本的解，就必須經過解碼的步驟，就如圖所示的，將染色體轉換回它所代表的實際數值，轉換的方式取決於當初是怎麼設計這個染色體的。<br>


<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/2.png" width="550" height="475">
</div>
<br>

當然編碼的方式還有很多種，除了二元的編碼方式，也可以是直接以實數表示或含有字母的形式等等，又或者像在本主題實例應用的排程中，是以一個工件的加工序列作為染色體的表示，因此在GA裡，染色體的編碼也是很重要的一環，染色體設計的好壞，可能會影響編碼、解碼的難易度或整個GA的執行效率。<br>

:bulb: 以下列出幾個在編碼時所需決定的幾個問題：
1. 要使用什麼符號來編碼? 二元、實數...
2. 編碼架構為何? 一維、二維...
3. 染色體的長度? 固定長度、變動長度...
4. 要將什麼樣的內容納入編碼中? 只有解，還是解加參數都要一併編碼

#### :unlock: 本步驟所需注意或設定的參數
- 編碼方式 (Encoding method)
- 染色體的長度 (Chromosome length)

-------------------------------------------

### :arrow_down_small: 初始族群 (Initial population) <br>

當完成染色體的設計後，將正式進入GA演算法的主體，一開始我們必須先產生一群染色體來當作初始族群，也就是所謂的初始解，如下圖所示，它們也可被稱為GA內的初始親代 (Parents)，有點像是某生物體的第一代祖先一樣，接著再透過下面步驟的交配、突變來產生子代 (Offspring)，以繁衍更多更優秀的子孫，因此在此步驟必須先決定族群大小。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/3.png" width="400" height="285">
</div>
<br>

#### :unlock: 本步驟所需注意或設定的參數
- 族群大小 (Population size)

--------------------------------------------
在GA中會透過所謂的**基因操作 (Genetic operations) - 交配及突變**，來產生子代，也就是產生新的潛在解 (當然也是有可能產生重複的解)，並且期望可以達到探索 (exploration) 的效果，增加解的多樣性，希望能跳脫局部解，進而找到更多更優秀的解。

### :arrow_down_small: 交配 (Crossover) <br>

通常在進行交配時，會先根據所設定的交配率 (Crossover rate) 來決定任意兩條染色體是否要做交配的動作，將兩個染色體的部分基因進行交換重組，以產生新的染色體。<br>
交配的方式也是有很多種，下面將說明三種常見的交配方法 (在排程實例說明中，將會示範其他不一樣的交配方式。)<br>

(以下皆以二元編碼的染色體進行示範)<br>

**1. 單點交配 (Single point crossover)** <br>

隨意選取某個基因位置當成交配點，並以此基因位置將親代染色體切成兩段，接著將某段固定，另一段互相交換，產生兩個新的子代。
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/4.png" width="450" height="355">
</div>
<br>

**2. 多點交配 (Multi-point crossover)** <br>

多點交配的概念與單點交配相似，只是變成一次選取多個基因位置當成交配點，接著依照個人設定，固定某幾段，其餘的進行交換，以產生新的子代。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/5.png" width="450" height="355">
</div>
<br>

**3. 均勻交配 (Uniform crossover)**<br>

均勻交配則是先隨機產生一條與親代染色體等長的二元編碼，稱為 Crossover Mask，當 Mask 內的值呈現1時，則親代染色體與 Mask 相對應的基因就必須彼此互相交換，其餘則不須交換，用此方式來產生新的子代。

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/6.png" width="460" height="325">
</div>
<br>

#### :unlock: 本步驟所需注意或設定的參數
- 交配方式 (Crossover method)
- 交配率 (Crossover rate)


### :arrow_down_small: 突變 (Mutation) <br>

為了增加解的多樣性，避免陷入局部解，對於每個染色體，會根據所設定的突變率，來決定某個染色體是否要進行突變，透過隨機的方式來改變單一染色體內的基因，一個常見的方式，即為針對單一染色體，隨機挑選染色體中的若干個基因進行互換，如下圖所示：
<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/7.png" width="445" height="225">
</div>
<br> 

#### :unlock: 本步驟所需注意或設定的參數
- 突變方式 (Mutation method)
- 突變率 (Mutation rate)

---------------------------------

### :arrow_down_small: 適應值計算 (Fitness computation) <br>

:balloon: **適應函數用來評估染色體品質**<br>

用GA求解問題時，必須制定屬於這個問題的適應函數 (Fitness function)，**適應函數是用來評估染色體好壞的機制**，透過轉換出來的適應值 (Fitness value)，來判斷染色體的適應度，當適應值越好，在下一個步驟選擇染色體時，該染色體就有越大的機率被保留下來繼續繁衍，相反的，適應值越糟，則越有可能被淘汰。

:balloon: **制定適應函數 (Fitness function)** <br>

一般來說，**適應函數通常是求解問題的目標函數**，或者訂定一個足以代表求解問題目標的函數，以能夠充分評估染色體的品質。

:bulb: 基本上在執行這個步驟前，必須先將染色體進行解碼才能進一步的去計算適應值。

#### :unlock: 本步驟所需注意或設定的參數
- 適應函式 (Fitness function)

-----------------------------------

### :arrow_down_small: 選擇 (Selection) <br>

為了保留更優秀的染色體來進行演化，此步驟主要是根據上面步驟所產生的染色體，透過一些選擇機制 (Selection mechanism)，來進行挑選，將品質較好的染色體留下來，形成新的族群，來進行下一回合的演化，以下將介紹兩種選擇機制：<br>

**1. 輪盤法 (Roulette wheel)** <br>

輪盤法的概念可以想像成射飛鏢遊戲，首先我們將一個可轉動的輪盤，劃分出許多面積大小不同的扇形區域，每個染色體都有相對應專屬的扇形區，接著我們拿出一支飛鏢，隨意射向這個輪盤，當我射到哪個扇形區，屬於這個扇形區的染色體將會被選擇，因此可想而知，擁有面積較大的染色體，將有較大的機率會被選擇，當然，染色體所屬的扇形面積並非隨意劃分，而是透過它們的適應值所推得而來，以下將說明輪盤法的詳細步驟：<br>

<br>
<div align=center>
<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/14.gif" width="445" height="250">
</div>
<br> 

( eval()：適應函數、v<sub>k</sup></sub>：第 k 個染色體、eval(v<sub>k</sup></sub>)：第 k 個染色體的適應值 ) <br>

:balloon: Step 1. 計算所有要被選擇染色體的適應值總和 F

<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/8.png" width="250" height="115">

:balloon: Step 2. 對每個染色體 v<sub>k</sup></sub>，計算其選擇機率 p<sub>k</sup></sub>

<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/9.png" width="360" height="50">

:balloon: Step 3. 對每個染色體 v<sub>k</sup></sub>，計算其累積機率 q<sub>k</sup></sub>

<img src="https://github.com/wurmen/Genetic-Algorithm-for-Job-Shop-Scheduling-and-NSGA-II/blob/master/introduction/GA/picture/10.png" width="450" height="70">

:balloon: Step 4. 從區間 [ 0 , 1 ] 中，隨機產生一個數字 r


:balloon: Step 5. 如果 r <= q<sub>1</sup></sub>，則選擇第一條染色體，否則，當q<sub>k-1</sup></sub> < r < q<sub>k</sup></sub>，則選擇第 k 個染色體 v<sub>k</sup></sub>


:balloon: Step 6. 回到 Step 4 ，直到選擇的染色體數量，達到所設定的族群大小<br>

**Example**<br>
假設現在有一個最大化的問題，共有四個染色體，這四個染色體的適應值，分別為 4、7、3、6 <br>
- Step 1. 計算所有要被選擇染色體的適應值總和 F<br>
F = 4 + 7 + 3 + 6 = 20

- Step 2. 對每個染色體 vk，計算其選擇機率 pk<br>
p1 =0.2 、p2 =0.35、p3 =0.15、p4 =0.3

- Step 3. 對每個染色體 vk，計算其累積機率 qk<br>
q1=0.2、 q2=0.55、 q3=0.7、 q4=1

- Step 4. 從區間 [ 0 , 1 ] 中，隨機產生一個數字 r <br>
r = 0.6

**2. 競爭選取法 (Tournament selection)** <br>

隨意從族群中挑選若干個染色體出來，比較它們的適應值，從中選擇具有最佳適應值的染色體出來，重複執行上述動作，直到選擇的染色體數量，達到所設定的族群大小。 (一次要挑選出來比較的染色體數，可依個人自行設定一個合理的挑選個數)

#### :unlock: 本步驟所需注意或設定的參數
- 選擇機制 (Selection mechanism)

----------------------------------------
### :arrow_down_small: 終止條件 (Termination condition)<br>

通常會設定一個停止機制來當作終止條件，一旦尚未達到所設定的停止條件，則會將最後一步驟所產生的新族群，回到突變與交配的步驟，再依序往下執行其他步驟，不斷的循環，直到到達設定的停止條件到達為止，最後即可得到在所有迭代中獲得的最佳解。一般而言常見的停止機制如下所示：
- 迭代次數 (Number of iterations)
- 連續幾次解不變的次數
- 連續幾次解的差異都小於設定的數字時停止

#### :unlock: 本步驟所需注意或設定的參數
- 迭代次數 (Number of iterations)

## :black_nib: 總結 (Summary)
經過上述的介紹，這裡總結一下，在使用基因演算法時，一般而言，必須設定的幾個參數：<br>

- 編碼方式 (Encoding method)
- 染色體的長度 (Chromosome length)
- 族群大小 (Population size)
- 交配方式 (Crossover method)
- 交配率 (Crossover rate)
- 突變方式 (Mutation method)
- 突變率 (Mutation rate)
- 適應函式 (Fitness function)
- 選擇機制 (Selection mechanism)
- 終止條件 (Termination condition)

## :black_nib: Reference
- Holland, J. H. (1975). Adaptation in natural and artificial systems. Ann Arbor, MI: University of Michigan Press.
- Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization and Machine Learning. Addison-Wesley Longman Publishing Co., Inc. Boston, MA.
- Chia-Yen Lee  (2017), Meta-Heuristic Algorithms-Genetic Algorithms & Particle Swarm Optimization, Intelligent Manufacturing Systems course

