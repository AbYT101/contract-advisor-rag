from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def generate(question, retriever):
    llm = ChatOpenAI(temperature=0.0, model='gpt-4o')
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    response = qa_chain.run(question)
    return response
