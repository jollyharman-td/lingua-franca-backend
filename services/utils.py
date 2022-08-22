import os, re
import string
import numpy as np
from config import OP_DIR, SRC_DIR

def readFile(path):
    with open(path, "r") as myfileip:
        filematerial = myfileip.readlines()
    return filematerial

def writeFile(path, data):
    with open(path, "w") as myfileop:
        # myfileop.writelines(["%s\n" % item  for item in data])
        myfileop.write('\n'.join(data))
        
def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)

def preprocess(sentence: string):

    sentence = sentence.lower()
    sentence = re.sub('([.,:;!?|()\-_"])', r' \1 ', sentence)
    sentence = re.sub('\s{2,}', ' ', sentence)
    return sentence

def translationEng2Pun():

    output_filepath = os.path.join(OP_DIR, "output_punjabi.txt")
    remove_file(output_filepath)

    os.system("python3 models/MT/helpers/2-subword.py models/MT/english-tokenizer.model models/MT/punjabi-tokenizer.model static/ip_files/input_english.txt models/MT/helpers/empty_file.txt")
    
    os.system("onmt_translate -model models/MT/english2punjabi_lat.pt -src static/ip_files/input_english.txt.subword -output static/op_files/output_punjabi.txt")
    
    os.system("python3 models/MT/helpers/3-desubword.py models/MT/punjabi-tokenizer.model static/op_files/output_punjabi.txt")

    read_output = readFile(os.path.join(OP_DIR, "output_punjabi.txt.desubword"))
    
    read_output = "".join(read_output)
    read_output = read_output.strip()
    print(read_output)
    return read_output

def translationPun2Eng():
    
    output_filepath = os.path.join(OP_DIR, "output_english.txt")
    remove_file(output_filepath)

    os.system("python3 models/MT/helpers/2-subword.py models/MT/punjabi-tokenizer.model models/MT/english-tokenizer.model static/ip_files/input_punjabi.txt models MT/helpers/empty_file.txt")
    
    os.system("onmt_translate -model models/MT/punjabi2english_lat.pt -src static/ip_files/input_punjabi.txt.subword -output static/op_files/output_english.txt")
    
    os.system("python3 models/MT/helpers/3-desubword.py models/MT/english-tokenizer.model static/op_files/output_english.txt")

    read_output = readFile(os.path.join(OP_DIR, "output_english.txt.desubword"))
    read_output = "".join(read_output)
    read_output = read_output.strip()
    print(read_output)
    return read_output