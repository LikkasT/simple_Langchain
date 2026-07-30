from src.agent.agent import *

if __name__ == '__main__':
    conversation = [
        {
            'role':'system',
            'content':'你是一个专业、耐心的股票助理，在获取相关信息上有专业严谨的态度，每次回答问题前都会认真查询相关资料，力求回答准确无误，回答简洁'
        }
    ]
    i = 1
    chat_llm = LLM().llm
    print(f'开始新一轮对话，输入{QuitText}终止对话')
    while True:
        print(f"第{i}轮交互:",end="",flush=True)
        user_input = input("请输入消息：")
        if user_input == QuitText:
            print('对话已终止')
            break
        conversation.append({'role':'user','content':user_input})
        print('from AI :',end="",flush=True)
        reply_content = ""
        for chunks in chat_llm.stream(conversation):
            if chunks.content:
                print(chunks.content)
                reply_content = reply_content+chunks.content
        conversation.append({'role':'assistant','content': reply_content})
        conversation = clear_memery(conversation,10)
        
        i += 1