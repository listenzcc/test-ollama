import random
from nicegui import ui
import ollama
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 添加全局线程池
executor = ThreadPoolExecutor()

# 初始化模型
model = 'deepseek-r1:7b'

def generate_feedback(scores):
    """调用 Ollama 生成建议（模拟延迟）"""
    try:
        scores_txt = open('./scores.txt').read()
    except FileNotFoundError:
        scores_txt = "注意力分数范围：0-100，越高表示注意力越集中"
    
    try:
        suggests_txt = open('./suggests.txt').read()
    except FileNotFoundError:
        suggests_txt = "建议包括：深呼吸、短暂休息等"

    response = ollama.generate(
        model=model,
        system = '\n'.join(['''
你是一个注意力状态咨询师，必须严格遵循以下规则：
1. 所有输出必须使用标准的Markdown格式
2. 分数数据用代码块包裹
3. 建议使用分点列表
4. 重点内容使用**加粗**或*斜体*
''',
f'注意力量表：{scores_txt}。',
f'建议风格：{suggests_txt}'
]),
        prompt=f'客户注意力分数：{scores}。用口语化方式直接告知结果并给出具体建议（限200字）',
        options={"temperature": 0.7, "num_predict": 2000},
    )

    feedback = response['response']
    print(feedback)
    return feedback

def submit_scores():
    """提交分数并显示加载状态"""
    # 验证输入
    try:
        scores = {
            '5分钟前': int(five_min_input.value),
            '2分钟前': int(two_min_input.value),
            '1分钟前': int(one_min_input.value),
            '当前': int(current_input.value),
        }
    except ValueError:
        ui.notify("请输入有效的分数（0-100）", type="negative")
        return

    # 显示加载状态
    loading.visible = True
    output.visible = False
    notify = ui.notify("正在生成建议，请稍候...", type="info")
    
    # 异步生成建议（避免阻塞UI）
    async def generate_async():
        try:
            # feedback = await ui.run.io_bound(generate_feedback, scores)
            # 在后台线程中运行阻塞操作
            feedback = await asyncio.get_event_loop().run_in_executor(
                executor, 
                generate_feedback, 
                scores
            )
            feedback = feedback.split('</think>', 1)[1].strip()
            feedback = feedback.replace('\n1.', '\n\n1.')
            print(feedback, file=open('content.txt', 'w'))
            output.set_content('\n'.join([
                '**注意力分析**',
                '```json',
                f'{scores}',
                '```',
                '---',
                feedback
            ]))
        except Exception as e:
            import traceback
            traceback.print_exc()
            ui.notify(f"生成失败：{e}", type="negative")
        finally:
            loading.visible = False
            output.visible = True

    ui.timer(0.1, generate_async, once=True)  # 微小延迟确保加载动画显示

# 界面布局
with ui.card().classes("w-full max-w-2xl mx-auto"):
    ui.label("🧠 注意力评估助手").classes("text-2xl font-bold")
    
    with ui.row().classes("w-full grid grid-cols-2 gap-4"):
        five_min_input = ui.number("5分钟前", min=0, max=100, value=random.randint(10, 90))
        two_min_input = ui.number("2分钟前", min=0, max=100, value=random.randint(10, 90))
        one_min_input = ui.number("1分钟前", min=0, max=100, value=random.randint(10, 90))
        current_input = ui.number("当前", min=0, max=100, value=random.randint(10, 90))
    
    ui.button("生成建议", on_click=submit_scores, icon="rocket").classes("mt-4")
    
    # 加载动画（初始隐藏）
    loading = ui.spinner(size="xl", color="primary").classes("mx-auto mt-8")
    loading.visible = False
    
    # 输出区域（初始隐藏）
    output = ui.markdown().classes("mt-4 p-4 bg-gray-100 rounded-lg border")
    output.visible = False
    # output.set_content(open('./content.txt').read())
    # output.visible = True

ui.run(title="注意力助手", port=8080)