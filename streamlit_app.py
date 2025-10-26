import streamlit as st
import pandas as pd
from wp_client import get_posts, update_post
from ai_optimizer import generate_optimized_content
from gsc_import import load_gsc_data

st.set_page_config(page_title="ClickBoost AI", layout="wide")

st.title("🚀 ClickBoost AI – WordPress Post Optimizer")

st.sidebar.header("⚙️ Settings")
mode = st.sidebar.radio("Optimization Mode", ["🧩 Review Mode", "⚡ Auto Mode"])
st.sidebar.info("🧩 Review Mode: Approve AI suggestions manually.\n⚡ Auto Mode: Automatically optimize low CTR posts.")
st.sidebar.markdown("---")

queries_file = st.sidebar.file_uploader("Upload Queries.csv", type="csv")
pages_file = st.sidebar.file_uploader("Upload Pages.csv", type="csv")

if queries_file and pages_file:
    queries, pages = load_gsc_data(queries_file, pages_file)
    st.sidebar.success("✅ GSC data loaded")
else:
    st.sidebar.warning("Upload Queries.csv and Pages.csv for performance insights")

st.subheader("📜 Fetching WordPress Posts")
posts = get_posts()

if not posts:
    st.error("⚠️ Could not fetch posts. Check credentials in Streamlit Secrets.")
else:
    st.success(f"Fetched {len(posts)} posts from your WordPress site.")

    df = pd.DataFrame(posts)
    df["Optimize"] = False

    if pages_file:
        df = df.merge(pages, how="left", left_on="link", right_on="Top pages").fillna(0)

    for i, row in df.iterrows():
        with st.expander(f"📝 {row['title']['rendered']}"):
            st.markdown(f"**URL:** {row['link']}")
            st.markdown(f"**CTR:** {row.get('CTR', 'N/A')} | **Position:** {row.get('Position', 'N/A')}")
            st.write(row["excerpt"]["rendered"])

            if st.button(f"Optimize Post {row['id']}", key=row['id']):
                optimized = generate_optimized_content(
                    title=row['title']['rendered'],
                    content=row['excerpt']['rendered']
                )
                st.markdown("### ✨ AI Suggestions")
                st.markdown(f"**New Title:** {optimized['title']}")
                st.markdown(f"**New Meta Description:** {optimized['meta']}")
                st.markdown(f"**New Intro:** {optimized['intro']}")

                if st.button(f"✅ Approve & Update Post {row['id']}", key=f"approve_{row['id']}"):
                    update_post(row['id'], optimized)
                    st.success("✅ Post updated successfully!")

    if mode == "⚡ Auto Mode":
        st.warning("Auto Mode will optimize all low CTR posts automatically.")
        if st.button("🚀 Run Auto Optimization"):
            for i, row in df.iterrows():
                if row.get("CTR", 100) < 2:
                    optimized = generate_optimized_content(
                        title=row['title']['rendered'],
                        content=row['excerpt']['rendered']
                    )
                    update_post(row['id'], optimized)
            st.success("✅ Auto optimization complete!")
