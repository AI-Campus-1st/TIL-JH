import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

iris = sns.load_dataset('iris')

st.title('1. matplotlib')

fig, ax = plt.subplots()
ax.scatter(iris['sepal_length'], iris['sepal_width'], c='blue', label='Sepal')
ax.set_xlabel('Sepal length')
ax.set_ylabel('Sepal width')
ax.set_title('Iris Sepal Dimensions')
ax.legend()

st.pyplot(fig)

st.title('2. seaborn')

fig, ax = plt.subplots()
sns.histplot(iris['petal_length'], bins=20, kde=True, ax=ax)
ax.set_title('Petal Length Distribution')

st.pyplot(fig)

fig, ax = plt.subplots()
sns.boxplot(x='species', y='petal_length', data=iris, ax=ax)
ax.set_title('Petal Length by Species')

st.pyplot(fig)


import plotly.express as px

st.title('3. plotly')

fig = px.scatter(
    iris,
    x='sepal_length',
    y='sepal_width',
    color='species',
    title='Interactive Iris Sepal Scatter Plot'
)
st.plotly_chart(fig)

fig = px.line(
    iris,
    x='sepal_length',
    y='sepal_width',
    color='species',
    title='Interactive Iris Sepal Line Chart'
)
st.plotly_chart(fig)