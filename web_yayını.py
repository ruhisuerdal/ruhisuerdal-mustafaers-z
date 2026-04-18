import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd




st.set_page_config(    
    page_title='ruhisuerdal-mustafaersöz',
    page_icon=None,
    layout='wide',
    initial_sidebar_state='expanded'
    )


@st.cache_data 
def load_data():
    return pd.read_excel('bkm.xlsx') 
df=load_data()




st.sidebar.title('ruhisuerdal-mustafaersöz_proje')  

with st.sidebar.expander('Filtreler', expanded=False):
    yayınevi_listesi = ['Tümü'] + sorted(df['Yayınevi'].unique().tolist())
    secilen_yayinevi = st.selectbox('Yayınevi', yayınevi_listesi)
    
    if secilen_yayinevi != 'Tümü':
        df_filtered = df[df['Yayınevi'] == secilen_yayinevi]
    else:
        df_filtered = df
    
    
    yazar_listesi = ['Tümü'] + sorted(df_filtered['Yazar-ismi'].unique().tolist())
    secilen_yazar = st.selectbox('Yazar', yazar_listesi)
    
    if secilen_yazar != 'Tümü':
        df_filtered = df_filtered[df_filtered['Yazar-ismi'] == secilen_yazar]
    
    
    kitap_listesi = ['Tümü'] + sorted(df_filtered['Kitap-İsmi'].unique().tolist())
    secilen_kitap = st.selectbox('Kitap', kitap_listesi)
    
    if secilen_kitap != 'Tümü':
        df_filtered = df_filtered[df_filtered['Kitap-İsmi'] == secilen_kitap]


 

st.title('BKM VERİ ANALİZİ')
st.caption('Veri analizi uygulaması')
st.info('BİLGİ KUTUM')


col1, col2, col3, col4, col5 = st.columns(5) 



col1.metric('Toplam Kitap', len(df_filtered))
col2.metric('Ortalama Puan', round(df_filtered['Rating'].mean(), 2))
col3.metric("Ortalama Fiyat", f"{round(df_filtered['Fiyat'].mean(), 2)} TL")
col4.metric('Yazar Sayısı', df_filtered['Yazar-ismi'].nunique())
col5.metric('Yayınevi Sayısı', df_filtered['Yayınevi'].nunique())


st.divider()


tab1, tab2, tab3 = st.tabs(["VERİ", "GRAFİKLER", 'FORM'])

                            

                            
with tab1:
    st.subheader('Filtrelenmiş Veri Tablosu')
    st.dataframe(df_filtered, use_container_width=True)


with tab2:
    st.subheader('Analiz Grafikleri')
    chart_type = st.selectbox('Grafik türü seç:', ['Puan vs Fiyat (Dağılım)', 'Fiyat Dağılımı (Histogram)', 'Yayınevi Kitap Sayısı'])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if chart_type == 'Puan vs Fiyat (Dağılım)':
        sns.scatterplot(data=df_filtered, x='Rating', y='Fiyat', ax=ax)
    elif chart_type == 'Fiyat Dağılımı (Histogram)':
        sns.histplot(data=df_filtered, x='Fiyat', kde=True, ax=ax)
    elif chart_type == 'Yayınevi Kitap Sayısı':
        sns.countplot(data=df_filtered, y='Yayınevi', ax=ax)
        
    st.pyplot(fig)

with tab3:
    st.subheader('Geri Bildirim Formu')
    with st.form("my_form"):
        ad = st.text_input("Adın Soyadın")
        öneri = st.text_area("Önerin nedir?")
        if st.form_submit_button("Gönder"):
            st.success(f"Teşekkürler {ad}, önerin kaydedildi!")
            