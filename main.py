import ollama
import random

model = 'deepseek-r1:7b'

# response = ollama.generate(
#     model=model,
#     prompt="你是谁。"  # 提示文本
# )
# print(response)

# response = ollama.generate(
#     model=model,
#     system="你是一个专业的技术作家，用简洁的语言回答。",
#     prompt="解释一下量子计算的基本原理",
#     options={
#         "temperature": 0.7,  # 控制随机性（0-1）
#         "num_predict": 200,  # 最大生成长度
#     },
# )
# print(response["response"])


scores_txt = open('./scores.txt').read()
suggests_txt = open('./suggests.txt').read()

scores = {
    '5分钟前注意力分数': random.randint(10, 90),
    '2分钟前注意力分数': random.randint(10, 90),
    '1分钟前注意力分数': random.randint(10, 90),
    '当前注意力分数': random.randint(10, 90),
}

print(scores)

response = ollama.generate(
    model=model,
    system='你是一个注意力状态咨询师。你的注意力量表是 {}。我们公司给出的咨询建议是这种风格的，{}。'.format(scores_txt, suggests_txt),
    prompt='现在你的客户最近的注意力分数是{}。请告知他这个数值，并同时给出生动、可执行的建议。是直接说给客户的话，用口语化的风格即可。'.format(scores),
    options={
        "temperature": 0.7,  # 控制随机性（0-1）
        "num_predict": 2000,  # 最大生成长度
    },
)
print(response["response"])