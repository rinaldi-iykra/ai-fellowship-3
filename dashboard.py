import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    layout="wide",
    page_title="Sales Dashboard",
    page_icon=":bar_chart:")
st.title("Vendor Dashboard")
st.markdown("_Testing_")

@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    return data

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info("Upload a file through config", icon="ℹ️")
    st.stop()

df = load_data(uploaded_file)

def plot_pie():
    fig = px.pie(
        df,
        names='Cluster',
        title="Number of Supplier in each Cluster"
    )
    st.plotly_chart(fig)

def plot_bar():
    fig = px.histogram(
        df,
        x="Supplier_Location",
        y="Average_Invoice_Value",
        color="Cluster_Name",
        histfunc = 'avg'
    )
    st.plotly_chart(fig)

def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_scatter():
    fig = px.scatter(
        df[["Loyalty_Score", "Freight_Cost_Per_Shipment", "Average_Invoice_Value", "Cluster_Name"]].groupby("Cluster_Name").mean().reset_index(),
        x="Loyalty_Score",
        y="Freight_Cost_Per_Shipment",
        size="Average_Invoice_Value",
        hover_name="Cluster_Name"
    )
    st.plotly_chart(fig)

top_left_column, top_right_column = st.columns((2, 1))
bottom_left_column, bottom_right_column = st.columns(2)

with top_left_column:
    column_1, column_2 = st.columns(2)

with column_1:
    plot_gauge(indicator_number=round(df['Risk_Score'].mean(), 2), indicator_color='#0068C9', indicator_suffix='', indicator_title='Risk Score', max_bound=df['Risk_Score'].max())
    plot_gauge(indicator_number=round(df['Compliance_Score'].mean(), 2), indicator_color='#0068C9', indicator_suffix='', indicator_title='Compliance Score', max_bound=df['Compliance_Score'].max())
with column_2:
    plot_gauge(indicator_number=round(df['Credit_Score'].mean(), 2), indicator_color='#0068C9', indicator_suffix='', indicator_title='Credit Score', max_bound=df['Credit_Score'].max())
    plot_gauge(indicator_number=round(df['Loyalty_Score'].mean(), 2), indicator_color='#0068C9', indicator_suffix='', indicator_title='Loyalty Score', max_bound=df['Loyalty_Score'].max())

with top_right_column:
    plot_bar()

with bottom_left_column:
    plot_scatter()

with bottom_right_column:
    with st.expander("Data Preview"):
        st.dataframe(df[['Supplier_Name', 'Overall_Performance_Score']])
