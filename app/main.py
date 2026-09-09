# import streamlit as st    #Streamlit essentially reruns your Python script.
# from services import search_product

# def get_products_input():
#     asin = st.text_input(
#                 "Enter Amazon ASIN",
#                 placeholder="ex. B09G3HRMVB"
#         )
#     return asin


# def main():
#     st.title("Amazon Competitor Analyzer")

#     asin = get_products_input()   

#     if st.button("Search Product"):
#         try:
#             product = search_product(asin)
#             st.session_state['product'] = product
#         except Exception as error:
#             st.error(f"Error: {str(error)}")


#     if 'product' in st.session_state:
#         product = st.session_state['product']

#         st.subheader(product['title'])

#         st.write('Brand:', product['brand'])
#         st.write('Price:', product['price'], product['currency'])
#         st.write('Rating:', product['rating'])
#         st.write('Review Count:', product['reviews_count'])


# if __name__ == "__main__":
#     main()



import streamlit as st

from services import analyze_product


def main():
    st.title("Amazon Competitor Analyzer")

    asin = st.text_input(
        "Enter Amazon ASIN",
        placeholder="e.g. B0FGYCJ7NJ"
    )

    if st.button("Analyze Product"):
        if not asin.strip():
            st.warning("Please enter an ASIN.")
            return

        try:
            with st.spinner("Analyzing product and competitors..."):
                result = analyze_product(asin)

            product = result["product"]
            competitors = result["competitors"]
            analysis = result["analysis"]

            st.subheader("Main Product")

            st.write("**Title:**", product["title"])
            st.write("**Brand:**", product["brand"])
            st.write("**Price:**", product["price"], product["currency"])
            st.write("**Rating:**", product["rating"])
            st.write("**Reviews:**", product["reviews_count"])

            st.subheader("Competitors")

            for index, competitor in enumerate(competitors, start=1):
                st.write(f"### Competitor {index}")
                st.write("**Title:**", competitor["title"])
                st.write("**Brand:**", competitor["brand"])
                st.write(
                    "**Price:**",
                    competitor["price"],
                    competitor["currency"]
                )
                st.write("**Rating:**", competitor["rating"])
                st.write("**Reviews:**", competitor["reviews_count"])

            st.subheader("AI Analysis")
            st.write(analysis)

        except Exception as error:
            st.error(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()