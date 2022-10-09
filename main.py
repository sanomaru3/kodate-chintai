from operator import truediv
import streamlit as st
import numpy as np
import pandas as pd
import get_dict as gd
import get_result_dic_list as gr
import base64

show_flg = False

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
    

with col3:
    if st.button('GO!'):
        #st.write('your choice : ', ken, city)
        show_flg = True
#    else:
#        st.write('push start')

if(show_flg):
    input_dict = []
    input_dict.append({
            'prefecture':ken,
            'city':city    
    })

    result_dic_list = gr.get_result_dict_list(input_dict)

    df = pd.DataFrame(result_dic_list)

    #st.write(df)

    st.dataframe(df)


    #st.write('city: ', city)

    # CSVのダウンロードリンクを生成
    csv = df.to_csv(index=False)  

    # utf-8(BOM)
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="result_utf-8-sig.csv">Download Link</a>'
    st.markdown(f"CSVファイルのダウンロード(utf-8 BOM):  {href}", unsafe_allow_html=True)