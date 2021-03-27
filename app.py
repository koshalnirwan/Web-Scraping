import pandas as pd
from bs4 import BeautifulSoup
import requests
import pickle
import streamlit as st

html = """
<div style='background-color:tomato;padding:10px'>
<h2 style='color:white;text-align:center;'><b>FETCHING RESULT</b> </h2>
</div>
"""
st.markdown(html, unsafe_allow_html=True)
st.subheader('    ') 

pickle_out = open("col.pickle","rb")
col = pickle.load(pickle_out)
pickle_out.close()

columns2 = col.copy() 
del columns2[-2:]

df = pd.DataFrame(columns=columns2)

st.markdown("""<h4 style='color:green;'><i>Enter URL</i></h4>""", unsafe_allow_html=True)
user_url = st.text_input('')

st.markdown("""<h4 style='color:green;'><i>Enter First Roll Number</i></h4>""", unsafe_allow_html=True)
frno = st.number_input('', min_value=10, max_value=100000) 

st.markdown("""<h4 style='color:green;'><i>Enter Last Roll Number</i></h4>""", unsafe_allow_html=True)
srno = st.number_input(' ', min_value=10, max_value=100000) 

url = []
for i in range(frno,srno+1):
    #url2=user_url+str(i)+"&submit=Submit"
    url.append(user_url+str(i)+"&submit=Submit") 

#df.to_csv('Result.csv')
st.subheader(' ')
button = st.button('Create File')
if button:
    st.markdown("""<h5 style='color:red;'><i>PLEASE WAIT THIS MAY TAKE FEW MINUTES.....</i></h5>""", unsafe_allow_html=True)

    dn=[]
    name=[]
    roll_no=[]
    Result=[]
    for ur in url:
        df2=pd.DataFrame(columns=columns2)
        res = requests.get(ur)
        soup = BeautifulSoup(res.text,'html.parser')
        name.append(soup.find('td',{'class':'c3'}).text)
        roll_no.append(ur[-19:-14])
        result = [i.text for i in soup.select('div > b > span')]
        Result.append(result[0])
        n = soup.find('table',{'class':'enf'})
        headers = [tr.text for tr in n.select("tr td")]  
        for subject in (9,18,27,36,45,72,81,90):                       #(17,26,35,44,53,80,89,98)     values
            df2[headers[subject]] = [headers[subject+8]]
        dn.append(df2)
        df = pd.concat(dn,axis=0,sort=False)

    df.insert(0,'Name',name)
    df.insert(1,'Roll No',roll_no) 
    df.insert(18,'Result',Result)
    
    df.to_excel('Result.xlsx')
    st.markdown("""<h2 style='color:green;'><b>DONE !!</b></h2>""", unsafe_allow_html=True)
 

   
    

