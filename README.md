# Pricing_Analysis
# 📊 Pricing Strategy Analysis

A Streamlit-based interactive web app to analyze product pricing, demand, revenue, elasticity, discount strategies, and competitor pricing — all without touching any code.

---

## 🚀 Features

- 📁 **Upload your own CSV or Excel file** — no hardcoded data
- 🔗 **Auto column detection** — maps Price and Units columns automatically
- 🔍 **Category filter** — segment analysis by product, region, etc.
- 📈 **Revenue optimization** — finds the price point with maximum revenue
- 🔢 **Elasticity analysis** — identifies high/low customer price sensitivity
- 🏷️ **Interactive discount simulator** — adjust discount % and demand boost in real time
- 🏢 **Competitor pricing comparison** — model competitor markup dynamically
- ⬇️ **Download results** — export full analysis as CSV

---

## 🗂️ Project Structure

```
pricing-analysis/
│
├── pricing_analysis.py       # Main Streamlit app
├── sample_pricing_data.csv   # Sample data to test the app
└── README.md                 # Project documentation
```

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone https://github.com/shreshthapurohit/pricing-analysis.git
cd pricing-analysis
```

### 2. Install dependencies

```bash
pip install streamlit pandas matplotlib openpyxl
```

### 3. Run the app

```bash
streamlit run pricing_analysis.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📄 Input File Format

Your CSV or Excel file must contain at least two columns:

| Price | Units_Sold |
|-------|------------|
| 10    | 150        |
| 20    | 110        |
| 30    | 75         |

**Supported column name variations:**

| Column     | Accepted Names                          |
|------------|-----------------------------------------|
| Price      | `price`, `rate`, `cost`                 |
| Units Sold | `units`, `qty`, `quantity`, `sold`, `demand`, `sales` |

> If your column names are different, you can manually select them from the sidebar dropdowns.

**Supported file types:** `.csv`, `.xlsx`, `.xls`

---

## 🧪 Testing with Sample Data

A ready-to-use sample file `sample_pricing_data.csv` is included.

1. Run the app
2. Click **Browse files** in the sidebar
3. Upload `sample_pricing_data.csv`
4. Explore all charts and insights instantly

---

## 📊 Analysis Modules

### 1. Price vs Demand
Scatter plot showing how demand drops as price increases, with the optimal price point highlighted in red.

### 2. Revenue Insights
Identifies the price that generates maximum revenue using the formula:
```
Revenue = Price × Units Sold
```

### 3. Elasticity Analysis
Calculates price elasticity of demand:
```
Elasticity = % Change in Demand / % Change in Price
```
- **Elasticity > 1** → Customers are highly sensitive (elastic)
- **Elasticity < 1** → Customers are less sensitive (inelastic)

### 4. Discount Strategy
Simulates the revenue impact of applying a discount:
```
New Revenue = (Price × Discount%) × (Units Sold × Demand Boost%)
```
Adjust both sliders in real time to find the best discount scenario.

### 5. Competitor Comparison
Models competitor pricing by applying a markup percentage to your prices, plotted side-by-side.

---

## 📥 Download Results

After analysis, click **Download Analysis as CSV** to export a full table including:
- Original price and units
- Revenue
- Elasticity
- Discounted price and new revenue
- Competitor price

---

## 🛠️ Dependencies

| Package      | Purpose                        |
|--------------|--------------------------------|
| streamlit    | Web app framework              |
| pandas       | Data manipulation              |
| matplotlib   | Charts and graphs              |
| openpyxl     | Excel file support (.xlsx)     |

Install all at once:
```bash
pip install streamlit pandas matplotlib openpyxl
```

---

## 🙋 FAQ

**Q: My columns have different names — will it work?**  
A: Yes. Use the sidebar dropdowns to manually map your columns to Price and Units Sold.

**Q: Can I filter data by product category?**  
A: Yes. Enable the "Filter by category column" checkbox in the sidebar and select your category column and value.

**Q: Can I upload multiple files?**  
A: One file at a time. Filter by category to analyze different segments within the same file.

---

## 📌 Author

Built as a pricing strategy analysis tool for product and business analytics.  
Feel free to fork, extend, and customize.
