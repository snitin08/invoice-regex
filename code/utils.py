def convert_key_value_pairs(text):
    import re
    print(text)
    # format dd/mm/yyyy
    date_regex = re.compile('[0-9]*/\d{2}/\d{4}')
    # format of 1 item1 50.00
    item_regex = re.compile('([\d+]*) (\w+[\s\w+]) (\d*[\.]\d*)')
    # format: <text>:(optional) 123456
    invoice_regex = re.compile('(\S+[\s#: ]*)(\d+)')


    invoice_field = re.search(invoice_regex,text)
    date_field = re.search(date_regex,text)
    items_field = re.findall(item_regex,text)
    
    if invoice_field is not None:
        print(invoice_field)
        print("Invoice number",invoice_field.groups())
    if date_field is not None:
        print("Date",date_field.group())
    if item_regex is not None:
        print("Items",items_field)
    

def label_studio_to_spacy(path):
    import json
    f = open(path,'r')         
    res = json.load(f)    
    TRAIN_DATA = []
    for i in range(len(res)):
        text = res[i]['text']
        labels = res[i]['label']
        entities = {"entities":[]}
        for j in range(len(labels)):
            start = labels[j]['start']
            end = labels[j]['end']
            NER = labels[j]['labels'][0]
            entities['entities'].append((start,end,NER))
        TRAIN_DATA.append((text,entities))
    return TRAIN_DATA

def train_spacy_ner(path):
    import spacy
    TRAIN_DATA = label_studio_to_spacy(path)
    nlp=spacy.load('en_core_web_sm')
    ner=nlp.get_pipe("ner")
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    import random
    from spacy.util import minibatch, compounding
    from pathlib import Path

    # TRAINING THE MODEL
    with nlp.disable_pipes(*unaffected_pipes):

    # Training for 30 iterations
        for iteration in range(50):

            # shuufling examples  before every iteration
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                            texts,  # batch of texts
                            annotations,  # batch of annotations
                            drop=0.5,  # dropout - make it harder to memorise data
                            losses=losses,
                        )
                print("Losses", losses)
    output_dir = Path(r'E:\Nitin\RVCE\Projects\PDF-OCR\code\models')
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

    # Load the saved model and predict
   
    #doc=nlp(TRAIN_DATA[0][0])
    #for ent in doc.ents:
    #    print(ent.text,ent.label_)

def predict_entites():
    import spacy
    import random
    from spacy.util import minibatch, compounding
    from pathlib import Path
    output_dir = Path(r'E:\Nitin\RVCE\Projects\PDF-OCR\code\models')
    text = "Wings and things 1717 DUTCH BRDY ELMONT, NY 11003 THANKS CALL AGAIN 516-341-7075 #168 OUT 1 MAC&CHZ - SMALL 1.19 1 COLL GRN - SMALL 1.19 1 1 CORN BREAD 0.62 1 5 WINGS 5.75 SPCY FRY TXTL 0.75 TOTL 9.50 CASH 9.50 CHNG 0.00 THANK YOU COME AGAIN PM #1 0168 20:14 #04 MAR.19'17 REG0001"
    print("Loading from", output_dir)
    nlp_updated = spacy.load(output_dir)

    doc = nlp_updated(text)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])


#path = r'E:\Nitin\RVCE\Projects\PDF-OCR\Dataset\address_data_nlp\2020-09-05-15-38-13\result.json'
#train_spacy_ner(path)
predict_entites()



"""TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
]
"""