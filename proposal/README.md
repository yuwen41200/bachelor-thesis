# Research Proposal #

社群網站上之政治活動分析：以台灣 2016 年總統選舉為例  
Analysis of Political Activities on Social Networking Sites: A Perspective from 2016 Taiwan Presidential Election

學生：蒲郁文／指導教授：孫春在  
Student: Yu-wen Pwu / Advisor: Prof. Chuen-tsai Sun

國立交通大學資訊工程學系
Department of Computer Science, National Chiao Tung University, Taiwan

關鍵字：數位行動主義、社群媒體、社會網絡分析、政治參與、台灣政治  
Keywords: Digital Activism, Social Media, Social Network Analysis, Political Participation, Politics of Taiwan

## 文獻回顧 ##

Larsson and Moe, 2012

* 摘要
  * 蒐集選舉期間含有特定 hashtag 的推文，進行社會網絡分析（SNA）。
* 資料分析
  * 不同時間推文數量的變化。
  * 各種推文類型（一般、提及、轉推）所佔的比例。
  * 列出最活躍的使用者及其推文數量，並調查其身份背景。
  * 活躍用戶的「提及」網絡圖（透過資料視覺化）。
  * 呈上，將使用者分為發送者、接受者、兩者皆是，並調查其身份背景。
  * 活躍用戶的「轉推」網絡圖（透過資料視覺化）。
  * 呈上，將使用者分為轉推者、被轉推者、兩者皆是，並調查其身份背景。
* 資料解讀
  * 推文數量的變化反應了線下競選活動的情勢。
  * 大部份的推文都是由少部份的活躍用戶所發出。
  * 大部份的活躍用戶都是政治精英，然而，平民的聲音仍具有一定的影響力。
  * 大部份的推文都是一般推文，然而，許多活躍用戶仍會在 Twitter 上與人討論。
* 研究限制
  * 只有極少數的民眾有使用 Twitter。
  * 只蒐集含有特定 hashtag 的推文。
  * 應分析不同情境下的使用情形，加以比較。
* 問題
  * 如何區別真人用戶與機器用戶？

Zhang et al., 2010

* 摘要
  * 社群網站的使用與公民參與的提升呈現顯著的正相關。
  * 討論政治議題有助於促進公民參與和政治參與。

Hosch-Dayican et al., 2016

* 摘要
  * 相較於政治人物，平民更常使用負面宣傳（negative campaigning）。
  * 透過質化內容分析（qualitative content analysis），發現大部份的推文都是在宣洩情緒與意見。

Tzeng and Zhang, 2014

* 摘要
  * 網路促成的公民運動，其規模差異可用三個要素來解釋：情緒蔓延因子、認知門檻障礙、技術門檻障礙。

## 研究方向 ##

第一部份：可藉由已知的公開資料探討的議題

1. 哪些貼文最熱門？（最多人傳達心情／留言／分享）  
   留言／分享人數對時間的關係圖。
2. 有多少比例的貼文／留言是負面宣傳？  
   誰／什麼時候最常使用負面宣傳？
3. 各發文者與其分享的連結之網絡圖。  
   特定族群是否會傾向於分享特定來源的資訊？
4. 比較使用者於網路上對各政黨／候選人表達支持的人數與實際的選舉結果。  
   社群網站上的輿論反應出社會大眾意見的程度。

第二部份：需向使用者蒐集資料才能得到完整解答的議題【困難！】

1. 社會大眾意見極化之現象是否存在？該如何理解？  
   以下是我的推論。

   > (a) 有愈來愈多人使用社群媒體來接收政治新聞。  
   > (b) 台灣許多發佈政治新聞的粉絲專頁都有很鮮明的意識型態，報導內容也相當偏頗。  
   > (c) 社群媒體的檢索演算法會將我們最可能感興趣的文章排序在最前面。  
   > -> 抱持特定立場者會關注特定的粉絲專頁。  
   > (d) 機器用戶於粉絲專頁大量留言，或擁護自己的立場，或對反對者批評謾罵。  
   > -> 強化對立並製造出擁有人數優勢的假象。  
   > -> 使用者對自己的立場更加堅定。  
   > -> 缺少機會傾聽反對者的想法，人們意見更加分歧，難以達成共識。

2. 線上政治參與可能為台灣政治帶來哪些正面／負面影響？  
   非本次研究範圍，但因其具有研究價值，仍列入研究企畫。

## 研究方法 ##

* 量化研究（quantitative research）

  作為一個資訊科學的研究計畫，比較適合採用量化研究。

* Facebook Graph API

  蒐集選舉期間各大政治性粉絲專頁之公開資料。

* R: The R Project for Statistical Computing

  進行資料之統計與繪圖。

* Gephi: The Open Graph Visualization Platform

  進行社會網絡分析之視覺化。

* 問卷調查

  針對第二部份，設計問卷以調查使用者使用社群網站之習慣、張貼政治評論之動機等。

## 參考文獻 ##

1. Larsson, A. O., & Moe, H. (2012). Studying political microblogging: Twitter users in the 2010 Swedish election campaign. New Media & Society, 14(5), 729-747.

   http://nms.sagepub.com/content/14/5/729

2. Zhang, W., Johnson, T. J., Seltzer, T., & Bichard, S. L. (2010). The Revolution Will be Networked: The Influence of Social Networking Sites on Political Attitudes and Behavior. Social Science Computer Review, 28(1), 75-92.

   http://ssc.sagepub.com/content/28/1/75

3. Hosch-Dayican, B., Amrit, C., Aarts, K., & Dassen, A. (2016). How Do Online Citizens Persuade Fellow Voters? Using Twitter During the 2012 Dutch Parliamentary Election Campaign. Social Science Computer Review, 34(2), 135-152.

   http://ssc.sagepub.com/content/34/2/135

4. Tzeng, A., & Zhang, J. (2014). Internet-Facilitated Social Activism in Taiwan: Modes and Constraints. Paper presented at the XVIII ISA World Congress of Sociology, Yokohama, Japan.

   https://isaconf.confex.com/isaconf/wc2014/webprogram/Paper39547.html
