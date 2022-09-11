import streamlit as st
import numpy as np
import pandas as pd
import get_dict as gd

japan = gd.get_dict()
#st.write(japan["東京都"])

st.title('戸建て賃貸需要供給調査ツール')

df = pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40]
})

dict = {'東京都':['練馬区', '大泉町'],
       '神奈川県':['平塚市']}

col1, col2, col3 = st.columns(3)

with col1:
    ken = st.selectbox(
        '都道府県を選択ください',
        #('sanomaru', 'ityan', 'utamaru')
        #tuple(dict.keys())
        tuple(japan.keys())
    )

with col2:
    city = st.selectbox(
        '市区町村を選択してください',
        #('sanomaru2', 'ityan2')
        #tuple(dict[ken])
        tuple(japan[ken])
    )
    #st.write('city: ', city)

with col3:
    if st.button('GO!'):
        st.write('your choice : ', ken, city)
    else:
        st.write('push start')

