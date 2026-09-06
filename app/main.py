import streamlit as st    #Streamlit essentially reruns your Python script.
from services import search_product

def get_products_input():
    asin = st.text_input(
                "Enter Amazon ASIN",
                placeholder="ex. B09G3HRMVB"
        )
    return asin


def main():
    st.title("Amazon Competitor Analyzer")

    asin = get_products_input()   

    if st.button("Search Product"):
        try:
            product = search_product(asin)
            st.session_state['product'] = product
        except Exception as error:
            st.error(f"Error: {str(error)}")


    if 'product' in st.session_state:
        product = st.session_state['product']

        st.subheader(product['title'])

        st.write('Brand:', product['brand'])
        st.write('Price:', product['price'], product['currency'])
        st.write('Rating:', product['rating'])
        st.write('Review Count:', product['reviews_count'])


if __name__ == "__main__":
    main()