# Genetic Algorithm (GA)
*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/feed/?trk=nav_back_to_linkedin)*<br>

<br>

## :black_nib: GA 背景 (Background)
基因演算法(GA)的架構一開始是由John Holland教授於1975年所提出，該演算法的主要靈感來自於生物圈中的演化機制，在大自然中，生物的繁衍及遺傳是透過染色體的交配與變異，以改變不同基因的組成，來產生下一代，染色體主要是由DNA及蛋白質所組成，一段DNA片段代表著控制某一性狀的基因，因此染色體也表示是由許多基因所組成。<br>

簡單來說，基因演算法即是透過這種概念所發展，將求解問題的一個解或參數用一條染色體來表示，藉由編碼將染色體轉成字串或數值的形式，而每個數值或字串代表染色體內的基因，表示解的某個部分，接著透過突變及交配的方式，來產生下一代，也就是不同的解，最後以適者生存，不適者淘汰的觀念，將好的解進行保留，以進行下一輪的交配突變，來產生更好的解，期望未來能找到全域最佳解。<br>

基因演算法能用來求解大部分的最佳化問題，而本主題主要著重在 GA 與排程 (Scheduling)問題的結合與應用，因此以下將針對GA進行概念上的介紹，並於實作單元中說明GA如何運用於排程問題上。

## :black_nib: GA 流程 (Procedure)


## :black_nib: Reference
- Holland, J. H. (1975). Adaptation in natural and artificial systems. Ann Arbor, MI: University of Michigan Press.
- Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization and Machine Learning. Addison-Wesley Longman Publishing Co., Inc. Boston, MA.
