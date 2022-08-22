from base64 import encode
import json, os
from services.utils import translationEng2Pun, translationPun2Eng, writeFile, preprocess
from config import SRC_DIR
from flask import Blueprint, request, Response


translate_api = Blueprint("translating", __name__) # name of api file

@translate_api.route("/translating", methods=['POST'])
def translating1():

    if request.method == "POST":
        req = request.form
        text_area = req["text_area"] ## id of form is used here
        option = req["option"]
        print("*************************************1****************************************************")
        print(text_area)
        data = text_area.strip().split("\n")
        if option == '1':
            writeFile(os.path.join(SRC_DIR, "input_english.txt"), data)
            print(data)
            translatedText = translationEng2Pun()
            
        elif option == '2':
            writeFile(os.path.join(SRC_DIR, "input_punjabi.txt"), data)
            print(data)
            translatedText = translationPun2Eng()
        
        print("**************************************2****************************************************")

    data = {"translation": "done",
            "translated_text_is": translatedText}

    return Response(json.dumps(data),
                mimetype="application/json",
                status=200)
