#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Decoding the translation prediction
# Command: python3 desubword.py <target_model_file> <target_pred_file>


import sys
import sentencepiece as spm
import spacy
nlp = spacy.load("en_core_web_lg")


target_model = sys.argv[1]
target_pred = sys.argv[2]
target_decodeded = target_pred + ".desubword"


sp = spm.SentencePieceProcessor()
sp.load(target_model)

def postprocessing(sentence):
    updated_sentence = sentence
    sent_obj = nlp(sentence)
    for i, word in enumerate(sent_obj.ents):
#         print(word.text, word.label_)
        
        if i == 0:
            if word.label_ == 'GPE' and len(word.text) <= 4:
                updated_sentence = updated_sentence.replace(word.text, word.text.upper(), 1)
            
            elif word.label_ == 'ORG' and len(word.text) <= 5:
                updated_sentence = updated_sentence.replace(word.text, word.text.upper(), 1)
        else:            
            if word.label_ == 'GPE' and len(word.text) < 4:
                updated_sentence = updated_sentence.replace( " " + word.text, " " + word.text.upper())

            elif word.label_ == 'ORG' and len(word.text) <= 5:
                updated_sentence = updated_sentence.replace( " " + word.text, " " + word.text.upper())

            elif word.label_ == 'DATE':
                pass
            else:
                for term in word.text.split():
                    updated_sentence = updated_sentence.replace( " " + term, " " + term.capitalize())
            
    sent_obj = nlp(updated_sentence)  
    for i, word in enumerate(sent_obj):
#         print(word.text, word.pos_)

        if i == 0 and word.text.islower():
            updated_sentence = updated_sentence.replace(word.text, word.text.capitalize())
            
        elif word.pos_ in ['PROPN', 'NUM'] and  word.text.islower():
            updated_sentence = updated_sentence.replace( " " + word.text, " " + word.text.capitalize())
                
    updated_sentence = updated_sentence.replace(' i ', ' I ')
    
    print('Original Sentence: ', sentence)
    print("Updated Sentence: ",updated_sentence)
    
    return updated_sentence

with open(target_pred) as pred, open(target_decodeded, "w+") as pred_decoded:
    for line in pred:
        line = line.strip().split(" ")
        line = sp.decode_pieces(line)
        line = postprocessing(line)
        pred_decoded.write(line + "\n")
        
print("Done desubwording! Output:", target_decodeded)
