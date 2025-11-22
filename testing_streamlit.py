import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Simple Data Dashboard")

# Uploader accepts Excel files
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)

        # Use containers for better layout
        with st.container():
            st.subheader("Data Preview")
            st.write(df.head())

            st.subheader("Data Summary")
            st.write(df.describe())

        # Filter by Region (assuming 'REGION' column exists)
        with st.container():
            st.subheader("Filter Data by Region")
            if 'REGION' in df.columns:
                regions = df['REGION'].dropna().unique()
                selected_region = st.selectbox("Select Region", regions)
                filtered_by_region = df[df['REGION'] == selected_region]
                st.write(filtered_by_region)
            else:
                st.warning("No 'REGION' column found in the data.")

        # Display data for a specific vendor (assuming 'VENDOR_ID' column exists for vendor)
        with st.container():
            st.subheader("Display Data for a Specific Vendor")
            if 'ID' in df.columns:
                vendor_ids = df['ID'].dropna().unique()
                selected_vendor_id = st.multiselect("Select Vendor ID(s)", vendor_ids)
                if selected_vendor_id:
                    filtered_by_vendor = df[df['ID'].isin(selected_vendor_id)]
                    st.write(filtered_by_vendor)
                else:
                    st.info("Select at least one vendor ID.")
            else:
                st.warning("No 'VENDOR_ID' column found in the data.")

        # Graphs for Units Sold, Total Sales, and Average Sales
        with st.container():
            st.subheader("Graphs")
            # Assuming columns: 'UNITS SOLD', 'TOTAL SALES', 'AVERAGE SALES', and a date or category column for x-axis
            graph_columns = ['UNITS SOLD', 'TOTAL SALES', 'AVERAGE SALES']
            available_graph_cols = [col for col in graph_columns if col in df.columns]
            if available_graph_cols:
                x_column = st.selectbox("Select x-axis column for graphs (e.g., Date or Category)", df.columns.tolist())
                for col in available_graph_cols:
                    if st.button(f"Generate {col} Graph"):
                        try:
                            fig, ax = plt.subplots()
                            ax.plot(df[x_column], df[col], marker='o')
                            ax.set_title(f"{col} over {x_column}")
                            ax.set_xlabel(x_column)
                            ax.set_ylabel(col)
                            st.pyplot(fig)
                        except Exception as e:
                            st.error(f"Error generating {col} graph: {e}")
            else:
                st.warning("Required columns for graphs ('UNITS SOLD', 'TOTAL SALES', 'AVERAGE SALES') not found.")

        # Additional interactive elements: General filter and plot
        with st.container():
            st.subheader("General Filter and Plot")
            columns = df.columns.tolist()
            selected_column = st.selectbox("Select column to filter by", columns)
            unique_values = df[selected_column].dropna().unique()
            selected_value = st.selectbox("Select value", unique_values)

            filtered_df = df[df[selected_column] == selected_value]
            st.write(filtered_df)

            x_column = st.selectbox("Select x-axis column", columns, key="x_axis")
            y_column = st.selectbox("Select y-axis column", columns, key="y_axis")

            if st.button("Generate Plot"):
                try:
                    st.line_chart(filtered_df.set_index(x_column)[y_column])
                except Exception as e:
                    st.error(f"Error generating plot: {e}")

    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")

else:
    st.info("Please upload an Excel file to begin.")