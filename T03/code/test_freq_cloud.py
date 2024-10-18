# 导入扩展库
import re                           # 正则表达式库
import jieba                        # 结巴分词
import jieba.posseg                 # 词性获取
import collections                  # 词频统计库
import wordcloud                    # 词云展示库
import matplotlib.pyplot as plt     # 图像展示库（这里以plt代表库的全称）

language = 'en'
number = 100                          
replace = u'[\t\n;:<>"~!@#$%^&*()\-+\[\]\|{}/*.,\?]+'

with open("test_en.txt", "r", encoding='utf-8') as f:  #打开文本
    string_data = f.read().lower()   #读取文本

# 文本预处理
pattern = re.compile(replace) # 定义正则表达式匹配模式（空格等）
string_data = re.sub(pattern, '', string_data)     # 将符合模式的字符去除

# 文本分词
if language == 'zh-cn':
    words = jieba.cut(string_data, cut_all=False, HMM=True)    # 精确模式分词+HMM
elif language == 'en':
    #（英文文本不需要分词，使用空格分隔单词）
    words = string_data.split()

# 去除停用词（去掉一些意义不大的词，如标点符号、嗯、啊等）
with open('stopwords_full.txt', 'r', encoding='UTF-8') as meaninglessFile:
    stopwords = set(meaninglessFile.read().split('\n'))
stopwords.add(' ')
words = [word for word in words if word not in stopwords]

# 词频统计
word_counts = collections.Counter(words)       # 对分词做词频统计
word_counts_top = word_counts.most_common(number)    # 获取前number个最高频的词

# 输出至工作台，并导出“词频.txt”文件
fileOut = open('词频.txt', 'w', encoding='UTF-8')  # 创建文本文件；若已存在，则进行覆盖
fileOut.write('词语\t词频\n')
fileOut.write('——————————\n')
for TopWord, Frequency in word_counts_top:  # 获取词语和词频
    # print(TopWord + '\t' + str(Frequency))
    fileOut.write(TopWord + '\t' + str(Frequency) + '\n')
fileOut.close()  # 关闭文件

# 4. 生成词云
wc = wordcloud.WordCloud(font_path='simhei.ttf',  # 设置字体（确保支持中文）
                      width=800, height=400).generate_from_frequencies(word_counts)

# 显示词云图像
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud.png', dpi=300)  # 保存为PNG文件，300 DPI的分辨率
plt.show()

