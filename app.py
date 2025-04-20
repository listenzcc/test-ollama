import random
from nicegui import ui
import ollama

# 初始化 Ollama 模型
model = 'deepseek-r1:7b'

def generate_feedback(scores):
    """调用 Ollama 生成注意力建议"""
    # 读取注意力量表和建议模板（如果文件存在）
    try:
        scores_txt = open('./scores.txt').read()
    except FileNotFoundError:
        scores_txt = "注意力分数范围：0-100，越高表示注意力越集中"
    
    try:
        suggests_txt = open('./suggests.txt').read()
    except FileNotFoundError:
        suggests_txt = "建议包括：深呼吸、短暂休息、调整环境光线等"

    # 调用 Ollama
    response = ollama.generate(
        model=model,
        system=f'你是一个注意力状态咨询师。你的注意力量表是 {scores_txt}。建议风格参考：{suggests_txt}',
        prompt=f'客户最近的注意力分数是 {scores}。请直接告知他结果，并给出生动、可执行的建议（口语化，限200字内）。',
        options={"temperature": 0.7, "num_predict": 2000},
    )
    print(response['response'])
    return response["response"]

def submit_scores():
    """提交分数并生成反馈"""
    scores = {
        '5分钟前注意力分数': int(five_min_input.value),
        '2分钟前注意力分数': int(two_min_input.value),
        '1分钟前注意力分数': int(one_min_input.value),
        '当前注意力分数': int(current_input.value),
    }

    print(scores)
    
    # 显示分数
    ui.notify(f"提交的分数：{scores}")
    
    # 生成建议
    with card:
        card.clear()
        output = ui.markdown(content='Suggestion...').classes("mt-4 p-4 bg-gray-100 rounded-lg whitespace-pre-wrap")
        feedback = generate_feedback(scores)
        # output.set_text(feedback[:20])
        # output.set_text('bb')
        print(type(feedback))
        content = feedback.split('</think>', 1)[1].strip()
        print(content)
        output.set_content(content)  # 用 set_content 而非 set_text
        # output.set_content(f'{scores}')
        # output.set_content(''.join(['a' for e in content]))
        print(content, file=open('content.txt', 'w'))


# 创建输入界面
with ui.card().classes("w-full max-w-2xl mx-auto"):
    ui.label("注意力分数评估").classes("text-2xl font-bold")
    
    with ui.row():
        five_min_input = ui.number("5分钟前注意力分数", min=0, max=100, value=random.randint(10, 90)).classes('w-[8rem]')
        two_min_input = ui.number("2分钟前注意力分数", min=0, max=100, value=random.randint(10, 90)).classes('w-[8rem]')
        one_min_input = ui.number("1分钟前注意力分数", min=0, max=100, value=random.randint(10, 90)).classes('w-[8rem]')
        current_input = ui.number("当前注意力分数", min=0, max=100, value=random.randint(10, 90)).classes('w-[8rem]')
    
    ui.button("生成建议", on_click=submit_scores).classes("mt-4")
    
    # output = ui.label().classes("mt-4 p-4 bg-gray-100 rounded-lg")
    # output.set_text('aa')
    card = ui.card()
    with card:
        # spinner = ui.spinner(size="xl", color="primary").classes("mt-8")
        output = ui.markdown(content='Suggestion...').classes("mt-4 p-4 bg-gray-100 rounded-lg whitespace-pre-wrap")

# 启动应用
ui.run(title="注意力咨询助手", port=8080)