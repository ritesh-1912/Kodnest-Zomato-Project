# Zomato restaurant data analysis

Python analysis of Zomato restaurant listings: cleaning, exploratory summaries, visualizations, correlation heatmaps, and SQLite export.

## Setup

1. Clone the repository and enter the project directory.
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Add the dataset file `zomato.csv` in the project root (same folder as `run_analysis.py`). Use a public Zomato Bangalore CSV export with the expected columns (`rate`, `votes`, `location`, `online_order`, `book_table`, `cuisines`, `approx_cost(for two people)`, etc.).

4. Run the pipeline or open the notebook:

   ```bash
   python run_analysis.py
   ```

   Or open `zomato_analysis.ipynb` in Jupyter / VS Code and run all cells.

5. Optional: regenerate the notebook JSON from `_build_notebook.py` after editing that script:

   ```bash
   python _build_notebook.py
   ```

Figures are written to `outputs/`. The SQLite file `zomato.db` is created when you run the script or the notebook.

## Repository contents

| Item | Description |
|------|-------------|
| `requirements.txt` | Python dependencies |
| `run_analysis.py` | End-to-end script |
| `zomato_analysis.ipynb` | Interactive notebook |
| `_build_notebook.py` | Helper to rebuild the `.ipynb` from embedded templates |
| `outputs/` | Saved chart images |
