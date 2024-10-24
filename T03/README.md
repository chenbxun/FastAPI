## 更新日志 (Changelog)

### [v1.0.1] - 2024-10-24

#### 优化

- 将音频保存到本地磁盘由upload_audio函数负责，upload_audio无需将音频文件读到内存再将其传递给函数transcribe_audio。

#### 新增

- 对于在用whisper库转录音频过程中捕获到的异常，引入了 traceback 模块来获取异常的堆栈信息。
- 新增了多段中文播客音频用于测试。
- 为了提高代码的安全性，API密钥不再直接硬编码在源代码中，而是通过环境变量 ZHIPUAI_API_KEY 进行管理。

### [v1.0.0] - 2024-10-21

#### 初始版本

- 完成了项目的第一个版本。
- 设置了项目结构和文档。

## 文件夹结构

D:.
│  README.md
│
├─code
│  │  audio_process.py
│  │  main.py
│  │  test_freq_cloud.py
│  │  test_optimize.py
│  │  test_zhipuai_api_key.py
│  │
│  └─__pycache__
│          audio_process.cpython-312.pyc
│          main.cpython-312.pyc
│
├─input
│  ├─audio
│  │      M500001XYXr432F0q8.mp3
│  │      M500003BN6Ja2Bq2Jc.mp3
│  │      M500003mRBoY2hIlV3.mp3
│  │      simple test.m4a
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

## 结构解释

1. **code** 目录存放源代码。其中 `audio_process.py` 和 `main.py` 是主要的源代码文件，其余以 "test" 开头的 `.py` 文件用于特定模块的测试，在项目实际运行时无需关注。
2. **input** 目录存放用于测试的音频文件（测试音频转文字）和文本文件（测试词频统计和词云生成）。在 `text` 子目录下还有两个文件：`prompt.txt` 存放文本优化所需的提示词；`stopwords_full.txt` 存放中英文停用词。此外，后端在处理音频转录时会将音频文件临时保存在这个目录下，并在处理完成后删除这些文件。
3. **output** 目录用来保存后端对音频文件的处理结果。对于每段上传的音频，程序都会创建一个以其任务ID命名的子目录，用来存放对应的转录文本、词频统计、词云数据以及优化后的文本。

## 一些提示

1. `task_result/{id}` 查询接口不会直接输出处理后的数据，而是返回四个网址，用户可以通过这些网址查询具体的处理结果。
2. 程序能够自动识别播客音频的语言，当前版本仅支持中文和英文的处理。如果程序检测到其他语言，任务状态将被标记为 "failed"。
3. 程序支持多种格式的音频文件上传。如果上传的是非音频文件，程序将会报错并将任务状态设为 "failed"。
