"""
Restaurant Data Analysis — Zomato listings (Python pipeline).
Run:  python run_analysis.py
Outputs: outputs/*.png, zomato.db
"""
from __future__ import annotations

import os
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(PROJECT_DIR, "zomato.csv")
OUT_DIR = os.path.join(PROJECT_DIR, "outputs")
DB_PATH = os.path.join(PROJECT_DIR, "zomato.db")

BLUE = "#1f77b4"
SKY = "#AED6F1"


def load_and_clean() -> pd.DataFrame:
    """Load CSV, drop duplicates and invalid rows, normalize rating and cost columns."""
    df = pd.read_csv(CSV_PATH, low_memory=False)
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["rate", "approx_cost(for two people)"], inplace=True)

    df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False)
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

    df["approx_cost(for two people)"] = (
        df["approx_cost(for two people)"].astype(str).str.replace(",", "", regex=False)
    )
    df["approx_cost(for two people)"] = df["approx_cost(for two people)"].astype(float)

    df.dropna(subset=["rate"], inplace=True)
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Add cost_per_person and rating_category."""
    df = df.copy()
    df["cost_per_person"] = df["approx_cost(for two people)"] / 2

    def rating_category(rating: float) -> str:
        if rating >= 4:
            return "Excellent"
        if rating >= 3:
            return "Good"
        return "Average"

    df["rating_category"] = df["rate"].apply(rating_category)
    return df


def savefig(name: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print("saved", path)


def main() -> None:
    plt.rcParams.update(
        {
            "axes.grid": True,
            "grid.alpha": 0.35,
            "axes.facecolor": "white",
            "figure.facecolor": "white",
        }
    )
    sns.set_theme(style="whitegrid")

    df = load_and_clean()
    print("--- Cleaned preview ---")
    print(df.head())
    print("\nShape after cleaning:", df.shape)

    plt.figure(figsize=(8, 5))
    plt.scatter(df["rate"], df["votes"], c=BLUE, edgecolors="black", linewidths=0.25, alpha=0.35, s=22)
    plt.title("Ratings vs Votes (Popularity)")
    plt.xlabel("Rate out of 5")
    plt.ylabel("Votes of popularity")
    savefig("04_rating_vs_votes_scatter.png")

    corr = df[["rate", "votes", "approx_cost(for two people)"]].corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation heatmap")
    savefig("06_correlation_heatmap.png")
    print("\n--- Correlation matrix ---")
    print(corr)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("zomato", conn, index=False, if_exists="replace")
    query = """
    SELECT location, name, rate
    FROM zomato
    WHERE rate IS NOT NULL
    ORDER BY rate DESC
    LIMIT 10;
    """
    top_restaurants = pd.read_sql(query, conn)
    print("\n--- Top 10 restaurants by rating ---")
    print(top_restaurants.to_string(index=False))
    conn.close()
    print("\nSQLite database written to:", DB_PATH)

    df = feature_engineering(df)
    print("\n--- Feature engineering ---")
    print(df[["rate", "rating_category"]].head())
    print(df["rating_category"].value_counts())

    freq = df["rate"].round(1).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(freq.index.astype(float), freq.values, width=0.09, color=BLUE, align="center")
    ax.set_title("Rating popularity")
    ax.set_xlabel("Rating")
    ax.set_ylabel("frequency")
    savefig("01_rating_popularity.png")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    order_lab = df["online_order"].map({"Yes": "Available", "No": "Not Available"})
    oc = order_lab.value_counts().reindex(["Available", "Not Available"])
    axes[0].bar(oc.index.astype(str), oc.values, color=SKY, edgecolor="black")
    axes[0].set_title("Online Order")
    axes[0].set_xlabel("Online Order Availability")
    axes[0].set_ylabel("Count")

    book_lab = df["book_table"].map({"Yes": "Available", "No": "Not Available"})
    bc = book_lab.value_counts().reindex(["Not Available", "Available"])
    axes[1].bar(bc.index.astype(str), bc.values, color=BLUE, edgecolor="black")
    axes[1].set_title("Book Table")
    axes[1].set_xlabel("Book Order Availability")
    axes[1].set_ylabel("Count")
    savefig("02_online_order_booking_comparison.png")

    oo = df["online_order"] == "Yes"
    bt = df["book_table"] == "Yes"
    ct = pd.crosstab(oo, bt)
    ct.index = ["False", "True"]
    ct.columns = ["False", "True"]
    plt.figure(figsize=(6.5, 4.5))
    sns.heatmap(ct, annot=True, fmt=".2e", cmap="Blues", cbar_kws={"label": "Count"})
    plt.ylabel("Online order available")
    plt.xlabel("Book table available")
    plt.title("Heatmap: Online Order vs Book Table")
    savefig("03_online_order_booking_heatmap.png")

    loc_counts = df["location"].value_counts().head(15).sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(loc_counts.index.astype(str), loc_counts.values, color=SKY, edgecolor="black")
    ax.set_title("Restaurant Distribution by Location")
    ax.set_xlabel("Number of Restaurants")
    ax.set_ylabel("Location")
    savefig("05_restaurants_by_location.png")


if __name__ == "__main__":
    main()
