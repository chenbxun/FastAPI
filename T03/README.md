# 项目结构说明

## 文件夹结构
D:.
│  README.md
│
├─code
│  │  audio_process.py
│  │  main.py
│  │  test_freq_cloud.py
│  │  test_optimize.py
│  │
│  └─__pycache__
│          audio_process.cpython-312.pyc
│          main.cpython-312.pyc
│
├─input
│  ├─audio
│  │      经济学人.mp3
│  │      英语听力.mp3
│  │
│  └─text
│          prompt.txt
│          stopwords_full.txt
│          test_en.txt
│          test_zh.txt
│
└─output
    ├─经济学人音频处理结果
    │      frequency.txt
    │      optimized_text.txt
    │      transcription.txt
    │      wordcloud.png
    │
    └─英语听力音频处理结果
            frequency.txt
            optimized_text.txt
            transcription.txt
            wordcloud.png

## 目录结构解释

1. **code** 目录存放源代码。其中 `audio_process.py` 和 `main.py` 是主要的源代码文件，其余以 "test" 开头的 `.py` 文件用于特定模块的测试，在项目实际运行时无需关注。
2. **input** 目录存放用于测试的音频文件（测试音频转文字）和文本文件（测试词频统计和词云生成）。在 `text` 子目录下还有两个文件：`prompt.txt` 存放文本优化所需的提示词；`stopwords_full.txt` 存放中英文停用词。此外，后端在处理音频转录时会将音频文件临时保存在这个目录下，并在处理完成后删除这些文件。
3. **output** 目录用来保存后端对音频文件的处理结果。对于每段上传的音频，程序都会创建一个以其任务ID命名的子目录，用来存放对应的转录文本、词频统计、词云数据以及优化后的文本。

## 程序运行时的一些提示

1. `task_result/{id}` 查询接口不会直接输出处理后的数据，而是返回四个网址，用户可以通过这些网址查询具体的处理结果。
2. 程序能够自动识别播客音频的语言，当前版本仅支持中文和英文的处理。如果程序检测到其他语言，任务状态将被标记为 "failed"。
3. 程序支持多种格式的音频文件上传。如果上传的是非音频文件，程序将会报错并将任务状态设为 "failed"。