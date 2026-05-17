Restaurant Data Analysis — Zomato Dataset

**What this project is**

- **Summary:** End-to-end exploratory analysis of the Zomato restaurant listings for Bangalore. It cleans the raw CSV, explores rating, cost, cuisine and location patterns, generates visual snapshots, and stores a cleaned table in SQLite for queries.

**Quick run (VS Code, recommended)**

```bash
cd "/Users/riteshgarg/Downloads/Data Science Project"
source .venv/bin/activate
pip install -r requirements.txt
export MPLBACKEND=Agg
python -m nbconvert --to notebook --execute zomato_analysis.ipynb --output executed.ipynb --ExecutePreprocessor.timeout=600
```

**What you will find**

- **Notebook:** [zomato_analysis.ipynb](zomato_analysis.ipynb) — analysis and code cells.
- **Executed notebook:** [executed.ipynb](executed.ipynb) — run outputs saved after execution.
- **Generated visuals:** [outputs/](outputs/) — PNGs of charts (rating popularity, heatmaps, scatter, location bars).
- **Cleaned data:** [zomato.db](zomato.db) — SQLite DB with the cleaned table.
- **Helpers:** [\_build_notebook.py](_build_notebook.py) and [requirements.txt](requirements.txt) — reproducibility.

**Key snapshots & where to look**

- **Rating distribution:** outputs/01_rating_popularity.png — shows how ratings are distributed.
- **Rating vs votes:** outputs/04_rating_vs_votes_scatter.png — relationship between ratings and popularity.
- **Service flags:** outputs/02_online_order_booking_comparison.png and outputs/03_online_order_booking_heatmap.png — online-order vs booking availability.
- **Location distribution:** outputs/05_restaurants_by_location.png — top locations by restaurant count.

**Why this matters (significance, in simple terms)**

- **Quick insights:** Visual summaries reveal where high-rated restaurants cluster and how cost, cuisine and service options relate to ratings and popularity. These help businesses, analysts, or product teams make data-driven decisions (e.g., target locations, pricing, or features like online ordering).
- **Reproducibility:** The notebook + scripts let anyone reproduce the exact figures and queries; the SQLite DB supports fast ranking and aggregation queries for further analysis.

**Notes & next steps**

- **View results quickly:** open the PNGs in the outputs folder or open report.html if you exported the notebook to HTML.
- **Edit & iterate:** open [zomato_analysis.ipynb](zomato_analysis.ipynb) in VS Code, select the project `.venv` kernel, and Run All to see inline outputs.
