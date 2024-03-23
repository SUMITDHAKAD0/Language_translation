import streamlit as st
import PyPDF2
from googletrans import Translator, LANGUAGES

def translate_text(text, source_lang='en', dest_lang='ur'):
    """Translates text from source language to destination language using Google Translate."""
    translator = Translator()
    try:
      return translator.translate(text, src=source_lang, dest=dest_lang).text
    except Exception as e:
      print(f"Error translating text: {e}")
      return text  # Fallback to original text on translation errors

def extract_text_from_file(file):
    """Extracts text from a PDF file."""
    if file.name.endswith(".pdf"):
      try:
        reader = PyPDF2.PdfReader(file)
        return ''.join(page.extract_text() for page in reader.pages)
      except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    else:
      st.error("Only PDF files are supported for translation.")
      return ""

def write_text_to_file(text, output_file, encoding='utf-8'):
    """Writes text to a file with specified encoding."""
    try:
      with open(output_file, 'w', encoding=encoding) as file:
        file.write(text)
    except Exception as e:
      print(f"Error writing text to file: {e}")

def main():
    """Main function for the Streamlit application."""
    st.title("Multi-Language Document and Text Translator")

    # Select source and destination languages
    col1, col2 = st.columns(2)
    with col1:
      source_lang = st.selectbox("Select Source Language", LANGUAGES.values())
    with col2:
      dest_lang = st.selectbox("Select Destination Language", LANGUAGES.values())

    # for user input
    user_input_text = st.text_input("Enter some text 👇")
    if user_input_text:
        translated_text = translate_text(user_input_text, source_lang, dest_lang)
        
        if translated_text:
            try:
              with st.expander("Translated Text", expanded=True):
                st.write(translated_text)
              st.success("Translation successful!")
              # st.balloons()

            except Exception as e:  # Exception handling block completed
                st.error(f"Error: {e}")
        else:
          st.info("Please enter text or upload a document to start translation.")


    # for doccment file    
    uploaded_file = st.file_uploader("Upload a document (PDF only) (Optional)", type=['pdf'])
    if uploaded_file:
        # Save uploaded file temporarily
        
        text_to_translate = extract_text_from_file(uploaded_file)
        translated_text = translate_text(text_to_translate, source_lang, dest_lang)
  
        if text_to_translate:
            try:
              with st.expander("Translated Text", expanded=True):
                st.write(translated_text)

              st.success("Translation successful!")
              # st.balloons()

              def convert_text_to_bytes(text):
                  return text.encode('utf-8')
              st.download_button('Download Text as TXT', data=convert_text_to_bytes(translated_text), file_name="translated.txt", mime='text/plain', key='download-txt')

            except Exception as e:  # Exception handling block completed
                st.error(f"Error: {e}")
        else:
            st.info("Please enter text or upload a document to start translation.")
    
if __name__ == "__main__":
  main()