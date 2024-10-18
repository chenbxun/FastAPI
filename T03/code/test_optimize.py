import zhipuai

def GetReply(content):#生成针对content的个性化回复
    ApiKey="cc290d43585f010c842256b1fe5e900d.mesgGSSRsUhFgGCs"
    bginfo = "123"
    question=content
    prompt=[]
    prompt.append({"role": "system", "content": bginfo})
    prompt.append({"role": "user", "content": question})
    client = zhipuai.ZhipuAI(api_key=ApiKey)
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=prompt
    )
    print(response.choices[0].message.content)

GetReply("请问什么是机器学习？")