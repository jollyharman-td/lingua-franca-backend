import torch.nn as nn
import torch
import pickle
import re

class BiLSTMPOSTagger(nn.Module):
    def __init__(self, 
                 input_dim, 
                 embedding_dim, 
                 hidden_dim, 
                 output_dim, 
                 n_layers, 
                 bidirectional, 
                 dropout, 
                 pad_idx):
        
        super().__init__()
        
        self.embedding = nn.Embedding(input_dim, embedding_dim, padding_idx = pad_idx)
        
        self.lstm = nn.LSTM(embedding_dim, 
                            hidden_dim, 
                            num_layers = n_layers, 
                            bidirectional = bidirectional,
                            dropout = dropout if n_layers > 1 else 0)
        
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, text):

        #text = [sent len, batch size]
        
        #pass text through embedding layer
        embedded = self.dropout(self.embedding(text))
        
        #embedded = [sent len, batch size, emb dim]
        
        #pass embeddings into LSTM
        outputs, (hidden, cell) = self.lstm(embedded)
        
        #outputs holds the backward and forward hidden states in the final layer
        #hidden and cell are the backward and forward hidden and cell states at the final time-step
        
        #output = [sent len, batch size, hid dim * n directions]
        #hidden/cell = [n layers * n directions, batch size, hid dim]
        
        #we use our outputs to make a prediction of what the tag should be
        predictions = self.fc(self.dropout(outputs))
        
        #predictions = [sent len, batch size, output dim]
        
        return predictions

def clean_text(text):
    text = re.sub("।", " | ", text)
    text = re.sub('\n+', '\n', text).strip()
    text = re.sub("\s?\n\s\n\s?", "\n", text)
    text = re.sub('\n+', '\n', text).strip()
    text = re.sub(r"https?://\S+", "<URL>", text)
    text = re.sub(r"\www\.\S+\.\S+", "<URL>", text)
    pattern = r'[%,\.;:\-\/\\\[\]\{\}\|(\)"\'\*?!#&\$€¥£₹~]'
    text = re.sub(pattern, ' \g<0> ', text)
    text = re.sub('[a-zA-z]', ' ', text)
    text = re.sub("\s?\n\s?", "\n", text)
    text = re.sub(" +", " ", text)
    text = re.sub('\n+', '\n', text)
    text = re.sub(", ,", ",", text)
    return text

def save_vocab(vocab, file):
    
    output = open(file, 'wb')
    pickle.dump(vocab, output)
    output.close()

def read_vocab(path):
    pkl_file = open(path, 'rb')
    vocab = pickle.load(pkl_file)
    pkl_file.close()
    return vocab

def init_model():
    vocab_ = read_vocab('/home/hsj/Desktop/lingua/models/POS/vocab.pkl')
    tags = read_vocab('/home/hsj/Desktop/lingua/models/POS/tags.pkl')
    INPUT_DIM = len(vocab_)
    EMBEDDING_DIM = 300
    HIDDEN_DIM = 128
    OUTPUT_DIM = len(tags)
    N_LAYERS = 2
    BIDIRECTIONAL = True
    DROPOUT = 0.25
    PAD_IDX = 1

    model = BiLSTMPOSTagger(INPUT_DIM, 
                            EMBEDDING_DIM, 
                            HIDDEN_DIM, 
                            OUTPUT_DIM, 
                            N_LAYERS, 
                            BIDIRECTIONAL, 
                            DROPOUT, 
                            PAD_IDX)
    model.load_state_dict(torch.load('/home/hsj/Desktop/lingua/models/POS/pos_punjabi_bilstm', map_location=torch.device('cpu') ))
    return model, vocab_, tags

def tag_sentence(model, sentence,vocab_, tags, device='cpu'):
    output = ''
    model.eval()
    tokens = [token for token in sentence.split(' ')]

    if vocab_:
        tokens = [t for t in tokens]
        
    numericalized_tokens = [vocab_.stoi[t] for t in tokens]

    unks = [t for t, n in zip(tokens, numericalized_tokens) if n == 0]
    token_tensor = torch.LongTensor(numericalized_tokens)
    token_tensor = token_tensor.unsqueeze(-1).to(device)
    predictions = model(token_tensor)
    top_predictions = predictions.argmax(-1)
    predicted_tags = [tags.itos[t.item()] for t in top_predictions]
    
    for token, pred_tag in zip(tokens, predicted_tags):
        output += token + '//' + pred_tag + ' '
        
    return output.strip()


if __name__ == "__main__":   
    model, vocab_, tags = init_model()
    sentence = "ਕੇਂਦਰੀ ਦਿੱਲੀ ਵਿੱਚ ਆਂਧਰਾ ਭਵਨ ਦੇ ਬਾਹਰ ਗਿਟਾਰ ਰਾਓ ਆਪਣੇ ਸਾਜ ਲੈ ਕੇ ਬੈਠਾ ਹੈ ਅਤੇ ਲੋਕਾਂ ਨੂੰ ਸੰਗੀਤ ਦੀ ਸਿੱਖਿਆ ਦੇ ਰਿਹਾ ਹੈ |"
    print(tag_sentence(model, sentence, vocab_, tags))
    