import os

apikey = os.getenv('ZHIPUAI_API_KEY')
if apikey is None:
    raise EnvironmentError("未找到环境变量 'ZHIPUAI_API_KEY'。")
else:
    print(f"API密钥已设置,值为: {apikey[:5]}...")  # 仅显示部分密钥