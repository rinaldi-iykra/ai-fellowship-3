from dotenv import load_dotenv
import os
import streamlit as st 
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib

matplotlib.use('TkAgg')

load_dotenv()  # Load environment variables from .env file if you have one
API_KEY = os.environ.get('PANDASAI_API_KEY')

if API_KEY is None:
    st.error("API key is not set. Please set the PANDASAI_API_KEY environment variable.")
else:
    # Create an LLM by instantiating OpenAI object, and passing API token
    llm = OpenAI(api_token=API_KEY)

    #Title
    st.title('AI Assistant for Procurement Team 🤖')
    
    #Welcoming message
    st.write("Hello, 👋 I am your AI Assistant and I am here to help you with the supplier that you need.")

    #Explanation sidebar
    with st.sidebar:
        st.write('**Your Supplier Search Begins here.**')
        st.caption('''**The exciting supplier journey starts with a dataset. That's why I'd love for you to upload a CSV file.**''')
        st.caption('''**Then, we'll work together to shape your business challenge.**''')
        st.divider()
        st.caption("<p style ='text-align:center'> made with ❤️ by Group 3</p>",unsafe_allow_html=True )
        st.caption("<p style ='text-align:center'> IYKRA AI Engineer Fellowship</p>",unsafe_allow_html=True )
    
    #Initialise the key in session state
    if 'clicked' not in st.session_state:
        st.session_state.clicked ={1:False}

    #Function to udpate the value in session state
    def clicked(button):
        st.session_state.clicked[button]= True
    st.button("Let's get started", on_click = clicked, args=[1])
    if st.session_state.clicked[1]:
        uploaded_file = st.file_uploader("Upload your file here", type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df.head(3))  # Display the first few rows of the dataframe
            
            st.write("Got burning questions about your supplier problem or need help navigating the intricacies of your need? You're in the right place! Our chatbot is geared up to assist you with insights, advice, and solutions. Just type in your queries, and let's unravel the mysteries of your supplier together! 🔍💻")

            if df.empty:
                st.warning("The uploaded CSV file is empty.")
            else:
                prompt = st.text_area("State Your Curiosity, Please...")
                
                # Generate output
                if st.button("Reveal It"):
                    if prompt:
                        # Create SmartDataframe object
                        smart_df = SmartDataframe(df, llm)
                        with st.spinner("Thinking..."):
                            st.write(smart_df.chat(prompt))
                    else:
                        st.warning("Please enter a prompt.Please enter a prompt.")