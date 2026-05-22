import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Pricing Strategy Analysis", layout="wide")
st.title("📊 Pricing Strategy Analysis")
st.write("Upload your sales data or use the built-in sample to analyze price, demand, revenue, and elasticity.")

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.sidebar.header("📁 Data Input")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="File must have at least a Price column and a Units/Quantity column."
)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

SAMPLE_DATA = {
    "Price": [10, 15, 20, 25, 30, 35, 40],
    "Units_Sold": [100, 90, 80, 60, 50, 30, 20]
}

if uploaded_file is not None:
    try:
        raw_df = load_data(uploaded_file)
        st.sidebar.success(f"✅ Loaded: **{uploaded_file.name}**  \n{len(raw_df)} rows × {len(raw_df.columns)} columns")
    except Exception as e:
        st.sidebar.error(f"❌ Could not read file: {e}")
        raw_df = pd.DataFrame(SAMPLE_DATA)
        st.sidebar.info("Using sample data instead.")
else:
    raw_df = pd.DataFrame(SAMPLE_DATA)
    st.sidebar.info("ℹ️ No file uploaded. Using built-in sample data.")

# -------------------------------
# COLUMN MAPPING
# -------------------------------
st.sidebar.header("🔗 Column Mapping")

all_cols = raw_df.columns.tolist()

# Try to auto-detect price and units columns
def guess_col(cols, keywords):
    for col in cols:
        if any(k in col.lower() for k in keywords):
            return col
    return cols[0]

default_price = guess_col(all_cols, ["price", "rate", "cost"])
default_units = guess_col(all_cols, ["unit", "qty", "quantity", "sold", "demand", "sales"])

price_col = st.sidebar.selectbox("Price Column", all_cols, index=all_cols.index(default_price))
units_col = st.sidebar.selectbox("Units Sold Column", all_cols, index=all_cols.index(default_units))

# Optional: filter by a category column
cat_cols = [c for c in all_cols if c not in [price_col, units_col]]
use_filter = st.sidebar.checkbox("Filter by a category column", value=False)
if use_filter and cat_cols:
    cat_col = st.sidebar.selectbox("Category Column", cat_cols)
    cat_values = raw_df[cat_col].dropna().unique().tolist()
    selected_cat = st.sidebar.selectbox(f"Select {cat_col}", cat_values)
    raw_df = raw_df[raw_df[cat_col] == selected_cat]

# Build working dataframe
try:
    df = raw_df[[price_col, units_col]].dropna().copy()
    df.columns = ["Price", "Units_Sold"]
    df = df.sort_values("Price").reset_index(drop=True)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Units_Sold"] = pd.to_numeric(df["Units_Sold"], errors="coerce")
    df = df.dropna()
except Exception as e:
    st.error(f"Column error: {e}")
    st.stop()

# -------------------------------
# REVENUE CALCULATION
# -------------------------------
df["Revenue"] = df["Price"] * df["Units_Sold"]
optimal = df.loc[df["Revenue"].idxmax()]

# ================================
# LAYOUT: Two columns at the top
# ================================
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Dataset")
    st.dataframe(df, use_container_width=True)

    st.subheader("💡 Revenue Insights")
    st.metric("Optimal Price", f"₹ {optimal['Price']:,.2f}")
    st.metric("Maximum Revenue", f"₹ {optimal['Revenue']:,.2f}")
    st.metric("Units at Optimal Price", f"{int(optimal['Units_Sold'])}")

with col2:
    st.subheader("📈 Price vs Demand")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(df["Price"], df["Units_Sold"], label="All Data", zorder=3)
    ax.scatter(optimal["Price"], optimal["Units_Sold"],
               color='red', s=200, label="Optimal Price", zorder=4)
    ax.annotate(
        f"Best: {optimal['Price']}",
        (optimal["Price"], optimal["Units_Sold"]),
        textcoords="offset points", xytext=(0, 12), ha='center',
        fontsize=9, color='red'
    )
    ax.set_xlabel("Price")
    ax.set_ylabel("Units Sold")
    ax.set_title("Optimal Pricing Point")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    st.pyplot(fig)

# -------------------------------
# ELASTICITY ANALYSIS
# -------------------------------
st.divider()
st.subheader("🔢 Elasticity Analysis")

df["Price_Change"] = df["Price"].pct_change()
df["Demand_Change"] = df["Units_Sold"].pct_change()
df["Elasticity"] = df["Demand_Change"] / df["Price_Change"]

ecol1, ecol2 = st.columns(2)

with ecol1:
    st.dataframe(df[["Price", "Units_Sold", "Elasticity"]].round(3), use_container_width=True)

with ecol2:
    st.subheader("Customer Sensitivity Insights")
    for i in range(1, len(df)):
        row = df.iloc[i]
        e = abs(row["Elasticity"])
        if pd.isna(e):
            continue
        if e > 1:
            st.write(f"💸 At price **{row['Price']}** → 🔴 HIGH sensitivity (elastic)")
        else:
            st.write(f"💰 At price **{row['Price']}** → 🟢 LOW sensitivity (inelastic)")

# -------------------------------
# DISCOUNT STRATEGY
# -------------------------------
st.divider()
st.subheader("🏷️ Discount Strategy")

discount_pct = st.slider("Select Discount %", min_value=1, max_value=50, value=10, step=1)
demand_boost_pct = st.slider("Expected Demand Boost %", min_value=1, max_value=100, value=20, step=1)

df["Discounted_Price"] = df["Price"] * (1 - discount_pct / 100)
df["New_Revenue"] = df["Discounted_Price"] * (df["Units_Sold"] * (1 + demand_boost_pct / 100))

dcol1, dcol2 = st.columns(2)

with dcol1:
    st.dataframe(
        df[["Price", "Discounted_Price", "Revenue", "New_Revenue"]].round(2),
        use_container_width=True
    )

with dcol2:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(df["Price"], df["Revenue"], marker='o', label="Original Revenue")
    ax2.plot(df["Price"], df["New_Revenue"], marker='s', linestyle='--', label=f"After {discount_pct}% Discount")
    ax2.set_xlabel("Price")
    ax2.set_ylabel("Revenue")
    ax2.set_title("Revenue Impact of Discount")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.4)
    st.pyplot(fig2)

# -------------------------------
# COMPETITOR ANALYSIS
# -------------------------------
st.divider()
st.subheader("🏢 Competitor Price Comparison")

comp_markup = st.slider("Competitor Price Markup %", min_value=-50, max_value=100, value=10, step=1)
df["Competitor_Price"] = df["Price"] * (1 + comp_markup / 100)

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.plot(df.index, df["Price"], marker='o', label="Our Price")
ax3.plot(df.index, df["Competitor_Price"], marker='s', linestyle='--', label="Competitor Price")
ax3.set_xticks(df.index)
ax3.set_xticklabels([f"₹{p}" for p in df["Price"]], rotation=30)
ax3.set_title("Competitor Pricing Comparison")
ax3.set_ylabel("Price")
ax3.legend()
ax3.grid(True, linestyle='--', alpha=0.4)
st.pyplot(fig3)

# -------------------------------
# DOWNLOAD RESULTS
# -------------------------------
st.divider()
st.subheader("⬇️ Download Results")

output_df = df[["Price", "Units_Sold", "Revenue", "Elasticity", "Discounted_Price", "New_Revenue", "Competitor_Price"]].round(3)

csv_buffer = io.StringIO()
output_df.to_csv(csv_buffer, index=False)

st.download_button(
    label="📥 Download Analysis as CSV",
    data=csv_buffer.getvalue(),
    file_name="pricing_analysis_results.csv",
    mime="text/csv"
)

# -------------------------------
# CONCLUSION
# -------------------------------
st.success(
    f"✅ Analysis complete! Optimal price is **{optimal['Price']}** generating max revenue of **{optimal['Revenue']:,.0f}**. "
    f"Adjust the discount and competitor sliders in real-time to explore different scenarios."
)
