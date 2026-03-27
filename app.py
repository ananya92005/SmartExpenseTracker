import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import joblib
import streamlit.components.v1 as components

# Set page config
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰", layout="wide")

# Custom CSS and JS for better look and interactivity
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stApp {
        background: transparent;
    }
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 16px;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Custom JS for interactivity
components.html("""
<script>
    function showAlert(message) {
        alert(message);
    }
</script>
""", height=0)

# Database setup
def create_table():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, amount REAL, category TEXT, date TEXT, description TEXT)''')
    conn.commit()
    conn.close()

create_table()

# Functions
def add_expense(amount, category, date, desc):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)", (amount, category, date, desc))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

# Streamlit App
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title("💰 Smart Expense Tracker")
st.markdown("### Track your expenses intelligently with AI-powered insights!")
st.markdown('</div>', unsafe_allow_html=True)

menu = st.sidebar.selectbox("📋 Menu", ["➕ Add Expense", "👀 View Expenses", "📊 Analysis", "🤖 AI Insights"])

if menu == "➕ Add Expense":
    st.header("➕ Add Daily Expense")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("💵 Amount ($)", min_value=0.0, step=0.01)
        category = st.selectbox("📂 Category", ["🍔 Food", "✈️ Travel", "🛍️ Shopping", "🎬 Entertainment", "💡 Bills", "🔧 Other"])
    with col2:
        date = st.date_input("📅 Date")
        desc = st.text_input("📝 Description")
    if st.button("✅ Add Expense"):
        add_expense(amount, category, str(date), desc)
        st.success("✅ Expense added successfully!")
        st.balloons()
        # Custom JS alert
        components.html('<script>showAlert("Expense added!");</script>', height=0)

elif menu == "👀 View Expenses":
    st.header("👀 All Expenses")
    df = get_expenses()
    if not df.empty:
        st.dataframe(df.style.format({"amount": "${:.2f}"}))
        csv = df.to_csv(index=False)
        st.download_button("📥 Download as CSV", csv, "expenses.csv", mime="text/csv")
    else:
        st.info("📝 No expenses recorded yet. Add some expenses to get started!")

elif menu == "📊 Analysis":
    st.header("📊 Expense Analysis")
    df = get_expenses()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        category_sum = df.groupby('category')['amount'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Category-wise Expenses")
            fig = px.pie(values=category_sum.values, names=category_sum.index, title="Spending by Category")
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("📊 Monthly Trends")
            monthly_sum = df.groupby('month')['amount'].sum()
            fig2 = px.line(x=monthly_sum.index.astype(str), y=monthly_sum.values, title="Monthly Expenses")
            st.plotly_chart(fig2)
        
        st.subheader("💰 Summary")
        total_expenses = df['amount'].sum()
        avg_monthly = monthly_sum.mean()
        col1, col2 = st.columns(2)
        with col1:
            components.html(f"""
            <div class="metric-card">
                <h3>Total Expenses</h3>
                <h2>${total_expenses:.2f}</h2>
            </div>
            """, height=100)
        with col2:
            components.html(f"""
            <div class="metric-card">
                <h3>Average Monthly</h3>
                <h2>${avg_monthly:.2f}</h2>
            </div>
            """, height=100)
    else:
        st.info("📊 No data available for analysis. Add some expenses first!")

elif menu == "🤖 AI Insights":
    st.header("🤖 AI-Powered Insights")
    df = get_expenses()
    if len(df) > 5:  # need some data
        df['date'] = pd.to_datetime(df['date'])
        df['cat_code'] = df['category'].astype('category').cat.codes
        
        # Pattern detection with clustering
        st.subheader("🔍 Spending Patterns")
        kmeans = KMeans(n_clusters=min(3, len(df)), random_state=42)
        df['cluster'] = kmeans.fit_predict(df[['amount', 'cat_code']])
        cluster_summary = df.groupby('cluster')['category'].agg(lambda x: x.mode()[0]).reset_index()
        cluster_summary['avg_amount'] = df.groupby('cluster')['amount'].mean()
        for _, row in cluster_summary.iterrows():
            st.write(f"**Cluster {int(row['cluster'])}:** High spending in {row['category']} (Avg: ${row['avg_amount']:.2f})")
        
        # Monthly prediction
        df['month'] = df['date'].dt.to_period('M')
        monthly_totals = df.groupby('month')['amount'].sum().reset_index()
        monthly_totals['month_num'] = (monthly_totals['month'] - monthly_totals['month'].min()).apply(lambda x: x.n)
        if len(monthly_totals) > 1:
            X = monthly_totals[['month_num']]
            y = monthly_totals['amount']
            model = LinearRegression()
            model.fit(X, y)
            next_month = monthly_totals['month_num'].max() + 1
            pred = model.predict([[next_month]])[0]
            st.subheader("🔮 Monthly Expense Prediction")
            st.metric("Predicted Next Month", f"${pred:.2f}")
            
            # Prediction chart
            future_months = pd.DataFrame({'month_num': list(monthly_totals['month_num']) + [next_month], 'amount': list(monthly_totals['amount']) + [pred]})
            fig = px.line(future_months, x='month_num', y='amount', title="Expense Trend & Prediction")
            st.plotly_chart(fig)
        
        # Savings suggestions
        st.subheader("💡 Savings Suggestions")
        avg_monthly = monthly_totals['amount'].mean()
        top_category = df.groupby('category')['amount'].sum().idxmax()
        st.write(f"💰 Your average monthly spending is **${avg_monthly:.2f}**")
        st.write(f"🎯 Consider reducing expenses in **{top_category}** to save more.")
        st.write("📋 Tip: Aim to keep monthly expenses below 80% of average for better savings!")
    else:
        st.info("🤖 Need more expense data for AI insights. Add at least 5 expenses to unlock predictions!")

# Custom Footer
st.markdown("---")
components.html("""
<div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.8); border-radius: 10px; margin-top: 20px;">
    <p>Built with ❤️ using Streamlit, HTML, CSS & JS</p>
    <p>Smart Expense Tracker - Your AI Finance Companion</p>
</div>
""", height=100)