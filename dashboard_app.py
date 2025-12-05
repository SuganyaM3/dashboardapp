import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Define a function to load the data from `/content/Sales_Analysis_Report.xlsx`
@st.cache_data
def load_data():
    df = pd.read_excel('/content/Sales_Analysis_Report.xlsx')
    # Ensure 'OrderDate' is in datetime format for time-series analysis
    if 'OrderDate' in df.columns:
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    return df

# 2. Set up the Streamlit page configuration
st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Sales Analysis Dashboard")

# Load the data
df = load_data()

# 3. Create a sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to",
    ("Overview", "Sales by Product", "Sales by Region", "Sales Over Time")
)

# 4. Implement the main content area based on the user's sidebar selection
if selection == "Overview":
    st.header("Data Overview")
    st.subheader("First 5 Rows of the Data")
    st.write(df.head())

    if st.button("Show Full Data Summary"):
        st.subheader("Full Data")
        st.write(df)
        st.subheader("Descriptive Statistics")
        st.write(df.describe(include='all'))

elif selection == "Sales by Product":
    st.header("Sales by Product")
    if 'Product' in df.columns and 'Total Price' in df.columns:
        sales_by_product = df.groupby('Product')['Total Price'].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(
            sales_by_product,
            x='Product',
            y='Total Price',
            title='Total Sales by Product',
            labels={'Total Price': 'Total Sales Amount', 'Product': 'Product Name'}
        )
        st.plotly_chart(fig)
    else:
        st.warning("Required columns 'Product' or 'Total Price' not found in data.")

elif selection == "Sales by Region":
    st.header("Sales by Region")
    if 'Region' in df.columns and 'Total Price' in df.columns:
        sales_by_region = df.groupby('Region')['Total Price'].sum().sort_values(ascending=False).reset_index()
        fig = px.pie(
            sales_by_region,
            values='Total Price',
            names='Region',
            title='Total Sales by Region',
            hole=0.3
        )
        st.plotly_chart(fig)
    else:
        st.warning("Required columns 'Region' or 'Total Price' not found in data.")

elif selection == "Sales Over Time":
    st.header("Sales Over Time")
    if 'OrderDate' in df.columns and 'Total Price' in df.columns:
        # Aggregate sales by month
        df['YearMonth'] = df['OrderDate'].dt.to_period('M').astype(str)
        sales_over_time = df.groupby('YearMonth')['Total Price'].sum().reset_index()
        sales_over_time['YearMonth'] = pd.to_datetime(sales_over_time['YearMonth'])
        sales_over_time = sales_over_time.sort_values('YearMonth')

        fig = px.line(
            sales_over_time,
            x='YearMonth',
            y='Total Price',
            title='Total Sales Over Time',
            labels={'Total Price': 'Total Sales Amount', 'YearMonth': 'Date'}
        )
        st.plotly_chart(fig)
    else:
        st.warning("Required columns 'OrderDate' or 'Total Price' not found in data.")

st.sidebar.markdown("Built with ❤️ by Your Name")
