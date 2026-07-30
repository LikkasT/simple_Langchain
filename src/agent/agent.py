from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os
import readline
QuitText = 'q'
class LLM:
    def __init__(self):
        load_dotenv(".env.local",override=True)
        self.api_key= os.getenv("DEEPSEEK_API_KEY").strip()
        self.model= os.getenv("MODEL").strip()
        self.url= os.getenv("DEEPSEEK_BASE_URL").strip()
        try:
            self.thinking_timeout= float(os.getenv("TINKING_TIMEOUT",30).strip())
            self.num_retries= int(os.getenv("RETRY_NUM",2).strip())
            self.temperature= int(os.getenv("TEMPERATURE",1).strip())
            self.stream= True if os.getenv("STREAM").strip() == 'True' else False
            self.max_token= int(os.getenv("MAX_TOKEN").strip()) if os.getenv("MAX_TOKEN").strip() else None
        except Exception as e:
            raise Exception(f'配置文件传入非法参数。错误信息：{e}')
        self.set_llm()
    def set_llm(self):
        self.llm = ChatDeepSeek(
            model= self.model,
            api_key= self.api_key,
            streaming= self.stream,
            api_base= self.url,
            temperature=self.temperature,
            request_timeout= self.thinking_timeout,
            max_tokens= self.max_token,
            max_retries= self.num_retries,
            # model_kwargs=   {'tools':[]}##用来存放一些langchain没有列出但模型本身支持的，比如tools
            # extra_body= {}  ##基于openai个性化字段 比如thinking
            # configurable_fields= ('model','temperature') ## 用来允许 config中的configurable 覆盖
        )

def clear_memery(messages,max_length):
    system_messages = [m for m in messages if m.get('role')=='system']
    conversation_messages = [m for m in messages if m.get('role')!='system']
    cleaned_messages = conversation_messages[-(max_length*2):]
    return system_messages+cleaned_messages

