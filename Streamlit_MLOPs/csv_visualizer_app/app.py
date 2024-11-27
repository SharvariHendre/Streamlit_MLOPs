import streamlit as st
import pandas as pd
import plotly.express as px
import io
import base64

def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def get_download_link(df, filename="data.csv"):
    """Generates a link to download the dataframe as CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'
    return href

def main():
    # Set page config
    st.set_page_config(
        page_title="CSV Data Visualizer",
        page_icon="📊",
        layout="wide"
    )
    
    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 CSV Data Visualizer")
    st.write("Upload your CSV file and create interactive visualizations")
    
    # File upload with additional info
    uploaded_file = st.file_uploader(
        "Choose a CSV file", 
        type="csv",
        help="Upload a CSV file to analyze and visualize its data"
    )
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            # Create tabs for different sections
            tab1, tab2, tab3 = st.tabs(["📈 Visualizations", "📊 Data Analysis", "📑 Raw Data"])
            
            with tab1:
                st.subheader("Create Visualization")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Visualization controls
                    chart_type = st.selectbox(
                        "Select Chart Type",
                        ["Line Chart", "Bar Chart", "Histogram", "Scatter Plot", "Box Plot"]
                    )
                    
                    # Get numerical columns
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                    
                    if chart_type in ["Line Chart", "Bar Chart"]:
                        x_col = st.selectbox("Select X-axis column", df.columns)
                        y_col = st.selectbox("Select Y-axis column", numeric_cols)
                        
                        if chart_type == "Line Chart":
                            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                        else:  # Bar Chart
                            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                    
                    elif chart_type == "Histogram":
                        col = st.selectbox("Select column for histogram", numeric_cols)
                        bins = st.slider("Number of bins", min_value=5, max_value=50, value=20)
                        fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}")
                    
                    elif chart_type == "Box Plot":
                        y_col = st.selectbox("Select column for box plot", numeric_cols)
                        x_col = st.selectbox("Select grouping column (optional)", ["None"] + list(df.columns))
                        if x_col == "None":
                            fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
                        else:
                            fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")
                    
                    else:  # Scatter Plot
                        x_col = st.selectbox("Select X-axis column", numeric_cols)
                        y_col = st.selectbox("Select Y-axis column", numeric_cols)
                        color_col = st.selectbox("Select color column (optional)", ["None"] + list(df.columns))
                        
                        if color_col == "None":
                            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                        else:
                            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                                          title=f"{y_col} vs {x_col} by {color_col}")
                
                with col2:
                    # Display the plot
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.subheader("Data Analysis")
                
                # Data info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Number of Rows", df.shape[0])
                with col2:
                    st.metric("Number of Columns", df.shape[1])
                with col3:
                    st.metric("Missing Values", df.isna().sum().sum())
                
                # Basic statistics
                st.subheader("Statistical Summary")
                st.dataframe(df.describe(), use_container_width=True)
                
                # Correlation matrix
                if len(numeric_cols) > 1:
                    st.subheader("Correlation Matrix")
                    corr = df[numeric_cols].corr()
                    fig_corr = px.imshow(corr, 
                                       title="Correlation Matrix",
                                       color_continuous_scale="RdBu")
                    st.plotly_chart(fig_corr, use_container_width=True)
            
            with tab3:
                st.subheader("Raw Data Preview")
                st.dataframe(df, use_container_width=True)
                
                # Download button
                st.markdown(get_download_link(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()