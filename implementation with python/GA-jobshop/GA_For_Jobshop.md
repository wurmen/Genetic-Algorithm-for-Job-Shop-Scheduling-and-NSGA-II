# Solving Job shop scheduling problem with genetic algorithm

*POLab* <br>
*[cheng-man wu](https://www.linkedin.com/in/chengmanwu)*<br>
*2018/07/14*
<br>

## :black_nib: 前言 <br>

這裡要來說明如何運用 GA 來求解 Job shop 的問題，以下將先對 Job shop 問題做個簡介，接著描述本範例的求解問題以及編碼原則說明，最後會根據每個程式區塊進行概念上的講解

### :arrow_down_small: 什麼是 flow shop 問題? <br>



## :black_nib: 問題描述 <br>


### :arrow_down_small: 排程目標 <br>




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

