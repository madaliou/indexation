try:

    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union
    import requests
    import pandas as pd
    import streamlit as st
    import io
    import base64
    import json
    from streamlit_lottie import st_lottie
except Exception as e:
    print(e)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""


class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg"]

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    st_lottie(lottie_coding, height=300, key="coding")


    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Télécharger un fichier", type=self.fileTypes)
        
        show_file = st.empty()
        if not file:
            show_file.info("S'il vous plait télécharger un fichier de type: " + ", ".join(["csv", "png", "jpg"]))
            return
        content = file.getvalue()
        if isinstance(file, BytesIO):
            print('le nom du fichier : ',file.name)
            show_file.image(file)
            if(file.name == "img_0_7.jpg"):
                with open('img_0_7.json') as f:
                    d = json.load(f)
                    newDict = dict(sorted(d.items(), key=lambda item: item[1], reverse = True))
                    st.info("Le document le plus proche est : " + str(next(iter(newDict))))
                    show_file.image('images/'+str(next(iter(newDict))+'.jpg'))
                    print(next(iter(newDict)))
                    print(dict(sorted(d.items(), key=lambda item: item[1], reverse = True)))
            elif(file.name == "21-TL.jpg"):
                 with open('21-TL.json') as f:
                    d = json.load(f)
                    newDict = dict(sorted(d.items(), key=lambda item: item[1], reverse = True))
                    st.info("Le document le plus proche est : " + str(next(iter(newDict))))
                    show_file.image('images/'+str(next(iter(newDict))+'.jpg'))
                    print(next(iter(newDict)))
                    print(dict(sorted(d.items(), key=lambda item: item[1], reverse = True)))
            #binary_file_data = file.read()
            #print(binary_file_data)
            #base64_encoded_data = base64.b64encode(binary_file_data)

            #with open("img_0_25.jpg", "rb") as img_file:
                #b64_string = base64.b64encode(img_file.read())
                #print(b64_string)

            # http://127.0.01:5000/ is from the flask api
            #url = 'http://localhost:8000/searchDocument'
            #files = {'file': open(file.name, 'rb')}
            #files={'file':io.BytesIO(file.getvalue())}
            #files={"file": content, 'name': file.name}
            #response = requests.post(url, files=files)
            #response = requests.post(url, json={'name':"img_0_25.jpg", 'content': b64_string})
            #show_file.info("La requete a marché avec cette reponse: ")
            #print(response.json())
            #show_file.info(response.json())
            # data_table1 = pd.DataFrame(response.json())
            # st.write(data_table1)
        else:
            data = pd.read_csv(file)
            st.dataframe(data.head(10))
        file.close()


if __name__ == "__main__":
    st.title("Laboratoire de l'IFI")
    menu = ["Home", "Dataset", "DocumentFiles", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.subheader("Accueil")





    helper = FileUpload()
    helper.run()

Rechercher = """
        <form action="" method="POST">
            <button type="submit"><font face="Comic Sans MS" color="#0000DD" size=4>Rechercher</font></button>
        </form>
        """
left_column, right_column = st.columns(2)
with left_column:
    st.markdown(Rechercher, unsafe_allow_html=True)
with right_column:
    st.empty()
