from typing import List, Union, Generator, Iterator
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel
import os


class Pipeline:
    class Valves(BaseModel):
        LANGCHAIN_OLLAMA_BASE_URL: str
        LANGCHAIN_MODEL_NAME: str
        pass

    def __init__(self):
        self.name = "Ollama Langchain Pipeline"
        self.llm = None

        self.valves = self.Valves(
            **{
                "LANGCHAIN_OLLAMA_BASE_URL": os.getenv("LANGCHAIN_OLLAMA_BASE_URL", "http://host.docker.internal:11434"),
                "LANGCHAIN_MODEL_NAME": os.getenv("LANGCHAIN_MODEL_NAME", "gemma2:latest"),
            }
        )

        pass

    async def on_startup(self):
        from langchain_ollama import ChatOllama

        print("Langchain ollama pipline startup begin.")

        self.llm = ChatOllama(
            model=self.valves.LANGCHAIN_MODEL_NAME,
            base_url=self.valves.LANGCHAIN_OLLAMA_BASE_URL,
        )

        print("Langchain ollama pipline startup done.")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom RAG pipeline.
        # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.

        print(messages)
        print(user_message)

        # 프롬프트
        prompt = ChatPromptTemplate([
            ("system", "You are a helpful AI bot. Your name is robot."),
            ("human", "Hello, how are you doing?"),
            ("ai", "I'm doing well, thanks!"),
            ("human", "{topic}"),
        ])

        # 체인 생성
        chain = prompt | self.llm

        # 간결성을 위해 응답은 터미널에 출력됩니다.
        response = chain.invoke(
            {"topic": user_message}
        )

        return response
