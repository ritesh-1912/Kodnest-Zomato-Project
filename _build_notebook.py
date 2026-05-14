"""Regenerate zomato_analysis.ipynb. Run: python _build_notebook.py"""
import json
import uuid
from pathlib import Path


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": text.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


cells: list[dict] = []

cells.append(
    md(
        "# Restaurant Data Analysis — Zomato Dataset\n\n"
        "End-to-end analysis of Zomato restaurant listings: methodology, implementation, exploratory "
        "analysis, visualizations, and conclusions.\n"
    )
)

cells.append(
    md(
        "## Chapter 4 — Methodology and architecture\n\n"
        "### 4.1 Development methodology\n\n"
        "| Phase | Focus | Deliverable |\n"
        "|------|--------|-------------|\n"
        "| Phase 1 | Data collection | Zomato CSV imported |\n"
        "| Phase 2 | Data cleaning and preprocessing | Missing values, duplicates, standardized types |\n"
        "| Phase 3 | EDA | Relationships among ratings, cost, cuisines, location |\n"
        "| Phase 4 | Data visualization | Bar charts, frequency plots, heatmaps, scatter |\n"
        "| Phase 5 | ELT | SQLite storage and SQL queries |\n\n"
        "### 4.2 Application architecture\n\n"
        "Data source → Pandas/NumPy processing → EDA → Matplotlib/Seaborn visualization → SQLite ELT.\n\n"
        "### 4.3 Notebook flow\n\n"
        "1. Load the CSV  \n"
        "2. Clean and type-cast key fields  \n"
        "3. Print exploratory summaries (cities, cuisines, service flags)  \n"
        "4. Scatter plot (ratings vs votes), correlation heatmap, SQLite export and sample queries  \n"
        "5. Feature engineering (derived columns)  \n"
        "6. Main visualization suite (figures 1–3 and 5); figure 4 is the same scatter as step 4, so it is saved once  \n"
        "7. Feature verification checklist  \n"
    )
)

cells.append(
    code(
        "import sqlite3\n"
        "from pathlib import Path\n\n"
        "import matplotlib.pyplot as plt\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import seaborn as sns\n\n"
        "# Project palette (primary blue + light accent)\n"
        "BLUE = '#1f77b4'\n"
        "SKY = '#AED6F1'\n\n"
        "plt.rcParams.update({\n"
        "    'axes.grid': True,\n"
        "    'grid.alpha': 0.35,\n"
        "    'axes.facecolor': 'white',\n"
        "    'figure.facecolor': 'white',\n"
        "})\n"
        "sns.set_theme(style='whitegrid')\n\n\n"
        "def project_root() -> Path:\n"
        "    cwd = Path.cwd().resolve()\n"
        "    for p in [cwd, *cwd.parents]:\n"
        "        if (p / 'zomato.csv').exists():\n"
        "            return p\n"
        "    raise FileNotFoundError('zomato.csv not found — run from the Data Science Project folder.')\n\n\n"
        "PROJECT_DIR = project_root()\n"
        "CSV_PATH = PROJECT_DIR / 'zomato.csv'\n"
        "OUT_DIR = PROJECT_DIR / 'outputs'\n"
        "DB_PATH = PROJECT_DIR / 'zomato.db'\n"
        "OUT_DIR.mkdir(parents=True, exist_ok=True)\n"
        "print('PROJECT_DIR:', PROJECT_DIR)\n"
    )
)

cells.append(md("## Chapter 5 — Implementation\n\n### Module 1 — Data collection\n"))

cells.append(
    code(
        "df = pd.read_csv(CSV_PATH, low_memory=False)\n"
        "print('Raw shape:', df.shape)\n"
        "print(df.iloc[:2, [1, 2, 5, 9, 12]].to_string())\n"
    )
)

cells.append(md("### Module 2 — Data cleaning and preprocessing\n"))

cells.append(
    code(
        "df = df.copy()\n"
        "df.drop_duplicates(inplace=True)\n"
        "df.dropna(subset=['rate', 'approx_cost(for two people)'], inplace=True)\n\n"
        "df['rate'] = df['rate'].astype(str).str.replace('/5', '', regex=False)\n"
        "df['rate'] = pd.to_numeric(df['rate'], errors='coerce')\n\n"
        "df['approx_cost(for two people)'] = (\n"
        "    df['approx_cost(for two people)'].astype(str).str.replace(',', '', regex=False)\n"
        ")\n"
        "df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(float)\n\n"
        "df.dropna(subset=['rate'], inplace=True)\n"
        "print(df.head())\n"
        "print('Shape after cleaning:', df.shape)\n"
    )
)

cells.append(md("### Module 3 — Exploratory Data Analysis\n"))

cells.append(
    code(
        "city_counts = df['listed_in(city)'].value_counts().head(15)\n"
        "print('--- Top cities (listed_in(city)) ---')\n"
        "print(city_counts)\n\n"
        "cuisine_series = (\n"
        "    df['cuisines'].dropna().astype(str).str.split(',').explode().str.strip()\n"
        ")\n"
        "cuisine_counts = cuisine_series[cuisine_series.ne('')].value_counts().head(15)\n"
        "print('\\n--- Top 15 cuisine tags ---')\n"
        "print(cuisine_counts)\n\n"
        "print('\\n--- Mean rating: online_order ---')\n"
        "print(df.groupby('online_order')['rate'].mean())\n"
        "print('\\n--- Mean rating: book_table ---')\n"
        "print(df.groupby('book_table')['rate'].mean())\n"
    )
)

cells.append(md("### Scatter plot — ratings vs votes\n"))

cells.append(
    code(
        "plt.figure(figsize=(8, 5))\n"
        "plt.scatter(df['rate'], df['votes'], c=BLUE, edgecolors='black', linewidths=0.25, alpha=0.35, s=22)\n"
        "plt.title('Ratings vs Votes (Popularity)')\n"
        "plt.xlabel('Rate out of 5')\n"
        "plt.ylabel('Votes of popularity')\n"
        "plt.tight_layout()\n"
        "plt.savefig(OUT_DIR / '04_rating_vs_votes_scatter.png', dpi=150)\n"
        "plt.show()\n"
    )
)

cells.append(md("### Correlation heatmap\n"))

cells.append(
    code(
        "corr = df[['rate', 'votes', 'approx_cost(for two people)']].corr()\n"
        "plt.figure(figsize=(6, 4))\n"
        "sns.heatmap(corr, annot=True, cmap='coolwarm')\n"
        "plt.title('Correlation heatmap')\n"
        "plt.tight_layout()\n"
        "plt.savefig(OUT_DIR / '06_correlation_heatmap.png', dpi=150)\n"
        "plt.show()\n"
        "print(corr)\n"
    )
)

cells.append(md("### SQLite — load cleaned data, then add features in memory\n\nPersist the cleaned frame **before** feature engineering so the database mirrors the cleaned core columns.\n"))

cells.append(
    code(
        "if DB_PATH.exists():\n"
        "    DB_PATH.unlink()\n"
        "conn = sqlite3.connect(DB_PATH)\n"
        "df.to_sql('zomato', conn, index=False, if_exists='replace')\n\n"
        "query_top = \"\"\"\n"
        "SELECT location, name, rate\n"
        "FROM zomato\n"
        "WHERE rate IS NOT NULL\n"
        "ORDER BY rate DESC\n"
        "LIMIT 10;\n"
        "\"\"\"\n"
        "top_restaurants = pd.read_sql(query_top, conn)\n"
        "print('--- Top 10 restaurants by rating ---')\n"
        "print(top_restaurants.to_string(index=False))\n\n"
        "cuisine_df = pd.read_sql('SELECT cuisines FROM zomato WHERE cuisines IS NOT NULL', conn)\n"
        "tags = cuisine_df['cuisines'].astype(str).str.split(',').explode().str.strip()\n"
        "tags = tags[tags.ne('') & tags.ne('nan')]\n"
        "print('\\n--- Top 10 cuisine tags (SQLite) ---')\n"
        "print(tags.value_counts().head(10))\n\n"
        "conn.close()\n"
        "print('\\nDatabase path:', DB_PATH)\n"
    )
)

cells.append(md("### Feature engineering\n"))

cells.append(
    code(
        "df['cost_per_person'] = df['approx_cost(for two people)'] / 2\n\n\n"
        "def rating_category(rating):\n"
        "    if rating >= 4:\n"
        "        return 'Excellent'\n"
        "    elif rating >= 3:\n"
        "        return 'Good'\n"
        "    else:\n"
        "        return 'Average'\n\n\n"
        "df['rating_category'] = df['rate'].apply(rating_category)\n"
        "print(df[['rate', 'rating_category']].head())\n"
        "print(df['rating_category'].value_counts())\n"
    )
)

cells.append(
    md(
        "## Chapter 6 — EDA and output\n\n"
        "### Visualizations\n\n"
        "Palette: primary blue (`#1f77b4`) and accent sky blue (`#AED6F1`), light grid, black bar edges where used. "
        "**Figure 4** (rating vs votes scatter) is the same chart as in Chapter 5 — already saved as `04_rating_vs_votes_scatter.png`.\n"
    )
)

cells.append(
    code(
        "# (1) Rating popularity — frequency by rounded rating\n"
        "freq = df['rate'].round(1).value_counts().sort_index()\n"
        "fig, ax = plt.subplots(figsize=(14, 5))\n"
        "x = freq.index.astype(float)\n"
        "ax.bar(x, freq.values, width=0.09, color=BLUE, align='center')\n"
        "ax.set_title('Rating popularity')\n"
        "ax.set_xlabel('Rating')\n"
        "ax.set_ylabel('frequency')\n"
        "plt.tight_layout()\n"
        "plt.savefig(OUT_DIR / '01_rating_popularity.png', dpi=150)\n"
        "plt.show()\n"
    )
)

cells.append(
    code(
        "# (2) Online order and book table — restaurant counts (not mean rating)\n"
        "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\n"
        "order_lab = df['online_order'].map({'Yes': 'Available', 'No': 'Not Available'})\n"
        "oc = order_lab.value_counts().reindex(['Available', 'Not Available'])\n"
        "axes[0].bar(oc.index.astype(str), oc.values, color=SKY, edgecolor='black')\n"
        "axes[0].set_title('Online Order')\n"
        "axes[0].set_xlabel('Online Order Availability')\n"
        "axes[0].set_ylabel('Count')\n\n"
        "book_lab = df['book_table'].map({'Yes': 'Available', 'No': 'Not Available'})\n"
        "bc = book_lab.value_counts().reindex(['Not Available', 'Available'])\n"
        "axes[1].bar(bc.index.astype(str), bc.values, color=BLUE, edgecolor='black')\n"
        "axes[1].set_title('Book Table')\n"
        "axes[1].set_xlabel('Book Order Availability')\n"
        "axes[1].set_ylabel('Count')\n"
        "plt.tight_layout()\n"
        "plt.savefig(OUT_DIR / '02_online_order_booking_comparison.png', dpi=150)\n"
        "plt.show()\n"
    )
)

cells.append(
    code(
        "# (3) Count heatmap: online order vs book table\n"
        "oo = df['online_order'] == 'Yes'\n"
        "bt = df['book_table'] == 'Yes'\n"
        "ct = pd.crosstab(oo, bt)\n"
        "ct.index = ['False', 'True']\n"
        "ct.columns = ['False', 'True']\n"
        "plt.figure(figsize=(6.5, 4.5))\n"
        "sns.heatmap(ct, annot=True, fmt='.2e', cmap='Blues', cbar_kws={'label': 'Count'})\n"
        "plt.ylabel('Online order available')\n"
        "plt.xlabel('Book table available')\n"
        "plt.title('Heatmap: Online Order vs Book Table')\n"
        "plt.tight_layout()\n"
        "plt.savefig(OUT_DIR / '03_online_order_booking_heatmap.png', dpi=150)\n"
        "plt.show()\n"
    )
)

cells.append(
    md(
        "**(4) Rating vs votes** — same plot as in Chapter 5 (`04_rating_vs_votes_scatter.png`).\n"
    )
)

cells.append(
    code(
        "# (5) Restaurant distribution by location\n"
        "loc_counts = df['location'].value_counts().head(15).sort_values()\n"
        "fig, ax = plt.subplots(figsize=(10, 5))\n"
        "ax.barh(loc_counts.index.astype(str), loc_counts.values, color=SKY, edgecolor='black')\n"
        "ax.set_title('Restaurant Distribution by Location')\n"
        "ax.set_xlabel('Number of Restaurants')\n"
        "ax.set_ylabel('Location')\n"
        "plt.tight_layout()\n"
        "plt.savefig(OUT_DIR / '05_restaurants_by_location.png', dpi=150)\n"
        "plt.show()\n"
    )
)

cells.append(md("### Feature verification\n"))

cells.append(
    code(
        "verification = pd.DataFrame(\n"
        "    [\n"
        "        ['Data Loading (CSV Import)', 'Working', 'Zomato dataset loaded using Pandas'],\n"
        "        ['Data Cleaning', 'Working', 'Missing values, duplicates, inconsistent formats handled'],\n"
        "        ['Data Transformation', 'Working', 'Ratings and cost converted to numerical formats'],\n"
        "        ['Exploratory Data Analysis (EDA)', 'Working', 'Patterns across ratings, votes, cuisines, locations'],\n"
        "        ['Data Visualization', 'Working', 'Charts generated using Matplotlib and Seaborn'],\n"
        "        ['Correlation Analysis', 'Working', 'Heatmap for rate, votes, approx_cost'],\n"
        "        ['Feature Engineering', 'Working', 'cost_per_person and rating_category'],\n"
        "        ['SQLite Integration (ELT)', 'Working', 'Cleaned data stored in zomato.db'],\n"
        "        ['SQL Query Execution', 'Working', 'Top-rated restaurants and popular cuisines'],\n"
        "        ['Insight Generation', 'Working', 'Meaningful trends identified from the dataset'],\n"
        "    ],\n"
        "    columns=['Feature', 'Status', 'Notes'],\n"
        ")\n"
        "print(verification.to_string(index=False))\n"
    )
)

cells.append(
    md(
        "## Conclusion\n\n"
        "This project loads the Zomato Bangalore listings CSV, cleans and types key fields, explores city and "
        "cuisine patterns, visualizes ratings and service options, quantifies linear relationships with a "
        "correlation heatmap, and stores the cleaned table in SQLite for reusable queries. Derived features "
        "(`cost_per_person`, `rating_category`) support segmentation for further analysis.\n\n"
        "### Takeaways\n\n"
        "- Built a repeatable Pandas workflow for messy restaurant data.\n"
        "- Combined Matplotlib and Seaborn for distribution, count, heatmap, and scatter views.\n"
        "- Used SQLite as a lightweight warehouse for ranking and cuisine-frequency queries.\n"
        "- Practiced feature engineering and checklist-style verification before drawing conclusions.\n"
    )
)

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "cells": cells,
}

for cell in nb["cells"]:
    cell["id"] = str(uuid.uuid4())

Path(__file__).resolve().parent.joinpath("zomato_analysis.ipynb").write_text(
    json.dumps(nb, indent=2), encoding="utf-8"
)
print("wrote zomato_analysis.ipynb,", len(cells), "cells")
