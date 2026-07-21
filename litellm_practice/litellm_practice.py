from dotenv import load_dotenv
from typing import Any
import os
import litellm_practice.litellm_practice as litellm_practice
import asyncio
class LLM:
    def __init__(self):
        env = os.getenv('ENV','local')
        load_dotenv(f'.env.{env}',override=True)
        self.api_key = os.getenv("API_KEY").strip()
        self.model = os.getenv("MODEL").strip()
        print(f"=========={self.model}")
        self.url = os.getenv("BASE_URL").strip()
        try:
            self.thinking_timeout = float(os.getenv("TINKING_TIMEOUT",30).strip())
            self.num_retries = int(os.getenv("RETRY_NUM",2).strip())
            self.temperature = int(os.getenv("TEMPERATURE",1).strip())
            self.stream = True if os.getenv("STREAM").strip() == 'True' else False
            self.max_token = int(os.getenv("MAX_TOKEN").strip()) if os.getenv("MAX_TOKEN") else None
        except Exception as e:
            raise Exception(f'配置文件传入非法参数。错误信息：{e}')
        
    async def run(self,message: list[dict],**kwargs: Any):
        param : dict[str,Any] = {
            'model': self.model,
            'api_key':self.api_key,
            'timeout':self.thinking_timeout, 
            'messages':message,
            'temperature': self.temperature,
            'stream': self.stream,
            'base_url': self.url,
            'max_tokens':self.max_token,
            'num_retries':self.num_retries,
            **kwargs
        }
        print(f"model: {param['model']}")
        try:
            res = await litellm_practice.acompletion(**param)
        except Exception as e:
            raise Exception(f"模型{self.model}调用失败，请检查配置。错误信息：{e}")
        return res
    async def send_message_once(self,message:str):
        m = []
        mes :dict[str,Any] = {
            'role': 'user',
            'content': message
        }
        m.append(mes)
        res = await self.run(m)
        return res

async def main():
    llm = LLM()
    res = await llm.send_message_once('你是什么模型')
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
