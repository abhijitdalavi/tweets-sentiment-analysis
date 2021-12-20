import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Analyse du sentiment des tweets")
st.sidebar.title("Options de visualisation")

st.markdown("## Les différentes visualisations de l'analyse sentimentale des tweets de US Airlines 🐦 ")
st.sidebar.markdown(
    "Sentiment Analysis des Tweets 🐦 ")
    
data_path = ("Tweets.csv")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(data_path)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data


data = load_data()

random_tweet = st.sidebar.radio(
    'Selectionner un Sentiment', ('positive', 'negative', 'neutral'))


st.subheader("Les examples en se basant sur votre choix!")
st.markdown("1." + data.query("airline_sentiment == @random_tweet")
            [['text']].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Nombre de Tweets")
select = st.sidebar.selectbox('Type de visualisation', ['Histogram', 'PieChart'])

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame(
    {'Sentiments': sentiment_count.index, 'Tweets': sentiment_count.values})

# Nombre des tweets par sentiment
if st.sidebar.checkbox('Afficher', False, key='0'):
    st.markdown("### Nombre des tweets par sentiment")
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x='Sentiments',
                     y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiments')
        st.plotly_chart(fig)

# Distibution Geographique des Tweets par rapport au temps différents
st.sidebar.subheader("Distibution Geographique des Tweets par rapport au temps différents")
hour = st.sidebar.slider("Heure", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if st.sidebar.checkbox('Afficher', False, key='1'):
    st.markdown('## Localisation des Tweets en se basant sur les temps de jour')
    st.markdown('%i tweets in %i:00 and %i:00' %
                (len(modified_data), hour, (hour+1) % 24))
    st.map(modified_data)
    st.sidebar.subheader("Afficher un exemple de données")    
    if st.sidebar.checkbox("Afficher", False):
        st.write(modified_data)

# Répartition des Tweets des compagnies aériennes par les sentiments
st.sidebar.subheader("Répartition des Tweets des compagnies aériennes par les sentiments")
st.markdown("## Répartition des Tweets des compagnies aériennes par les sentiments")
choice = st.sidebar.multiselect(
    "Choisir les Compagnies aériennes", tuple(pd.unique(data["airline"])))
if st.sidebar.checkbox("Afficher", False, key="5"):
    if len(choice) > 0:
        chosen_data = data[data["airline"].isin(choice)]
        fig = px.histogram(chosen_data, x="airline", y="airline_sentiment",
                           histfunc="count", color="airline_sentiment",
                           facet_col="airline_sentiment", labels={"airline_sentiment": "sentiment"})
        st.plotly_chart(fig)

# Nuage des mots
st.sidebar.subheader("Nuage des mots")
word_sentiment = st.sidebar.radio(
    "Quel sentiment voulez-vous afficher?", tuple(pd.unique(data["airline_sentiment"])))
if st.sidebar.checkbox("Afficher", False, key="6"):
    st.subheader(f"Word Cloud for {word_sentiment.capitalize()} Sentiment")
    df = data[data["airline_sentiment"] == word_sentiment]
    words = " ".join(df["text"])
    processed_words = " ".join([word for word in words.split(
    ) if "http" not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white",
                          width=800, height=640).generate(processed_words)
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(fig)
