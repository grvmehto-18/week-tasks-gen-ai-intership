"""
Chatbot Service
This module orchestrates the chatbot's functionality, including question answering.
"""
import os
import pandas as pd
from typing import Dict

from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from src.llm_config.llm_config import get_llm, get_embeddings
from src.vectorstore.vectorstore_service import create_vector_store


class ChatbotService:
    """
    Service for the LangChain chatbot.
    Handles document loading, vector store creation, and question answering.
    """

    def __init__(self, dataframe: pd.DataFrame, openai_api_key: str, model_name: str, base_url: str = None):
        """
        Initializes the ChatbotService.

        Args:
            dataframe (pd.DataFrame): The DataFrame to be used as a knowledge base.
            openai_api_key (str): The OpenAI API key.
            model_name (str): The name of the model to use.
            base_url (str, optional): The base URL for the API. Defaults to None.
        """
        if not openai_api_key:
            raise ValueError("OpenAI API key is required for the chatbot service.")
        
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.dataframe = dataframe
        self.model_name = model_name
        self.base_url = base_url
        self.qa_chain = self._create_qa_chain()

    def _create_qa_chain(self):
        """
        Creates the RetrievalQA chain.

        Returns:
            A RetrievalQA chain instance.
        """
        # print("Creating chatbot QA chain...")

        embeddings = get_embeddings(base_url=self.base_url)
        vector_store = create_vector_store(self.dataframe, embeddings)
        retriever = vector_store.as_retriever(search_kwargs={'k': 2})
        llm = get_llm(model_name=self.model_name, base_url=self.base_url)

        system_prompt = (
            "Use the given context to answer the question. "
            "If you don't know the answer, say you don't know. "
            "Use three sentence maximum and keep the answer concise. "
            "Context: {context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        qa = create_retrieval_chain(retriever, question_answer_chain)

        # print("Chatbot QA chain created successfully.")
        return qa

    def ask_question(self, query: str) -> Dict:
        """
        Asks a question to the chatbot.

        Args:
            query (str): The question to ask.

        Returns:
            Dict: The response from the QA chain.
        """
        # print(f"Asking question: {query}")
        response = self.qa_chain.invoke({"input": query})
        # Remove the special token if it exists
        if "answer" in response and isinstance(response["answer"], str):
            response["answer"] = response["answer"].strip()
        return response
