import requests
import streamlit as st

BASE_URL = st.secrets["wordpress"]["url"]
USER = st.secrets["wordpress"]["username"]
APP_PASSWORD = st.secrets["wordpress"]["app_password"]

def get_posts():
    try:
        response = requests.get(f"{BASE_URL}/wp-json/wp/v2/posts?per_page=50", auth=(USER, APP_PASSWORD))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching posts: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Connection error: {e}")
        return []

def update_post(post_id, optimized):
    payload = {
        "title": optimized["title"],
        "excerpt": optimized["intro"],
        "meta": {"_aioseo_description": optimized["meta"]},
    }
    response = requests.post(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}", json=payload, auth=(USER, APP_PASSWORD))
    if response.status_code in [200, 201]:
        return True
    else:
        st.error(f"Failed to update post {post_id}: {response.text}")
        return False
