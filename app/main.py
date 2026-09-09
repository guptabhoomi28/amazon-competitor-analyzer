import streamlit as st

from app.services import analyze_product
from app.exceptions import (
    ProductNotFoundError,
    ScrapingError,
    LLMError,
    DatabaseError,
)


st.set_page_config(
    page_title="Amazon Competitor Analyzer",
    page_icon="📊",
    layout="wide",
)


def display_product_card(product, title="Product"):
    st.subheader(title)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Price", f"{product['currency']} {product['price']}")

    with col2:
        st.metric("Rating", f"{product['rating']} ⭐")

    with col3:
        st.metric("Reviews", f"{product['reviews_count']:,}")

    with col4:
        st.metric("Brand", product["brand"] or "N/A")

    st.write(f"**{product['title']}**")

    details = {
        "Configuration": product.get("configuration"),
        "Screen Size": product.get("screen_size"),
        "Display": product.get("display_resolution"),
        "Refresh Rate": product.get("refresh_rate"),
        "Processor": product.get("processor"),
        "Battery Life": product.get("battery_life"),
        "Operating System": product.get("operating_system"),
    }

    for name, value in details.items():
        if value:
            st.write(f"**{name}:** {value}")

    if product.get("url"):
        st.link_button("View on Amazon", product["url"])


def display_competitors(competitors):
    st.subheader("Competitor Comparison")

    if not competitors:
        st.info("No competitors found.")
        return

    rows = []

    for competitor in competitors:
        rows.append(
            {
                "Product": competitor["title"],
                "Brand": competitor["brand"],
                "Price": (
                    f"{competitor['currency']} "
                    f"{competitor['price']}"
                ),
                "Rating": competitor["rating"],
                "Reviews": competitor["reviews_count"],
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    for index, competitor in enumerate(competitors, start=1):
        with st.expander(
            f"{index}. {competitor['title']}"
        ):
            display_product_card(
                competitor,
                f"Competitor {index}",
            )


def display_analysis(analysis):
    st.subheader("🤖 AI Analysis")

    st.write("### Summary")
    st.write(analysis.summary)

    st.write("### Market Position")
    st.write(analysis.market_position)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Strengths")

        for strength in analysis.strengths:
            st.success(f"✓ {strength}")

    with col2:
        st.write("### Weaknesses")

        for weakness in analysis.weaknesses:
            st.warning(f"⚠ {weakness}")

    st.write("### Recommendations")

    for recommendation in analysis.recommendations:
        st.info(f"💡 {recommendation}")


def main():
    st.title("📊 Amazon Competitor Analyzer")

    st.caption(
        "Analyze an Amazon product and compare it with relevant competitors."
    )

    st.divider()

    asin = st.text_input(
        "Amazon ASIN",
        placeholder="Example: B0FGYCJ7NJ",
    )

    analyze_button = st.button(
        "🔍 Analyze Product",
        type="primary",
        use_container_width=True,
    )

    if not analyze_button:
        st.info(
            "Enter an Amazon ASIN above and click "
            "**Analyze Product** to begin."
        )
        return

    if not asin.strip():
        st.warning("Please enter an ASIN.")
        return

    try:
        with st.spinner(
            "Fetching product data, competitors, and AI analysis..."
        ):
            result = analyze_product(asin)

        product = result["product"]
        competitors = result["competitors"]
        analysis = result["analysis"]

        st.divider()

        display_product_card(
            product,
            "🛒 Main Product",
        )

        st.divider()

        display_competitors(competitors)

        st.divider()

        display_analysis(analysis)

    except ProductNotFoundError as error:
        st.error(f"Product not found: {error}")

    except ScrapingError as error:
        st.error(f"Amazon data retrieval failed: {error}")

    except LLMError as error:
        st.error(f"AI analysis failed: {error}")

    except DatabaseError as error:
        st.error(f"Database error: {error}")

    except Exception as error:
        st.error(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()