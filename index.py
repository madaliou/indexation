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
    import cv2 as cv
    import pickle
    import tqdm
    import os
    import math
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
        self.fileTypes = ["jpeg", "png", "jpg"]

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Télécharger un fichier", type=self.fileTypes)

        prevCol1, prevCol2 = st.columns(2)

        col1, col2, col3, col4, col5 = st.columns(5)
        
        show_file = st.empty()
        if not file:
            show_file.info("S'il vous plait télécharger un fichier de type: " + ", ".join(["jpeg", "png", "jpg"]))
            return
        content = file.getvalue()
        if isinstance(file, BytesIO):
            print('le nom du fichier : ',file.name)
            with prevCol1:
                st.header("Le morceau de document à chercher ")
                st.image(file)
            #st.image(file)
            with open(os.path.join('newImages',file.name),'wb') as f:
                f.write(file.getbuffer())
            imgToQuery = cv.imread(os.path.join('newImages',file.name), cv.COLOR_BGR2RGB)

            imgToQueryToGray = cv.cvtColor(imgToQuery, cv.COLOR_RGB2GRAY)
            #sift = cv.xfeatures2d.SIFT_create()
            sift = cv.xfeatures2d.SIFT_create(nfeatures=200)

            keypoints, descriptorToQuery = sift.detectAndCompute(imgToQueryToGray, None)
            #chargement des descripteurs train et test
            # laod a pickle file
            with open("tablelsh/tableHashage.pickle", "rb") as file:
                lsh = pickle.load(file)
            finalDecompt = {}
            #with tqdm(total=len(descriptorToQuery), desc="Chargement", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            for element in descriptorToQuery:
                nn = lsh.query(element, num_results=3, distance_func="euclidean")
                for ((vec,extra_data),distance) in nn:
                    if extra_data not in finalDecompt:
                        finalDecompt[extra_data] = 1
                    else:
                        finalDecompt[extra_data] +=1
                    #pbar.update(1)
            newDict = dict(sorted(finalDecompt.items(), key=lambda item: item[1], reverse = True))
            print(newDict)
            #st.info("Le document le plus proche est : " + str(next(iter(newDict))+'.jpg'))
            #show_file = st.empty()
            #show_file.image('images/'+str(next(iter(newDict))+'.jpg'))
            
            with col1:
                st.info(str(next(iter(newDict))+' --> '+str(newDict.get(list(newDict)[0]) * 100//sum(newDict.values()))+' %'))
                st.image('images/'+str(next(iter(newDict))+'.jpg'))

            with col2:
                st.info(str(list(newDict)[1])+' --> '+str(newDict.get(list(newDict)[1]) * 100//sum(newDict.values()))+' %')
                st.image('images/'+str(list(newDict)[1])+'.jpg')

            with col3:
                st.info(str(list(newDict)[2])+' --> '+str(newDict.get(list(newDict)[2]) * 100//sum(newDict.values()))+' %')
                st.image('images/'+str(list(newDict)[2])+'.jpg')
            
            with col4:
                st.info(str(list(newDict)[3])+' --> '+str(newDict.get(list(newDict)[3]) * 100//sum(newDict.values()))+' %')
                st.image('images/'+str(list(newDict)[3])+'.jpg')
            
            with col5:
                st.info(str(list(newDict)[4])+' --> '+str(newDict.get(list(newDict)[4]) * 100//sum(newDict.values()))+' %')
                st.image('images/'+str(list(newDict)[4])+'.jpg')
        else:
            data = pd.read_csv(file)
            st.dataframe(data.head(10))
        file.close()


if __name__ == "__main__":
    st.title("Laboratoire de l'université")
    menu = ["Home", "Dataset", "DocumentFiles", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.subheader("Recherche de documents par image")
    helper = FileUpload()
    helper.run()
