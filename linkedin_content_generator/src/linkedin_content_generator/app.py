import streamlit as st
import pandas as pd
import requests

st.title("LinkedIn Post Generator")

# --- Upload CSV ---
st.subheader("📄 Upload Viral Post CSV (Optional)")
uploaded_file = st.file_uploader("Upload a CSV exported from PhantomBuster or similar", type="csv")

df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.dataframe(df.head())

    st.markdown("📌 *Note: You can download the final CSV from your PhantomBuster account.*")

# --- Input form ---
st.subheader("📝 Post Generation Inputs")

with st.form("post_form"):
    topic = st.text_input("Topic", value="AI tools for startup marketing")
    brand_voice = st.text_input("Brand Voice", value="Bold and visionary")
    cta_link = st.text_input("CTA Link", value="https://yourstartup.com")
    mission = st.text_input("Company Mission", value="Empowering startups with AI marketing tools")
    product = st.text_input("Product", value="AI-driven content generator")
    company_name = st.text_input("Company Name", value="AI Startup Hub")

    with st.expander("Optional: Add a viral post reference"):
        viral_text = st.text_area("Viral Post Text")
        likes = st.number_input("Likes", min_value=0, step=1)
        comments = st.number_input("Comments", min_value=0, step=1)
        shares = st.number_input("Shares", min_value=0, step=1)

    submitted = st.form_submit_button("Generate Post")

# --- Handle form submission ---
if submitted:
    payload = {
        "topic": topic,
        "brand_voice": brand_voice,
        "cta_link": cta_link,
        "mission": mission,
        "product": product,
        "company_name": company_name,
        "viral_post": {
            "text": viral_text,
            "metrics": {
                "likes": likes,
                "comments": comments,
                "shares": shares
            }
        } if viral_text else None
    }

    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        response = requests.post("http://localhost:8000/generate-final-post", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success("Post generated successfully!")

            final_post = result.get("final_post", "")
            st.subheader("📢 Final LinkedIn Post")
            st.write(final_post)

            with st.expander("🧠 Additional Info"):
                st.write("**Inspired By:**", result.get("inspired_by", "N/A"))
                st.write("**Brand Voice Used:**", result.get("brand_voice_used", "N/A"))
                st.write("**CTA Link:**", result.get("cta_link", "N/A"))

            # Option to download result as .txt
            txt_download = final_post.encode("utf-8")
            st.download_button(
                label="⬇️ Download Generated Post as TXT",
                data=txt_download,
                file_name="generated_linkedin_post.txt",
                mime="text/plain"
            )

        else:
            st.error(f"Failed to generate post: {response.status_code}")
            st.json(response.json())
    except Exception as e:
        st.error(f"Error: {str(e)}")