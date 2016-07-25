# Research Proposal #

社群網站上之政治活動分析：以台灣 2016 年總統選舉為例  
Analysis of Political Activities on Social Networking Sites: A Perspective from 2016 Taiwan Presidential Election

學生：蒲郁文／指導教授：孫春在  
Student: Yu-wen Pwu / Advisor: Prof. Chuen-tsai Sun

國立交通大學資訊工程學系  
Department of Computer Science, National Chiao Tung University, Taiwan

關鍵字：數位行動主義、社群媒體、社會網絡分析、政治參與、台灣政治  
Keywords: Digital Activism, Social Media, Social Network Analysis, Political Participation, Politics of Taiwan

## 研究原則 ##

近年來，愈來愈多學者開始嘗試將計算機科學應用於人文社會科學領域。  
然而，這樣的跨領域研究是否真的有價值一直是備受爭議的。  
以下舉出一些此類研究常受到的批評，以及我從事此類研究的立場。

### 常見對數位人文（digital humanities）的批評 ###

1. 只是用一些空洞的戲法來賣弄他們的研究能力，而沒有真正做出什麼新的分析。
2. 容易忽略種族、階級、性別、文化、意識型態等議題。
3. 現代社會中，一切都已經被商品化了，人文學科日漸式微。  
   但數位人文卻頂著科技的光環，而獲得了相當高的經費與聲望。
4. 研究者的背景不夠多元，其研究可能帶有某些偏見。

### 常見對社會模擬（social simulation）的批評 ###

1. 將現實社會過度地簡化為一般化的法則。
2. 模擬的成果仰賴預先建立好的模型，難以發現新的法則。
3. 預先建立的模型往往充滿偏見。
4. 模擬的成果並不能反映出現實社會的情況。

### 我的回應：傳統社會科學研究法仍是不可或缺的 ###

1. 並非所有問題都適合使用電腦來分析或模擬，有些現象無法被量化或歸納出一般化的法則。
2. 人文社會科學著重理解與詮釋，這部份的工作難以用電腦來取代。
3. 因此田野工作、民族誌、訪談等研究法仍有其彌足珍貴的價值。

### 我的回應：然而資訊科技仍然能對人文學科做出貢獻 ###

1. 數位人文提供了一個全新的視野來探究傳統上屬於人文社會科學領域的問題。
2. 資訊科技能幫助人文學者更有效率地獲得知識。
3. 資料探勘（data mining）、自然語言處理（NLP）等技術使一些過去被認為窒礙難行的研究成為可能。

## 文獻回顧 ##

從「洪仲丘事件」、「太陽花學運」到「反黑箱課綱運動」，網際網路均對社會運動的促成扮演了一個相當關鍵的角色。  
這也吸引了許多社會學家、傳播學家、計算機科學家對台灣數位行動主義研究產生興趣。  
儘管人們普遍同意數位行動主義能有效促進民主政治，這個趨勢仍然伴隨了一些潛在的隱憂。

### 常見對數位行動主義（digital activism）的批評 ###

1. 數位落差（digital divide）  
   由於經濟、教育等差異，有些族群缺少機會接觸資訊科技，或者沒有能力使用資訊科技。
2. 民粹主義（populism）  
   網路本質上便具有民粹主義、安那其（anarchy）、去中心化（decentralization）等特性，網路輿論的品質可能偏低。
3. 懶人行動主義（slacktivism）  
   並沒有參與什麼實際的行動，僅是在網路上分享自己關心的社會議題，便自以為自己已經對這個議題做出了貢獻。
4. 鍵擊行動主義（clicktivism）  
   類似懶人行動主義，若一味地追求點擊率、做網路行銷，可能反而會忽略了實際的行動。
5. 網路巴爾幹化（cyberbalkanization）  
   由於商業壟斷、政治審查、或是個人不願意接觸與自己立場相左的訊息等因素，使網際網路逐漸分裂、解體。

我挑選了數篇國內外的相關論文，作為這份研究的參考資料。

### Larsson and Moe, 2012 ###

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

### Zhang et al., 2010 ###

* 摘要
  * 社群網站的使用與公民參與的提升呈現顯著的正相關。
  * 討論政治議題有助於促進公民參與和政治參與。

### Hosch-Dayican et al., 2016 ###

* 摘要
  * 相較於政治人物，平民更常使用負面宣傳（negative campaigning）。
  * 透過質化內容分析（qualitative content analysis），發現大部份的推文都是在宣洩情緒與意見。

### Tzeng and Zhang, 2014 ###

* 摘要
  * 網路促成的公民運動，其規模差異可用三個要素來解釋：情緒蔓延因子、認知門檻障礙、技術門檻障礙。

## 研究方法 ##

採用量化研究（quantitative research），以下提出一些可行的作法。

### 資料蒐集 ###

Facebook Graph API  
蒐集選舉期間各大政治性粉絲專頁之公開資料。  
需注意蒐集的行為是否符合 Facebook 的使用條款（terms of use）。

### 資料探勘 ###

N/A

### 統計 ###

SciPy: Scientific Computing Tools for Python  
進行資料之統計與繪圖。

### 語意網絡 ###

N/A

### 社會網絡分析 ###

N/A

### 資料視覺化 ###

Gephi: The Open Graph Visualization Platform  
進行社會網絡分析之視覺化。

## 研究問題 ##

1. 哪些貼文最熱門？（最多人傳達心情／留言／分享）  
   留言／分享人數對時間的關係圖。
2. 有多少比例的貼文／留言是負面宣傳？  
   誰／什麼時候最常使用負面宣傳？
3. 各發文者與其分享的連結之網絡圖。  
   特定族群是否會傾向於分享特定來源的資訊？
4. 比較使用者於網路上對各政黨／候選人表達支持的人數與實際的選舉結果。  
   社群網站上的輿論反應出社會大眾意見的程度。

## 後續研究 ##

1. 社會大眾意見極化之現象是否存在？該如何理解？  
   以下是我的推論：  
   a. 有愈來愈多人使用社群媒體來接收政治新聞。  
   b. 台灣許多發佈政治新聞的粉絲專頁都有很鮮明的意識型態，報導內容也相當偏頗。  
   c. 社群媒體的檢索演算法會將我們最可能感興趣的文章排序在最前面。  
   -> 抱持特定立場者會關注特定的粉絲專頁。  
   d. 機器用戶於粉絲專頁大量留言，或擁護自己的立場，或對反對者批評謾罵。  
   -> 強化對立並製造出擁有人數優勢的假象。  
   -> 使用者對自己的立場更加堅定。  
   -> 缺少機會傾聽反對者的想法，人們意見更加分歧，難以達成共識。
2. 線上政治參與可能為台灣政治帶來哪些正面／負面影響？  

要回答這些問題，可能還需搭配問卷調查等方法。  
設計問卷以調查使用者使用社群網站之習慣、張貼政治評論之動機等。

## 參考文獻 ##

1. Larsson, A. O., & Moe, H. (2012). Studying political microblogging: Twitter users in the 2010 Swedish election campaign. New Media & Society, 14(5), 729-747.

   http://nms.sagepub.com/content/14/5/729

2. Zhang, W., Johnson, T. J., Seltzer, T., & Bichard, S. L. (2010). The Revolution Will be Networked: The Influence of Social Networking Sites on Political Attitudes and Behavior. Social Science Computer Review, 28(1), 75-92.

   http://ssc.sagepub.com/content/28/1/75

3. Hosch-Dayican, B., Amrit, C., Aarts, K., & Dassen, A. (2016). How Do Online Citizens Persuade Fellow Voters? Using Twitter During the 2012 Dutch Parliamentary Election Campaign. Social Science Computer Review, 34(2), 135-152.

   http://ssc.sagepub.com/content/34/2/135

4. Tzeng, A., & Zhang, J. (2014). Internet-Facilitated Social Activism in Taiwan: Modes and Constraints. Paper presented at the XVIII ISA World Congress of Sociology, Yokohama, Japan.

   https://isaconf.confex.com/isaconf/wc2014/webprogram/Paper39547.html
