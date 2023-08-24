import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain ,LLMChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)




def initialize_session(ref):
    link = f"https://albertsav.com/albertBrain/{ref}"
    st.write(link)
    loader = WebBaseLoader(link)
    data = loader.load()
    source = data[0].page_content.replace('\xa0', '\n')
    a_template = f"""Your role is to serve as a virtual receptionist, strictly adhering to all established guidelines. \
The SOURRCE provided to you corresponds to a unique apartment with its specific details. \
You are identified as "Albert," and your responsibility is to maintain your role as a professional receptionist, \
akin to that of a luxury hotel, during our conversations. \
Your task is to respond to my requests using the information from the given SOURCE. \
If an answer to a question is not found within the information from the given SOURCE, you should state \
"I don't have that information" and cease further responses. \
You must refrain from answering any question that does not pertain to the data present in the SOURCE. \
Your responses should be in English, but if requested, you may switch languages while maintaining a friendly and warm tone. \
Be careful not to make errors or provide inaccurate information from any other sources when presenting data.

SOURCE:
{source}
"""
    #st.write(a_template)
    system_message_prompt = SystemMessagePromptTemplate.from_template(a_template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)


    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key="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" , #st.secrets["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"],
        model_name="gpt-3.5-turbo",
    )
    st.session_state.conversation = LLMChain(
        llm=llm,
        prompt=chat_prompt,
        #memory=ConversationSummaryMemory(llm=llm),

    )





# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#input_num=''
#initialize_session(input_num)
input_num=st.text_input('Enter refrence number')
click=st.button('Update Source'  )
if click:
    st.session_state.clear()
    initialize_session(input_num)

#openai_api_key=st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assisttant", "content": "How can I help you?"}]
    # st.session_state["messages"] = "How can I help you?"

for msg in st.session_state.messages:
    #st.write(msg)
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    openai.api_key = st.secrets["open_api_key"]
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response1 = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # st.write(response1)
    #st.write(st.session_state.messages)
    response = st.session_state.conversation.run(prompt)
    #st.write(response)
    tem_hist= {"role":"assisttant", "content": response}
    #msg = tem_hist#response#.choices[0].message
    #st.write(tem_hist)
    st.session_state.messages.append({"role": "assistant", "content": tem_hist["content"]})
    st.chat_message("assistant").write(tem_hist["content"])
