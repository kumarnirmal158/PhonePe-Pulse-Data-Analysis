
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from utils.db import get_connection

conn = get_connection()

st.title("📈 Business Case Study")

# ------------------------------------------- BUSINESS CASE STUDY ---------------------------------------------------
question = st.selectbox(
    "Select Case Study",
    [
        "1️⃣ Device Dominance & User Engagement",
        "2️⃣ User Engagement & Growth Strategy",
        "3️⃣ Transaction Analysis (State & District)",
        "4️⃣ User Registration Analysis",
        "5️⃣ Insurance Transactions Analysis"
    ]
)

# ------------------------------------------- YEAR & QUARTER FILTERS -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("Select Year",sorted(pd.read_sql("SELECT DISTINCT Year FROM map_users", conn)["Year"]))

with col2:
    quarter = st.selectbox("Select Quarter", [1,2,3,4])


#------------------------------------------- 1️⃣ DEVICE DOMINANCE & USER ENGAGEMENT------------------------------------

if question.startswith("1"):
    st.header("📱 Device Dominance & User Engagement")

#---------- SQL Queries for Data Analysis ------------------------------
    query1 = ('''SELECT
    Transaction_brand AS Device_Brand,
    SUM(Transaction_count) AS Total_Tran_Count,
    AVG(Transaction_percentage) AS Total_Tran_percentage
    FROM Agg_user  WHERE Year=? AND quarter=?
    GROUP BY Device_Brand
    ORDER BY Total_Tran_Count DESC;''')
    df_brand = pd.read_sql_query(query1, conn, params=(year, quarter))
    
    query2 = ('''SELECT
    State,
    SUM(Registered_user) AS Total_Registered_Users,
    SUM(App_opening) AS Total_App_Opens
    FROM map_users
    WHERE Year=? AND quarter=?
    GROUP BY State
    ORDER BY Total_Registered_Users DESC, Total_App_Opens DESC;''')
    df_eng  = pd.read_sql_query(query2, conn, params=(year, quarter))
    df_eng['Engagement_Ratio'] = (df_eng['Total_App_Opens'] / df_eng['Total_Registered_Users']).round(2)

    query3 = ('''SELECT
    Year,
    quarter,
    Transaction_brand AS Device_Brand,
    SUM(Transaction_count) AS Total_Tran_Count
    FROM Agg_user
    GROUP BY Year, quarter, Device_Brand
    ORDER BY Year, quarter;''')
    df_trend = pd.read_sql_query(query3, conn)

    
# ------------------------------ CLEAN STATE NAMES -----------------------------------------------------
    df_eng['State']=df_eng['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
    df_eng['State']=df_eng['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
    df_eng['State']=df_eng['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
    df_eng['State']=df_eng['State'].str.replace("-"," ")
    df_eng['State']=df_eng['State'].str.title()
#---------------------------------- Map – Registered Users by State ----------------------------------------
    fig = px.choropleth(
        df_eng,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color='Total_Registered_Users',
        color_continuous_scale='Viridis',
        hover_data=['Total_Registered_Users', 'Engagement_Ratio']
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text="State-wise Registered Users & Engagement")
    st.plotly_chart(fig, width="stretch")
     


#--------------------------------- Visualization ----------------------------------------
# Bar Chart – Registered Users by Brand

    st.subheader("📊 Device Brand Dominance (Transaction Count)")

    df_top10_brand = df_brand.sort_values("Total_Tran_Count", ascending=False).head(10)

    fig = px.bar(
    df_top10_brand,
    x="Device_Brand",
    y="Total_Tran_Count",
    text_auto=True,
    title="Top 10 Device Brands by Transaction Count"
)

    st.plotly_chart(fig, width="stretch")


# Pie Chart – App Engagement Share by Brand

    st.subheader("📈 Engagement Share by Device Brand")
    df_top10 = df_brand.sort_values("Total_Tran_Count", ascending=False).head(10)
    fig = px.pie(
        df_top10, 
        values='Total_Tran_Count', 
        names='Device_Brand', 
        title='Average Transaction Share by Brand (%)',
        hole=0.3, 
        )
    fig.update_traces(textposition='outside', textinfo='percent+label')

    st.plotly_chart(fig, width="stretch")


# Horizontal Bar Chart – App Opens by State
    st.subheader("📍 App Opens by State")
    plt.figure(figsize=(12,8))
    plt.barh( df_eng.sort_values("Total_App_Opens")["State"], df_eng.sort_values("Total_App_Opens")["Total_App_Opens"])
    plt.title("Total App Opens by State")
    plt.xlabel("App Opens")
    plt.ylabel("State")
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

# Ratio Chart – App Opens per User (State Level)
    st.subheader("📈 App Opens per Registered User (Top States)")
    df_ratio = df_eng.sort_values("Engagement_Ratio", ascending=False).head(10)
    fig = px.bar(
    df_ratio,
    x="State",
    y="Engagement_Ratio",
    text_auto=True,
    title="Top States by Engagement Ratio")
    st.plotly_chart(fig, width="stretch")


# Line Chart – Registered Users vs App Opens (State-wise)
    st.subheader("📉 Registered Users vs App Opens")
    plt.figure(figsize=(14,6))
    plt.plot(df_eng['State'], df_eng['Total_Registered_Users'], marker='o', label='Registered Users')
    plt.plot(df_eng['State'], df_eng['Total_App_Opens'], marker='s', label='App Opens')
    plt.yscale('log')
    plt.title("Registered Users vs App Opens by State")
    plt.xticks(rotation=90)
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

# Line Chart – Brand Engagement Across Time
    st.subheader("📉 Brand Engagement Trend Over Time")
    top_10_brands = ( df_trend.groupby("Device_Brand")["Total_Tran_Count"].sum().sort_values(ascending=False).head(10).index)
    df_trend_top10 = df_trend[df_trend["Device_Brand"].isin(top_10_brands)]
    fig = px.line(
    df_trend_top10,
    x="quarter",
    y="Total_Tran_Count",
    color="Device_Brand",
    facet_col="Year",
    markers=True,
    title="Device Brand Engagement Trend")
    st.plotly_chart(fig, width="stretch")


#------------------------------------ 2️⃣ USER ENGAGEMENT & GROWTH STRATEGY------------------------------------------------------

elif question.startswith("2"):
    st.subheader("User Engagement & Growth Strategy")

#------------------- SQL Queries for Data Analysis -------------------------------
    
    query1 = ('''SELECT State, District, Year, quarter,
                SUM(App_opening) AS app_opens,
                SUM(Registered_user) AS Users
                FROM map_users
                WHERE Year=? AND quarter=?
                GROUP BY State, District, Year, quarter''')
    df_map_users_filt = pd.read_sql_query(query1,conn, params=(year, quarter))

    query2 = ('''SELECT State, District, Year,
                SUM(App_opening) AS app_opens,
                SUM(Registered_user) AS Users
                FROM map_users
                GROUP BY State, District, Year''')

    df_map_users_all = pd.read_sql_query(query2, conn)


   # --------------------------- CLEAN STATE NAMES ---------------------------
    df_map_users_filt['State']=df_map_users_filt['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
    df_map_users_filt['State']=df_map_users_filt['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
    df_map_users_filt['State']=df_map_users_filt['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
    df_map_users_filt['State']=df_map_users_filt['State'].str.replace("-"," ")
    df_map_users_filt['State']=df_map_users_filt['State'].str.title()
   
   #---------------------------------- Map -------------------------------------- 
    fig_map = px.choropleth(
        df_map_users_filt,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="app_opens",
        hover_data=["Users", "app_opens"],
        title="App Opens by State")
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, width="stretch")
 
#--------------------------------- Visualization ----------------------------------------

# Bar Chart – State-wise Registered Users (Top 10)

    st.subheader("Top 10 States by Registered Users")

    df_state_user = (df_map_users_filt.groupby("State", as_index=False)["Users"].sum()
                     .sort_values("Users", ascending=False).head(10))

    fig = px.bar(
        df_state_user,
        x="State",
        y="Users",
        text_auto=True,
        title="Top 10 States by Registered Users")

    st.plotly_chart(fig, width="stretch")


# Bar Chart – State-wise App Opens (Top 10)

    st.subheader("Top 10 States by App Opens")

    df_state_opens = (df_map_users_filt.groupby("State", as_index=False)["app_opens"].sum()
                      .sort_values("app_opens", ascending=False).head(10))

    fig = px.bar(
        df_state_opens,
        x="State",
        y="app_opens",
        text_auto=True,
        title="Top 10 States by App Opens")

    st.plotly_chart(fig, width="stretch")


# Bar Chart – Top 10 Districts by Registered Users
    st.subheader("TOP 10 DISTRICTS BY REGISTERED USERS")
    df_districts = (df_map_users_filt.groupby("District")["Users"].sum().sort_values(ascending=False).head(10))
    plt.figure(figsize=(13,6))
    plt.bar(df_districts.index, df_districts.values)
    plt.title("Top 10 Districts by Registered Users")
    plt.xlabel("District")
    plt.ylabel("Users")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

# Line Chart – Year-wise User Growth
    st.subheader("GROWTH TREND OF REGISTERED USERS OVER YEARS")

    df_yearly = df_map_users_all.groupby("Year")["Users"].sum()

    plt.figure(figsize=(10,6))
    plt.plot(df_yearly.index, df_yearly.values, marker="o")
    plt.title("Year-wise Growth of Registered Users")
    plt.xlabel("Year")
    plt.ylabel("Registered Users")
    plt.grid(True)
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

# Combined Bar Chart – Registrations vs App Opens (Top States)

    st.subheader("Registrations vs App Opens (Top States)")

    df_compare = (df_map_users_filt.groupby("State", as_index=False).sum()
                  .sort_values("Users", ascending=False).head(10))

    fig = px.bar(
        df_compare,
        x="State",
        y=["Users", "app_opens"],
        barmode="group",
        title="Registrations vs App Opens by State")

    st.plotly_chart(fig, width="stretch")

# Heatmap - App Opens (State vs Year)
    st.subheader("HEATMAP OF APP OPENS ACROSS STATES AND YEARS")
    df_heatmap = (df_map_users_all.groupby(["State", "Year"])["app_opens"].sum().unstack())

    plt.figure(figsize=(12,10))
    plt.imshow(df_heatmap, aspect="auto")
    plt.colorbar(label="App Opens")
    plt.title("Heatmap: App Opens Across States and Years")
    plt.xlabel("Year")
    plt.ylabel("State")
    plt.xticks(range(len(df_heatmap.columns)), df_heatmap.columns, rotation=45)
    plt.yticks(range(len(df_heatmap.index)), df_heatmap.index)
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)


#------------------------------------- 3️⃣ TRANSACTION ANALYSIS (STATES & DISTRICTS) ------------------------------------------------------
elif question.startswith("3"):
    st.subheader("Transaction Analysis (State & District)")

#------------------- SQL Queries for Data Analysis -------------------------------

    query1 = (''' SELECT
            State,
            SUM(Transaction_amount) AS Amount
            FROM Agg_Tran
            WHERE Year=? AND quarter=?
            GROUP BY State;''')
    df_state_value = pd.read_sql_query(query1, conn, params=(year, quarter))

    query2 = ('''SELECT 
    State,
    SUM(Transaction_count) AS Total_Transaction_Count
    FROM Agg_Tran
    GROUP BY State
    ORDER BY Total_Transaction_Count DESC;''')
    df_state_count = pd.read_sql_query(query2, conn)

    query3 = ('''SELECT
    Transaction_district AS District,
    State,
    SUM(Transaction_amount) AS Total_District_Value
    FROM map_trans
    GROUP BY Transaction_district, State
    ORDER BY Total_District_Value DESC;''')
    df_district_value = pd.read_sql_query(query3, conn)

    query4 = ('''SELECT
    Name AS Pincode,
    State,
    sum(Transaction_Amount) AS Pin_Value
    FROM top_ins
    where Level='Pincode'
    GROUP BY Name, State
    ORDER BY Pin_Value DESC;''')
    df_pincode_value = pd.read_sql_query(query4, conn)

    query5 = ('''SELECT
    Year,
    SUM(Transaction_amount) AS Yearly_Value,
    SUM(Transaction_count) AS Yearly_Count
    FROM Agg_Tran
    GROUP BY Year
    ORDER BY Year;''')
    df_yearly = pd.read_sql_query(query5, conn)
    
   # ---------------- CLEAN STATE NAMES ----------------
    df_state_value['State']=df_state_value['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
    df_state_value['State']=df_state_value['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
    df_state_value['State']=df_state_value['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
    df_state_value['State']=df_state_value['State'].str.replace("-"," ")
    df_state_value['State']=df_state_value['State'].str.title()

    fig_map = px.choropleth(
        df_state_value,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Amount", 
        title="Total Transaction Value by State"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, width="stretch")


# Visualization:
# Bar Chart – Top 10 States by Transaction Value
    st.subheader("Top 10 States by Transaction Value")

    df_top_value = df_state_value.sort_values("Amount", ascending=False).head(10)

    fig = px.bar(
        df_top_value,
        x="State",
        y="Amount",
        text_auto=True,
        title="Top 10 States by Transaction Value")

    st.plotly_chart(fig, width="stretch")

# Bar Chart – Top 10 States by Transaction Count
    st.subheader("Top 10 States by Transaction Count")
    df_top_count = df_state_count.sort_values("Total_Transaction_Count", ascending=False).head(10)
    fig = px.bar(
        df_top_count,
        x="State",
        y="Total_Transaction_Count",
        text_auto=True,
        title="Top 10 States by Transaction Count")
    st.plotly_chart(fig, width="stretch")

# Horizontal Bar Chart – Top Districts by Transaction Value
    st.subheader("Top 10 Districts by Transaction Value")

    df_district_tran = (df_district_value.sort_values("Total_District_Value", ascending=False).head(10))

    fig = px.bar(
        df_district_tran,
        x="Total_District_Value",
        y="District",
        text_auto=True,
        title="Top 10 Districts by Transaction Value",
        orientation='h')
    st.plotly_chart(fig, width="stretch")

# Bar Chart – Top 10 Pincodes by Transaction Value
    st.subheader("Top 10 Pincodes by Transaction Value")
    df_pincode_tran = (df_pincode_value.sort_values("Pin_Value", ascending=False).head(10))
    df_pincode_tran["Pincode"] = df_pincode_tran["Pincode"].astype(str)
    fig = px.bar(
        df_pincode_tran,
        x="Pincode",
        y="Pin_Value",
        text_auto=True,
        title="Top 10 Pincodes by Transaction Value")
    fig.update_layout(xaxis_type="category", xaxis_title="Pincode", yaxis_title="Transaction Value", xaxis_tickangle=-45)
    st.plotly_chart(fig, width="stretch")

# Pie Chart – Top States Contribution (Value %)
    st.subheader("Top States Contribution to Transaction Value")

    df_state_tran = df_state_value.groupby("State")["Amount"].sum().reset_index()
    df_state_tran = df_state_tran.sort_values("Amount", ascending=False).head(10)

    plt.figure(figsize=(8,8))
    plt.pie(df_state_tran["Amount"],
        labels=df_state_tran["State"],
        autopct='%1.1f%%')
    plt.title("Contribution of Top States to Transaction Value")
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)


# Line Chart – Year-wise Growth in Transaction Value
    st.subheader("Year-wise Growth in Transaction Value")
    plt.figure(figsize=(10,6))
    plt.plot(df_yearly["Year"],df_yearly["Yearly_Value"],marker="o")
    plt.title("Year-wise Growth of Transaction Value")
    plt.xlabel("Year")
    plt.ylabel("Transaction Value")
    plt.grid(True)
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

# Bar + Line Chart – Year-wise Transaction Count vs Value
    st.subheader("Year-wise Transaction Count vs Value")
    fig, ax1 = plt.subplots(figsize=(10,6))

# Bar for Value
    ax1.bar(df_yearly['Year'], df_yearly['Yearly_Value'], color='skyblue', label='Yearly Value')
    ax1.set_ylabel("Yearly Value", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

# Line for Count
    ax2 = ax1.twinx()
    ax2.plot(df_yearly['Year'], df_yearly['Yearly_Count'], color='orange', marker='o', label='Yearly Count')
    ax2.set_ylabel("Yearly Count", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    plt.title("Year-wise Transaction Count vs Value")
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)


#------------------------------------- 4️⃣ USER REGISTRATION ANALYSIS ------------------------------------------------------

elif question.startswith("4"):
    st.subheader("User Registration Analysis")

#--------------------- SQL Queries for Data Analysis ----------------------------
    query1 = ('''SELECT 
        State,
        SUM(Registered_user) AS Total_Registrations
        FROM map_users
        WHERE Year = ? AND quarter = ?
        GROUP BY State
        ORDER BY Total_Registrations DESC;''')
    df_state = pd.read_sql_query(query1, conn, params=(year, quarter))

    query2 = ('''SELECT 
        Name as District,
        State,
        SUM(registeredusers) AS Total_Registrations
        FROM top_users
        WHERE Year = ? AND quarter = ? and Level='District'
        GROUP BY District, State
        ORDER BY Total_Registrations DESC;''')
    df_district = pd.read_sql_query(query2, conn, params=(year, quarter))

    query3 = ('''SELECT
        Name AS Pincode,
        State,
        Transaction_Count AS Total_Registrations
        FROM top_ins
        WHERE Year = ? AND quarter = ? AND Level='Pincode'
        GROUP BY Name
        ORDER BY Total_Registrations DESC;''')
    df_pincode = pd.read_sql_query(query3, conn, params=(year, quarter))

    query4 = ('''SELECT
        State,
        SUM(Registered_user) AS Total_Registered_Users,
        SUM(App_opening) AS Total_App_Opens
        FROM map_users
        WHERE Year = ? AND quarter = ?
        GROUP BY State
        ORDER BY Total_Registered_Users DESC ;''')
    df_state_opens = pd.read_sql_query(query4, conn, params=(year, quarter))

    query5 = ('''SELECT 
        Year,
        quarter,
        SUM(Registered_user) AS Total_Registrations
        FROM map_users
        GROUP BY Year, quarter
        ORDER BY Year, quarter;''')
    df_trend = pd.read_sql_query(query5, conn)

   # ---------------- CLEAN STATE NAMES ----------------
    df_state_opens['State']=df_state_opens['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
    df_state_opens['State']=df_state_opens['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
    df_state_opens['State']=df_state_opens['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
    df_state_opens['State']=df_state_opens['State'].str.replace("-"," ")
    df_state_opens['State']=df_state_opens['State'].str.title()

#-----------------------------MAP-------------------------
    fig_map = px.choropleth(
        df_state_opens,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Total_Registered_Users",
        title="Total Registered Users by State"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, width="stretch")

#---------------------------- Visualization-----------------------
# Bar Chart – Top 10 States by User Registrations
    st.subheader("Top 10 States by User Registrations")

    df_state_top10 = df_state.head(10)

    fig = px.bar(
        df_state_top10,
        x="State",
        y="Total_Registrations",
        text_auto=True,
        title="Top 10 States by User Registrations")

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width= 'stretch')


# Horizontal Bar Chart – Top Districts (User Registrations)
    st.subheader("Top 10 Districts by User Registrations")

    df_district_top10 = df_district.head(10)

    fig = px.bar(
        df_district_top10,
        x="Total_Registrations",
        y="District",
        orientation="h",
        text_auto=True,
        title="Top 10 Districts by User Registrations")

    st.plotly_chart(fig, width= 'stretch')


# Bar Chart – Top 10 Pincodes by User Registrations
    st.subheader("Top 10 Pincodes by User Registrations")

    df_pincode_top10 = df_pincode.head(10)
    df_pincode_top10["Pincode"] = df_pincode_top10["Pincode"].astype(str)

    fig = px.bar(
        df_pincode_top10,
        x="Pincode",
        y="Total_Registrations",
        text_auto=True,
        title="Top 10 Pincodes by User Registrations")
    fig.update_layout(xaxis_type="category", xaxis_title="Pincode", yaxis_title="User registeration",xaxis_tickangle=-45)

    st.plotly_chart(fig, width= 'stretch')


# Combined Bar Chart – Registrations vs App Opens (State-wise)
    st.subheader("User Registrations vs App Opens by State")

    df_state_opens_top10 = df_state_opens.head(10)

    fig = px.bar(
        df_state_opens_top10,
        x="State",
        y=["Total_Registered_Users", "Total_App_Opens"],
        barmode="group",
        title="Registrations vs App Opens (Top States)")

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width= 'stretch')

# Line Chart – Year–quarter Trend in User Registrations
    st.subheader("User Registration Trend Over Time")

    df_trend["Year_Qtr"] = df_trend["Year"].astype(str) + " Q" + df_trend["quarter"].astype(str)

    fig = px.line(
        df_trend,
        x="Year_Qtr",
        y="Total_Registrations",
        markers=True,
        title="Year–Quarter Wise User Registration Growth")

    st.plotly_chart(fig, width= 'stretch')


#---------------------------------------------- 5️⃣ INSURANCE TRANSACTIONS ANALYSIS ---------------------------------------------------

elif question.startswith("5"):

    st.subheader("Insurance Transactions Analysis")

#-------------------- SQL Queries for Data Analysis -----------------------------------

    query1 = ('''SELECT 
            State,
            SUM(Transaction_amount) AS Total_Ins_Value
            FROM Agg_ins
            WHERE Year = ? AND quarter = ?
            GROUP BY State
            ORDER BY Total_Ins_Value DESC;''')
    df_state_value = pd.read_sql_query(query1, conn, params=(year, quarter))

    query2 = ('''SELECT 
            State,
            SUM(Transaction_count) AS Total_Ins_Count
            FROM Agg_ins
            WHERE Year = ? AND quarter = ?
            GROUP BY State
            ORDER BY Total_Ins_Count DESC;''')
    df_state_count = pd.read_sql_query(query2, conn, params=(year, quarter))

    query3 = ('''SELECT
            Name AS District,
            State,
            SUM(Transaction_amount) AS District_Ins_Value
            FROM top_ins
            WHERE Year = ? AND quarter = ? and Level = 'District'
            GROUP BY Name, State
            ORDER BY District_Ins_Value DESC;''')
    df_district_value = pd.read_sql_query(query3, conn, params=(year, quarter))

    query4 = ('''SELECT
            Name AS Pincode,
            State,
            Transaction_Amount AS Pin_Ins_Value
            FROM top_ins
            WHERE Year = ? AND quarter = ? AND Level='Pincode'
            GROUP BY Name
            ORDER BY Pin_Ins_Value DESC
            limit 10;''')
    df_pincode_value = pd.read_sql_query(query4, conn, params=(year, quarter))
    
    query5 = ('''SELECT 
            Year,
            SUM(Transaction_amount) AS Yearly_Ins_Value,
            SUM(Transaction_count) AS Yearly_Ins_Count
            FROM Agg_ins
            GROUP BY Year
            ORDER BY Year;''')
    df_yearly = pd.read_sql_query(query5, conn)

   # ---------------- CLEAN STATE NAMES ----------------
    df_state_value['State']=df_state_value['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
    df_state_value['State']=df_state_value['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
    df_state_value['State']=df_state_value['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
    df_state_value['State']=df_state_value['State'].str.replace("-"," ")
    df_state_value['State']=df_state_value['State'].str.title()


    fig_map = px.choropleth(
        df_state_value,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Total_Ins_Value",
        title="Total Insurance Transaction Value by State")
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, width="stretch")

# Visualization:

# Bar Chart – Top 10 States by Insurance Transaction Value
    st.subheader("Top 10 States by Insurance Transaction Value")

    df_state_top10 = (df_state_value.sort_values("Total_Ins_Value", ascending=False).head(10))

    fig = px.bar(
        df_state_top10,
        x="State",
        y="Total_Ins_Value",
        text_auto=True,
        title="Top 10 States by Insurance Transaction Value")

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width='stretch')

# Bar Chart – Top 10 States by Insurance Transaction Count

    st.subheader("Top 10 States by Insurance Transaction Count")

    df_state_count_top10 = (df_state_count.sort_values("Total_Ins_Count", ascending=False).head(10))

    fig = px.bar(
        df_state_count_top10,
        x="State",
        y="Total_Ins_Count",
        text_auto=True,
        title="Top 10 States by Insurance Transaction Count")

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width='stretch')

# Horizontal Bar Chart – Top Districts by Insurance Value
    st.subheader("Top 10 Districts by Insurance Transaction Value")

    df_district_top10 = (df_district_value.sort_values("District_Ins_Value", ascending=False).head(10))

    fig = px.bar(
        df_district_top10,
        x="District_Ins_Value",
        y="District",
        orientation="h",
        text_auto=True,
        title="Top 10 Districts by Insurance Transaction Value")

    st.plotly_chart(fig, width='stretch')


# Bar Chart – Top 10 Pincodes by Insurance Transaction Value
    st.subheader("Top 10 Pincodes by Insurance Transaction Value")

    df_pincode_value["Pincode"] = df_pincode_value["Pincode"].astype(str)

    fig = px.bar(
        df_pincode_value,
        x="Pincode",
        y="Pin_Ins_Value",
        text_auto=True,
        title="Top 10 Pincodes by Insurance Transaction Value")
    
    fig.update_layout(xaxis_type="category",xaxis_title="Pincode", yaxis_title="Insurance Transaction Value", xaxis_tickangle=-45)
    st.plotly_chart(fig, width='stretch')



# Line Chart – Year-wise Insurance Transaction Value Growth
    st.subheader("Year-wise Growth in Insurance Transaction Value")
    plt.figure(figsize=(10,6))
    plt.plot(df_yearly["Year"], df_yearly["Yearly_Ins_Value"], marker="o")
    plt.title("Year-wise Growth in Insurance Transaction Value")
    plt.xlabel("Year")
    plt.ylabel("Insurance Transaction Value")
    plt.grid(True)
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

# Bar + Line – Yearly Insurance Count vs Value
    st.subheader("Yearly Insurance Transaction Count and Value")

    fig, ax1 = plt.subplots(figsize=(10,6))

# Bar for Value
    ax1.bar(df_yearly['Year'], df_yearly['Yearly_Ins_Value'], color='skyblue', label='Yearly Value')
    ax1.set_ylabel("Yearly Value", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

# Line for Count
    ax2 = ax1.twinx()
    ax2.plot(df_yearly['Year'], df_yearly['Yearly_Ins_Count'], color='orange', marker='o', label='Yearly Count')
    ax2.set_ylabel("Yearly Count", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    plt.title("Yearly Insurance Transaction Count and Value")
    fig = plt.gcf()
    st.pyplot(fig)
    plt.close(fig)

