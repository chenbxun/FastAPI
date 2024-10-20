import os                           # 文件的增删改查
# import speech_recognition as sr   # 离线语音识别库(放弃使用)
import whisper                      # 离线语音识别库
import time                         # 模拟音频处理的阻塞操作
from langdetect import detect       # 语言识别库
import opencc                       # 中文转繁体库     
import re                           # 正则表达式库
import jieba                        # 结巴分词
import jieba.posseg                 # 词性获取
import collections                  # 词频统计库
import wordcloud                    # 词云展示库
import matplotlib.pyplot as plt     # 图像展示库
import zhipuai                      # 智谱清言api接口
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

# 任务对象
class Task:
    def __init__(self, id, status1="in_process", status2="in_process", status3="in_process"):
        self.id = id
        self.status = {"transcription": status1, "wordcloud": status2, "optimization": status3}

#保存任务对象的字典
tasks = {}
#加载语音识别模型
model = whisper.load_model("base")
#轮询上一任务状态的时间间隔
INTERVAL = 0.5
#保存语言识别的结果
language = None
#词云统计词个数
number = 100  
#移除的特殊字符                        
replace = u'[\t\n;:<>"~!@#$%^&*()\-+\[\]\|{}/*.,\?]+'
#智谱清言api密钥
ApiKey=""
#支持的音频文件类型
supported_audio_types = ['.wav', '.mp3', '.flac', '.m4a', '.aac', '.amr', '.ogg', '.opus', '.vorbis', '.wma']

def transcribe_audio(id: str, file_content: bytes, file_suffix: str):
    """ 利用本地库实现音频转文本 """
    global tasks, model, language, supported_audio_types
    # 新建一个任务对象，并将其保存在字典中
    if id not in tasks:
        tasks[id] = Task(id=id)

    #不支持的格式
    if file_suffix not in supported_audio_types:
        print(f"{id} Unsupported file type {file_suffix}")
        tasks[id].status["transcription"] = 'failed'
        return

    #保存路径
    file_path = f"../input/{id}{file_suffix}"
    #本地缓存音频文件
    with open(file_path, "wb") as f:
        f.write(file_content)

    # r = sr.Recognizer()
    # harvard = sr.AudioFile(file_path)
    # with harvard as source:
    #     audio = r.record(source)

    try:
        print(f"Start transcripting audio file {id}")
        # text = r.recognize_sphinx(audio)
        result = model.transcribe(file_path)
        print(f"Finish transcripting audio file {id}")

        #识别语言
        text = result['text']
        language = detect(text)

        #繁体字转简体中文
        if language == 'zh-hk' or 'zh-tw':
            cc = opencc.OpenCC("t2s")
            text = cc.convert(text)

        #控制台输出转录结果 
        language = detect(text)
        print("Language:", language)
        print("Text:", text)

        # 缓存到本地
        save_dir = f'../output/{id}/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        with open(save_dir + 'transcription.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        # 更新任务状态为完成
        tasks[id].status["transcription"] = 'completed'

    except Exception as e:
        # 如果在转录过程中发生错误，更新任务状态为失败
        print(f"Error transcripting audio file {id}: {e}")
        tasks[id].status["transcription"] = 'failed'
    finally:
        # 删除原始音频文件
        if os.path.exists(file_path):
            print(f"Removing audio file {id}")
            os.remove(file_path)
        print(f"Finish processing audio file {id}")

def freq_cloud(id: str):
    """ 对转录后的文本进行词频统计，并基于统计结果生成词云数据 """
    global tasks
    #等待任务创建
    while id not in tasks.keys(): 
        time.sleep(INTERVAL)
        print(f"freq_cloud{id}: waiting")

    #等待文本转录任务完成
    while tasks[id].status["transcription"] == 'in_process': 
        time.sleep(INTERVAL)
        print(f"freq_cloud{id}: waiting")

    #音频转录失败
    if tasks[id].status["transcription"] == 'failed':
        tasks[id].status["wordcloud"] = 'failed'
        return
    
    print(f"start freq_cloud {id}")
    # time.sleep(30)
    with open(f"../output/{id}/transcription.txt", "r", encoding='utf-8') as f:  #打开文本
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
    else:
        print(f'{id}: {language}, unsupported language.')
        tasks[id].status["wordcloud"] = 'failed'
        return

    # 去除停用词
    with open('../input/text/stopwords_full.txt', 'r', encoding='UTF-8') as meaninglessFile:
        stopwords = set(meaninglessFile.read().split('\n'))
    stopwords.add(' ')
    words = [word for word in words if word not in stopwords]

    # 词频统计
    word_counts = collections.Counter(words)       # 对分词做词频统计
    word_counts_top = word_counts.most_common(number)    # 获取前number个最高频的词

    #检查保存目录是否存在
    save_dir = f'../output/{id}/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # 导出文件
    fileOut = open(save_dir + 'frequency.txt', 'w', encoding='UTF-8')  # 创建文本文件；若已存在，则进行覆盖
    fileOut.write('word\tfrequency\n')
    fileOut.write('——————————\n')
    for TopWord, Frequency in word_counts_top:  # 获取词语和词频
        # print(TopWord + '\t' + str(Frequency))
        fileOut.write(TopWord + '\t' + str(Frequency) + '\n')
    fileOut.close()  # 关闭文件

    # 生成词云
    wc = wordcloud.WordCloud(font_path='simhei.ttf',  # 设置字体（确保支持中文）
                        width=800, height=400).generate_from_frequencies(word_counts)

    # 保存词云图像
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(save_dir + 'wordcloud.png', dpi=300)  # 保存为PNG文件，300 DPI的分辨率

    print(f"finish freq_cloud {id}")

    # 更新任务状态
    tasks[id].status["wordcloud"] = 'completed'

def optimize(id: str):
    """ 使用大语言模型优化转录文本,将其生成可读性强的博客或论文形式 """
    global tasks
    #等待任务创建
    while id not in tasks.keys(): 
        time.sleep(INTERVAL)
        print(f"optimization{id}: waiting")

    #等待文本转录任务完成
    while tasks[id].status["transcription"] == 'in_process': 
        time.sleep(INTERVAL)
        print(f"optimization{id}: waiting")

    #音频转录失败
    if tasks[id].status["transcription"] == 'failed':
        tasks[id].status["optimization"] = 'failed'
        return
    
    print(f"start optimization {id}")
    # time.sleep(30)
    with open("../input/text/prompt.txt", "r", encoding='utf-8') as f:  #打开文本
        prop = f.read()   #读取提示词
    with open(f"../output/{id}/transcription.txt", "r", encoding='utf-8') as f:  #打开文本
        content = f.read()   #读取文本
 
    question = prop + content
    prompt=[]
    prompt.append({"role": "user", "content": question})
    client = zhipuai.ZhipuAI(api_key=ApiKey)
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=prompt
    )
    resp = response.choices[0].message.content

    #检查保存目录是否存在
    save_dir = f'../output/{id}/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # 导出文件
    fileOut = open(save_dir + 'optimized_text.txt', 'w', encoding='UTF-8')  # 创建文本文件；若已存在，则进行覆盖
    fileOut.write(resp)
    print(f"finish optimization {id}")

    # 更新任务状态
    tasks[id].status["optimization"] = 'completed'
def get_tasks():
    """ 返回保存所有任务的字典,用于main.py获取任务处理情况 """
    global tasks
    return tasks
