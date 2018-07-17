# 填字游戏

## 背景介绍

在大家喜闻乐见的填字游戏(Crossword)的基础上，littleRound进行了一些更改，创建了PVP和PVE两种玩法。

## 游戏规则

### 基本概念

棋盘：20x20的方形格子，其中可以填写a-z的字母

字母：a-z

单词：一些字母的组合，不区分大小写（算作同一个单词）

字典：单词的集合，存在于字典的单词为合法的单词，在称呼单词时，除特别说明，一般是指合法的单词

已有单词表：游戏过程中的一个临时记录，也是单词的集合

动作：一个动作指游戏中一方在一个轮次按规则在格子内填写若干字母的行为

### 游戏道具

一局游戏由棋盘、字典以及一个已有单词表构成

游戏开始时，格子部分位置已经填好了一些随机字母，已有单词表中存在一些单词

游戏由两方交替进行，在进行一个动作后交换，先手权由猜拳（题目中为随机）决定

### 合法动作

定义构成单词——在一次填写字母的过程中，如果使得棋盘上左右、上下、斜向（45度）上所有的线上的字符子串中，出现了满足下述条件的一个/些单词：

  		1. 存在于字典中
  		2. 任意前缀和后缀（包括自身）不存在于已有单词表中

则在将这个/些单词写入已有单词表后，称这此填写“构成单词”

一个满足下述条件的动作是合法的：

1. 在棋盘上填写字母
2. 本次填写的字母在同一条左右、上下、斜向（45度）的线上
3. 填写的字母与原来的字母在上述2中那条线上不间断
4. 填写的字母在上述2那条线上“构成单词”
5. 至少将上述2那条线上的所有的构成单词写入已有单词表（这意味着，可以在其他方向上满足构成单词的条件（并未实际构成单词）而不将其写入）

### 动作得分

动作的得分由下式计算：

得分 = 参与本次构成单词的所有单词所使用的字母 - 填写的字母

这意味着，如果不将其他方向上满足构成单词条件的情况写入已有单词表，则这些单词并不能参与记分

### 游戏结束

游戏在指定步数（共计50个动作）或无人可以继续填写后结束

### 输赢条件

在游戏结束后，双方所有动作的总分越高的获胜

### PVE版本

在PVE版本中，不是双方互搏，而是一方连续给出至多50个动作（或在50步以内停止），并计算总分

总分越高越好。

### 样例

![1](1.png)

- 初始状态

![2](2.png)

- 进行了一次合法的填写，使用了四个字母，故加四分（蓝色字母），构成单词的写入已有单词表

![3](3.png)

- 在多个方向中构成了单词，共得到七分

## 编程规范

本次希望大家编写PVE的版本

### 输入格式

#### 字典文件

第一行n为单词总数

接下来2-(n+1)行，每行一个单词，为字典内单词

#### 询问

前20行：为长度为20的字符串，‘-’表示空位，a-z表示该位置填有某个字母

第21行：一个m，表示已有单词表中的单词个数

第22-(21+m)行：每行一个单词，为已有单词表

### 输出格式

前20行：更改后的棋盘状态

第21行：一个k，表示要写入已有单词表的单词个数

第22-(21+k)行：每行一个单词，表示要写入的单词

#### 提交程序

提交两个程序，init.cpp 和 run.cpp

其中开始时会把字典文件dict.txt放到与init.cpp、run.cpp的编译结果init、run同目录下并运行init，init允许在该目录下生成合理大小(100MB以内)的缓存文件，然后每次评测程序会调用run并将当前局面按照询问格式通过stdin传给run并从run中拿到运行结果更新局面、计算分数。

如init或run程序意外终止或长时间无响应(init 5s, run 1s)，程序会视为无法继续动作并结算分数。

## 评分方式

50轮结束或程序停止输出后的总动作分数。

