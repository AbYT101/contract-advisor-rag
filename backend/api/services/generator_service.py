from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def generate(question, context):
    llm = ChatOpenAI(temperature=0.0, model='gpt-3.5-turbo-instruct')
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=context
    )
    response = qa_chain.run(question)
    return response
