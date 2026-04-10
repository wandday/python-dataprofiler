import streamlit as st
import pandas as pd
import sweetviz as sv
import streamlit.components.v1 as components
import sys
import os
st.set_page_config(page_title='Data Profiler', layout='wide' )



def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024 * 1024) #or 1024**2
    return size_mb




def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv', '.xlsx'):
        return ext
    else:
        return False



#sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv, xlsx files not exceeding 10MB")
    file_error = None  # Initialize error message
    
    if uploaded_file is not None:
        st.write('Modes of Opearation')
        minimal = st.checkbox('Do you want to generate minimal report?')
        display_mode = st.radio('Display mode', 
                                options=('Primary', 'Dark', 'Orange'))

        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:          
            dark_mode = False
            orange_mode = False

        # Load and validate file
        ext = validate_file(uploaded_file)
        if ext:
            filesize = get_filesize(uploaded_file)
            if filesize <= 10:
                if ext == '.csv':
                    df = pd.read_csv(uploaded_file)
                else:
                    xl_file = pd.ExcelFile(uploaded_file)
                    sheet_tuples = tuple(xl_file.sheet_names)
                    sheet_name = st.sidebar.selectbox('Select the sheet to analyze', sheet_tuples)
                    df = xl_file.parse(sheet_name)
            else:
                file_error = f'Maximum allowed file size is 10MB. But received {filesize:.2f} MB. Please upload a smaller file.'
        else:
            file_error = 'Invalid file type. Please upload a .csv or .xlsx file.'
    else:
        pass  # Remove the info from sidebar

st.title('Data Profiler')

# Display upload message on main page if no file uploaded
if uploaded_file is None:
    st.info("Upload file")

# Display error on main page if any
if file_error:
    st.error(file_error)

# Generate and display report (outside sidebar)
if 'df' in locals() and 'minimal' in locals() and not file_error:
    with st.spinner('Generating report...'):
        report = sv.analyze(df)
        report.show_html(filepath='sweetviz_report.html', open_browser=False)
        with open('sweetviz_report.html', 'r') as f:
            html_content = f.read()
    st.success('Report generated successfully!')
    components.html(html_content, height=1000, scrolling=True)
