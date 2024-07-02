import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Function to create MySQL connection
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Your MySQL password
        database="db_forecasting"  # Your database name
    )
    return conn

# Function to fetch data from a table
def fetch_data(query, conn):
    return pd.read_sql(query, conn)

# Function to get total transactions and total stock from forecasting table
def get_total_statistics(conn):
    query = "SELECT COUNT(*) AS total_transactions, SUM(JUMLAH_STOK) AS total_stock FROM forecasting"
    df = fetch_data(query, conn)
    return df

# Function to get data for plotting
def get_data_for_plot(conn, table_name, x_column, y_column):
    query = f"SELECT {x_column}, {y_column} FROM {table_name}"
    df = fetch_data(query, conn)
    return df

# Function to show the statistics dashboard
def show_halaman_utama():
    st.title("Dashboard Statistika Toko CV.KaryaAnakBangsa")

    conn = create_connection()

    # Get total transactions and total stock from forecasting
    df_stats = get_total_statistics(conn)
    st.subheader("Total Transaksi dan Jumlah Stok")
    st.write(df_stats)

    # Plotting total transactions and total stock from forecasting
    if not df_stats.empty:
        total_transactions = df_stats["total_transactions"].iloc[0]
        total_stock = df_stats["total_stock"].iloc[0]

        # Display as text
        st.markdown(f"Total Transaksi: **{total_transactions}**")
        st.markdown(f"Total Jumlah Stok: **{total_stock}**")

    # Statistic 2: Pie Chart - Distribusi Level Akses Pengguna (users)
    st.header("Statistik 2: Distribusi Level Akses Pengguna (users)")
    df_users = get_data_for_plot(conn, "users", "level_akses", "COUNT(*)")
    st.write(df_users.head())  # Display the data for transparency

    if not df_users.empty:
        labels = df_users["level_akses"]
        sizes = df_users["COUNT(*)"]
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Pie Chart: Distribusi Level Akses Pengguna")
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(plt)

    # Statistic 3: Line Chart - Grafik Data Transaksi
    st.header("Statistik 3: Grafik Data Transaksi")
    df_transaksi = get_data_for_plot(conn, "transaksi", "ID_TRANSAKSI", "QTY_KIRIM")
    st.write(df_transaksi.head())  # Display the data for transparency

    if not df_transaksi.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(df_transaksi["ID_TRANSAKSI"], df_transaksi["QTY_KIRIM"], marker='o')
        plt.xlabel("ID Transaksi")
        plt.ylabel("Jumlah Stok")
        plt.title("Line Chart: Grafik Data Transaksi")
        st.pyplot(plt)

      # Example chart 3: Pie chart
    st.header("Pie Chart Example")
    df_transaksi = get_data_for_plot(conn, "transaksi", "ID_TRANSAKSI", "NAMA_BARANG")
    st.write(df_transaksi.head())  # Display the data for transparency

    if not df_transaksi.empty:
        labels = df_transaksi["NAMA_BARANG"]
        sizes = df_transaksi["ID_TRANSAKSI"]
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Pie Chart: Distribusi Nama Barang")
        st.pyplot(plt)

    conn.close()

# Run the Streamlit app
if __name__ == "__main__":
    show_halaman_utama()
