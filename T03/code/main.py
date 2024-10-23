from fastapi import BackgroundTasks, FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
import uvicorn# web服务器
import uuid
from audio_process import transcribe_audio, freq_cloud, get_tasks, optimize
from pathlib import Path
import os

#实例化FastAPI对象p
app = FastAPI()

#设置静态文件路由
app.mount("/output", StaticFiles(directory='../output'), name='output')
@app.post('/upload_audio')#上传音频文件接口
async def upload_audio(file: UploadFile, background_tasks: BackgroundTasks):
    """ 接收用户上传的播客长音频文件,返回一个唯一的任务ID,供用户查询任务状态或获取处理结果 """
    #生成唯一任务ID
    id = str(uuid.uuid4())
    # 获取文件名和后缀名
    file_name = file.filename
    file_suffix = Path(file_name).suffix
    # 保存文件到磁盘
    file_path = f"../input/{id}{file_suffix}"
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)  # 读取文件块
            if not chunk:
                break
            buffer.write(chunk)
    #将音频转文本加入后台任务
    background_tasks.add_task(transcribe_audio, id, file_path, file_suffix)
    #将词频统计和词云生成加入后台任务
    background_tasks.add_task(freq_cloud, id)
    #将文本优化加入后台任务
    background_tasks.add_task(optimize, id)

    return {"task_ID": id}
    
@app.get('/task_status/{task_id}')
async def get_task_status(task_id: str):
    """ 根据任务ID查询音频文件的处理状态 """
    task = get_tasks().get(task_id)
    if not task:
        return {"error": "Task not found"}
    else:
        return {"status": task.status}

@app.get('/task_result/{task_id}')
async def get_task_result(task_id: str):
    """ 根据任务ID查询音频文件的处理结果 """
    task = get_tasks().get(task_id)
    if not task:
        return {"error": "Task not found"}
    else:
        return {
    "transcription_url": (
        f"http://127.0.0.1:8080/output/{task.id}/transcription.txt"
        if task.status["transcription"] == 'completed'
        else f'task {task.status["transcription"]}'
    ),
    "word_frequency_url": (
        f"http://127.0.0.1:8080/output/{task.id}/frequency.txt"
        if task.status["wordcloud"] == 'completed'
        else f'task {task.status["wordcloud"]}'
    ),
    "wordcloud_url": (
        f"http://127.0.0.1:8080/output/{task.id}/wordcloud.png"
        if task.status["wordcloud"] == 'completed'
        else f'task {task.status["wordcloud"]}'
    ),
    "optimized_text_url": (
        f"http://127.0.0.1:8080/output/{task.id}/optimized_text.txt"
        if task.status["optimization"] == 'completed'
        else f'task {task.status["optimization"]}'
    ),
}
    
if __name__ == '__main__':
    uvicorn.run(app="main:app", host='127.0.0.1', port=8080, reload=True)
