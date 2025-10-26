import openai
import streamlit as st

openai.api_key = st.secrets["openai"]["api_key"]

def generate_optimized_content(title, content):
    prompt = f"""You are an expert SEO copywriter. Rewrite the following blog post title, meta description, and intro
    to increase click-through rates, curiosity, and engagement while keeping the main keyword intact.

    Current Title: {title}
    Excerpt: {content}

    Return JSON with:
    - title: improved title
    - meta: improved meta description (max 160 chars)
    - intro: new short intro paragraph
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    text = response.choices[0].message.content
    lines = text.split("\n")
    optimized = {
        "title": lines[0].replace("Title:", "").strip() if lines else title,
        "meta": lines[1].replace("Meta:", "").strip() if len(lines) > 1 else "",
        "intro": lines[2].replace("Intro:", "").strip() if len(lines) > 2 else "",
    }
    return optimized
