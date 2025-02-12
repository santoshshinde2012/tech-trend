import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Load Data
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return pd.read_csv("data.csv")  # Default dataset if no file is uploaded

# Define y-axis labels
y_labels = ["Not Significant", "Low", "Moderate", "Moderate to High", "High", "Very High"]

# Custom colormap
custom_cmap = LinearSegmentedColormap.from_list(
    "custom_cmap", ["#D3D3D3", "#ADD8E6", "#87CEEB", "#FFD700", "#FF8C00", "#FF4500"], N=6
)

# Plot Heatmap
def plot_heatmap(df, selected_technologies):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        df.set_index("Year")[selected_technologies].T,
        cmap=custom_cmap,
        linewidths=0.5,
        annot=True,
        fmt="d",
        ax=ax,
        vmin=0, vmax=5
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Technology")
    ax.set_title("Technology Impact Over Time")
    st.pyplot(fig)

# Plot Line Chart
def plot_line_chart(df, selected_technologies):
    fig, ax = plt.subplots()
    for tech in selected_technologies:
        ax.plot(df["Year"], df[tech], label=tech)
    ax.set_xlabel("Year")
    ax.set_ylabel("Impact Level")
    ax.set_title("Technology Trends Over Time")
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)
    st.pyplot(fig)

# UI Layout
def main():
    st.set_page_config(layout="wide")
    left_column, right_column = st.columns([30, 70])

    with left_column:
        # st.write("### Upload CSV File")
        # uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        uploaded_file = None
        # Load data based on upload
        df = load_data(uploaded_file)

        # st.write("### CSV Data")
        # st.write(df.style.set_sticky()) 
        selected_technologies = st.multiselect("Select Technologies", df.columns[1:], default=["AI"])
        chart_type = st.radio("Select Chart Type", ["Line Chart", "Heatmap"])
        st.download_button("Download CSV", df.to_csv(index=False), "data.csv", "text/csv")

    with right_column:
        if chart_type == "Line Chart":
            plot_line_chart(df, selected_technologies)
        else:
            plot_heatmap(df, selected_technologies)

if __name__ == "__main__":
    main()
