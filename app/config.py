import os


def get_secret(name: str) -> str | None:
    # Local development: .env / environment variables
    value = os.getenv(name)

    if value:
        return value

    # Streamlit Community Cloud
    try:
        import streamlit as st

        return st.secrets.get(name)

    except Exception:
        return None