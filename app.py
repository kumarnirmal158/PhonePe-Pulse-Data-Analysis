import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_connection

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PhonePe Pulse | Home",
    layout="wide"
)

conn = get_connection()

st.title("PHONEPE PULSE DASHBOARD")

# ---------------- FILTERS ----------------
c1, c2 = st.columns([1,1])

with c1:
    year = st.selectbox(
        "Select Year",
        sorted(pd.read_sql("SELECT DISTINCT Year FROM Agg_Tran", conn)["Year"])
    )

with c2:
    quarter = st.selectbox("Select Quarter", [1,2,3,4])

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "💳 Transactions",
    "👥 Users",
    "🛡 Insurance"
])

# =========================================================
# COMMON MAP FUNCTION
# =========================================================
def india_map(df, value_col, title):
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color=value_col,
        color_continuous_scale="Turbo",
        title=title
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig

# =========================================================
# 💳 TRANSACTIONS TAB
# =========================================================
with tab1:
    q = """
    SELECT
        State,
        SUM(Transaction_count) AS txn_count,
        SUM(Transaction_amount) AS txn_value
    FROM Agg_Tran
    WHERE Year=? AND Quarter=?
    GROUP BY State
    """
    df = pd.read_sql(q, conn, params=(year, quarter))

    q1 = """
    SELECT
        Transaction_type,
        SUM(Transaction_count) AS txn_count,
        SUM(Transaction_amount) AS txn_value
    FROM Agg_Tran
    WHERE Year=? AND Quarter=?
    GROUP BY Transaction_type
    """
    df1 = pd.read_sql(q1, conn, params=(year, quarter))

# ---------------- CLEAN STATE NAMES ----------------
    df['State']=df['State'].str.replace('andaman-&-nicobar-islands','andaman & nicobar')
    df['State']=df['State'].str.replace('jammu-&-kashmir', 'jammu & kashmir')
    df['State']=df['State'].str.replace('dadra-&-nagar-haveli-&-daman-&-diu','dadra and nagar haveli and daman and diu')
    df['State']=df['State'].str.replace("-"," ")
    df['State']=df['State'].str.title()
    
    left, right = st.columns([3,1])

    with left:
        st.plotly_chart(
            india_map(df, "txn_value", f"Transaction Value — {year} Q{quarter}"),
            width="stretch"
        )
        

    with right:
        st.subheader("📊 Transactions")
        st.metric("Total Transactions", f"{df.txn_count.sum():,}")
        st.metric("Total Value (₹)", f"₹ {df.txn_value.sum():,.0f}")
        st.metric(
            "Avg. Transaction Value",
            f"₹ {int(df.txn_value.sum()/df.txn_count.sum())}"
        )

        st.subheader("Category-wise Breakdown")
        for index, row in df1.sort_values("Transaction_type", ascending=False).iterrows():
           st.markdown(
                      f"""{row['Transaction_type']} </div> <div style="font-size:26px; font-weight:700; line-height:1;"> 
                      ₹ {row['txn_value']:,.0f}  </div> </div>
        """,
        unsafe_allow_html=True )

# =========================================================
# 👥 USERS TAB
# =========================================================
with tab2:
    q = """
    SELECT
        State,
        SUM(Registered_user) AS users,
        SUM(App_opening) AS app_opens
    FROM map_users
    WHERE Year=? AND Quarter=?
    GROUP BY State
    """
    df = pd.read_sql(q, conn, params=(year, quarter))

    df["State"] = df["State"].str.replace("-", " ").str.title()

    left, right = st.columns([3,1])

    with left:
        st.plotly_chart(
            india_map(df, "users", f"Registered Users — {year} Q{quarter}"),
            width="stretch"
        )

    with right:
        st.subheader("👥 Users")
        st.metric("Total Registered Users", f"{df.users.sum():,}")
        st.metric( "Total app opens", f"{df.app_opens.sum():,}")
        # ---------------- TABS ----------------
        tab1, tab2, tab_3 = st.tabs([ "States", "Districts", "Pincodes"])
        with tab1:
            st.dataframe(
                df.sort_values("users", ascending=False).reset_index(drop=True),
                width='stretch'
            )
        with tab2:
            q = """
            SELECT
                Name AS District,
                SUM(registeredusers) AS users
            FROM top_users
            WHERE Year=? AND Quarter=? and Level='District'
            GROUP BY District
            """
            df_district = pd.read_sql(q, conn, params=(year, quarter))
            st.dataframe(
                df_district.sort_values("users", ascending=False).reset_index(drop=True),
                width='stretch'
            )
        with tab_3:
            q = """ SELECT Name AS Pincode, SUM(registeredusers) AS users
                    FROM top_users
                    WHERE Year=? AND Quarter=? AND Level='Pincode'
                    GROUP BY Name """
            df_pincode = pd.read_sql(q, conn, params=(year, quarter))
            st.dataframe(
                df_pincode.sort_values("users", ascending=False).reset_index(drop=True),
                width='stretch'
            )

# =========================================================
# 🛡 INSURANCE TAB
# =========================================================
with tab3:
    q = """
    SELECT
        State,
        SUM(Transaction_count) AS policies,
        SUM(Transaction_amount) AS premium
    FROM Agg_ins
    WHERE Year=? AND Quarter=?
    GROUP BY State
    """
    df = pd.read_sql(q, conn, params=(year, quarter))

    df["State"] = df["State"].str.replace("-", " ").str.title()

    left, right = st.columns([3,1])

    with left:
        st.plotly_chart(
            india_map(df, "policies", f"Insurance Policies — {year} Q{quarter}"),
            width="stretch"
        )

    with right:
        st.subheader("🛡 Insurance")
        st.metric("Total Policies", f"{df.policies.sum():,}")
        st.metric("Total Premium (₹)", f"₹ {df.premium.sum():,.0f}")
        st.metric(
            "Avg. Premium per Policy",
            f"₹ {int(df.premium.sum()/df.policies.sum())}" if df.policies.sum() else "₹ 0"
        )
        tab1, tab2, tab3 = st.tabs([ "States", "Districts", "Pincodes"])
        with tab1:
            st.dataframe(
                df.sort_values("policies", ascending=False).reset_index(drop=True),
                width='stretch'
            )
        with tab2:
            q = """
            SELECT  Name AS District, SUM(Transaction_count) AS policies, SUM(Transaction_amount) AS premium
            FROM top_ins
            WHERE Year=? AND Quarter=? and Level='District'
            GROUP BY Name
            """
            df_district = pd.read_sql(q, conn, params=(year, quarter))
            st.dataframe(
                df_district.sort_values("policies", ascending=False).reset_index(drop=True),
                width='stretch'
            )

        with tab3:
            q = """ SELECT Name AS Pincode, SUM(Transaction_Count) AS policies, SUM(Transaction_Amount) AS premium
                    FROM top_ins
                    WHERE Year=? AND Quarter=? AND Level='Pincode'
                    GROUP BY Name """
            df_pincode = pd.read_sql(q, conn, params=(year, quarter))
            st.dataframe(
                df_pincode.sort_values("policies", ascending=False).reset_index(drop=True),
                width='stretch'
            )

# =========================================================