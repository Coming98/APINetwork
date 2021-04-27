1. 对数据集进行划分

> inputs: white black test - source data
>
> outputs: train_filenames (list)  test_filenames (list)

<details>
<summary><font color=darkred>preprocessing - 0</font></summary>
    <div style="padding-left:20px; border: 1px dashed #000">
=============================================<br>
train_filenames: <br>
length:  19999<br>
set length:  19999<br>
demo:  <br>00183dc70ab43aa5a20a1a88a2713e745c4cae0a75dd75125c0a8bf49ca1b541.xml # 0019348eddb972ded13c96670749c28c1b7f5dbfdb730d62c52b94b8b8a2db9a.xml<br>
length of the intersection with white_filenames:  9999<br>
length of the intersection with black_filenames:  10000<br>
length of the intersection with extra_filenames:  0<br>
=============================================<br>
test_filenames:<br>
length:  19999<br>
set length:  19999<br>
demo:  <br>00004cb3c839c9a6e7778d15768c5d2d67eeb088c2eb9af0705733cbfebea787.xml # 00005ee17aec986614a09daaa44e266671f23cb0d71b9b5761eeaedb8a622942.xml<br>
length of the intersection with white_filenames:  9999<br>
length of the intersection with black_filenames:  0<br>
length of the intersection with extra_filenames:  10000<br>
=============================================<br>
all:<br>
intersection between train set and test set:  set()<br>
    </div>
</details>

2. 获取API调用序列 inputs: 0

> inputs: white black test - source data; train_filenames, test_filenames;
>
> output: train_apinames_seq, test_apinames_seq
>
> Tips: 使用二维列表形式存储 - [ [] [] [] ] - 为了适应按照 pid 分类的序列

1. 

