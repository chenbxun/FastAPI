# 题目

## 1. 学习使用 Github 和 Markdown，建立一个 GitHub 仓库用于存放解题文件，文件夹结构见本文档末尾的`<提交>`板块。

## 2. 请从以下五个可视化研究领域中选择一个（每个方向后附有一篇相关文献），然后总结该领域内至少五篇相关文献的可视化研究。请确保在总结中涵盖这些文献的主要贡献和创新点：

### a. presentation video visualization

- 参考文献: GestureLens: Visual Analysis of Gestures in Presentation Videos
- 链接: https://ieeexplore.ieee.org/document/9761750

### b. geospatial data visualization

- 参考文献: GTMapLens: Interactive Lens for Geo-Text Data Browsing on Map
- 链接: https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.13995

### c. information diffusion visualization

- 参考文献: RumorLens: Interactive Analysis and Validation of Suspected Rumors on Social Media
- 链接: https://arxiv.org/abs/2203.03098

### d. multimodal video visualization

- 参考文献: Anchorage: Visual Analysis of Satisfaction in Customer Service Videos Via Anchor Events
- 链接: https://ieeexplore.ieee.org/abstract/document/10045801

### e. emotion analysis visualization

- 参考文献: EmotionCues: Emotion-Oriented Visual Summarization of Classroom Videos
- 链接: https://ieeexplore.ieee.org/abstract/document/8948010

## 3. 实现一个基于 FastAPI 的后端服务，处理播客的长音频文件，提供音频转文本、词频统计、词云生成及文本优化功能。

### a. 提供接口

#### i. 上传音频文件接口

- 功能: 接收用户上传的播客长音频文件，返回一个唯一的任务ID，供用户查询任务状态或获取处理结果
- 输入: 用户上传的音频文件
- 输出: 用于后续查询处理进度或结果的任务ID (`task_id`)
- 接口: `POST /upload_audio`

#### ii. 查询任务状态接口

- 功能: 根据任务ID查询音频文件的处理状态（处理中、已完成等）
- 输入: 任务ID (`task_id`)
- 输出: 任务状态（处理中、已完成、失败等）
- 接口: `GET /task_status/{task_id}`

#### iii. 获取处理结果接口

- 功能: 根据任务ID获取已处理的结果（包括转录文本、词频统计、词云数据、优化后的文本）
- 输入: 任务ID (`task_id`)
- 输出: 已处理的结果
- 接口: `GET /task_result/{task_id}`

### b．实现功能（所有数据都可以本地缓存，不需要涉及数据库等服务）

#### i. 音频转文本

- 功能: 将上传的音频文件转录为文本，使用本地的音频转文本服务（可以使用现有的开源库）
- 流程:
    1. 收到音频文件后，调用本地的音频转文本包，处理音频并生成转录文本
    2. 将转录结果缓存到本地文件系统，供后续使用
- 输入: 音频文件
- 输出: 转录后的文本文件

#### ii. 词频统计和词云生成

- 功能: 对转录后的文本进行词频统计，并基于统计结果生成词云数据
- 流程:
    1. 解析转录文本，移除停用词，统计各词语出现的频率
    2. 生成词频数据并生成词云数据
    3. 将词频和词云数据缓存供查询
- 输入: 转录文本
- 输出：词频统计数据和有效词云数据

#### iii．文本优化

- 功能: 使用大型语言模型优化转录文本，将其生成可读性强的博客或论文形式
- 流程:
    1. 使用本地或远程的大型语言模型（LLM），通过特定提示词（Prompt）对转录的原始文本进行优化
    2. 将优化后的文本缓存，供用户获取
- 输入: 转录文本
- 输出: 优化后的文本文件

### 总体流程：

a．用户上传长音频文件，后端返回任务ID。
b．后端处理音频，转录成文本。
c．进行词频统计并生成词云。
d．使用 LLM 优化文本。
e．用户根据任务ID查询任务状态或获取处理结果（包括转录文本、词频统计、词云数据和优化后的文本）。

## 4. 在完成上述题目时，你使用了哪些 AI 工具？它们分别解决了哪些具体问题？请分享你的使用体验和感受。
