import nltk
import string
from nltk.corpus import stopwords
import re


def hello_world():
    print('hello world')

    
def Concatenate_text_files(Dir_list, New_file_name):     
    # Create new write file
    New_File = open(str(New_file_name) + '.txt','w')
    # Create Loop Through List of Directories
    for x in Dir_list:
        File = open(x, 'rb')
        Text = File.read()
        # Write files to new file
        New_File.write(str(Text))
        New_File.write('\n')
    # Close File
    New_File.close()
    
    return New_File
    
def create_dict_punct():
    Dict = {}
    Punct = string.punctuation
    for x in Punct:
        Dict[x] = ''
    return Dict 

def create_dict_stopwords():
    Stopwords = stopwords.words('english')                  
    Dict = {}
    for x in Stopwords:
        Dict[x] = ''
    return Dict

def strip_punctuation(Token_list):
    dict_punct = create_dict_punct()
    List = []
    for x in Token_list:
        if x not in dict_punct:
            List.append(x)
    return List
    
def strip_stop_words(Token_list):
    stop_words = create_dict_stopwords()
    List = []
    for x in Token_list:
        if x not in stop_words:
            List.append(x)
    return List

def strip_tokens_forwardSlash_x2(Token_list):
    List = []
    for token in Token_list:
        if '\\' not in token and '/' not in token:
            
            List.append(token)
    return List

def strip_two_variable_tokens(Token_list):
    List = [x for x in Token_list if len(x) > 2]
    return List

def get_isalpha(Token_list):
    List = [x for x in Token_list if x.isalpha()]
    return List

def get_unusual_english_words(Token_list):
    list_vocab = set(w.lower() for w in Token_list if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = list_vocab.difference(english_vocab)  # unclear if 'difference' is being call on a standard list obj
    return sorted(unusual)

def get_spanish_words(Token_list):
    list_vocab = set(w.lower() for w in Token_list if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.cess_esp.words())
    list_spanish_words = list_vocab.difference(english_vocab)  # unclear if 'difference' is being call on a standard list obj
    return sorted(unusual)

def create_spanish_dictionary():
    Spanish_word_dict = {}
    for x in nltk.corpus.cess_esp.words():
        Spanish_word_dict[x] = ''
    return Spanish_word_dict

def strip_spanish_words(Token_list):
    Spanish_word_dict = create_spanish_dictionary()
    List = []
    for x in Token_list:
        if x not in Spanish_word_dict:
            List.append(x)
    return List


def get_long_words(dataframe, max_length):    
    # Note, you should create an alt version for lists
    df = dataframe
    List = []
    for x in dataframe.index:   # assumes dataframe index is the word. 
        List.append(len(x))     # Catch len of word.  
    df['Len Index Word'] = List # Create col2 w/ len of word. 
    Long_words = df['Len Index Word'] > max_length  # Limit dataframe to words > 
    df_long_words = df[Long_words]
    return df_long_words

def get_synsets(List_tokens):   
    # Get synstets from a list of tokenized words.  You should clean the list beforehand. 
    List = []
    for token in List_tokens:
        Synset = nltk.corpus.wordnet.synsets(token)
        if Synset == []:
            List.append(token)
        else:
            Synset = Synset[0]
            List.append(Synset)
    return List

def clean_synset(Synset_list):
    #Return a clean version of the Synsets with punct or word Synset. 
    Synset_clean_list = []
    
    # Regex Exp - Find
    Regex = "[a-z]+\.[a-z]\.[0-9]+"
    Re_compile = re.compile(Regex)
    
    # Regex loop expression to obtain synset
    for synset in Synset_list:
        
        # Search for Regex Exp
        synset = str(synset)
        Re_search = re.search(Re_compile, synset)
        
        if Re_search == None:
            Synset_clean_list.append(synset)
        
        elif '(' not in synset:
            Synset_clean_list.append(synset)
        
        else:
            Re_group = Re_search.group()
            Re_split = Re_group.split('.')
            Synset_clean_list.append(Re_split[0])
            
    # Return Clean Synset 
    return Synset_clean_list

def get_stem_of_token(Token_list):  
    # stem is the root of the word.  This are numerous stemmers. 
    stemmer = PorterStemmer()
    Stem_list = []
    
    for x in Token_list:
        stem = stemmer.stem(x)
        Stem_list.append(stem)
        
    return Stem_list

def text_cleaning_pipeline_Single_Text_pre_tokenize(Text_raw):
    # You should make this modular, in the sense that you get to pick the strippers 
    # that get fed into the pipeline. 
    
    # Convert text to lowercase
    Text_lower = Text.lower()  
    #Tokenize text
    Text_tokenized = nltk.word_tokenize(Text_lower)
    # Strip punctuation, stopwords, words contaning //
    Text_strip_punct = strip_punctuation(Text_tokenized)
    Text_strip_stop_words = strip_stop_words(Text_strip_punct)
    Text_strip_forwardslash = strip_tokens_forwardSlash_x2(Text_strip_stop_words)
    Text_strip_two_variable_tokens = strip_two_variable_tokens(Text_strip_forwardslash)
    Text_get_isalpha = get_isalpha(Text_strip_two_variable_tokens)
    Text_strip_spanish = strip_spanish_words(Text_get_isalpha)
    return Text_strip_spanish

def word_count_frequency_table(Text):
    # Straight forward function to create a word frequency table.  Returns a dataframe object. 
    Dict = {}
    
    for x in Text:
        if x in Dict.keys():
            Dict[x] = Dict[x] + 1
        else:
            Dict[x] = 1
    
    df = pd.DataFrame(Dict, index = [1])
    df_tran = pd.DataFrame.transpose(df)
    df_final = df_tran.sort_values(1, ascending = False)
    df_rename = df_final.rename(columns = {1:'Word Count'})
    return df_rename

def Frequency_Distriubtion_plot(Text):
    Dict = {}
    
    Text = str(Text)
    
    Split_text = Text.split(' ')
    for x in Split_text:
        if x in Dict.keys():
            Dict[x] = Dict[x] + 1
        else:
            Dict[x] = 1
    
    # Create Dataframe
    
    df = pd.DataFrame(Dict, index = [1])
    df_tran = pd.DataFrame.transpose(df)
    
    # Group on Count
    
    Group = df_tran.groupby(1)[1].count()
    Historgram = Group.plot.hist(bins = 20)
    Plot = Historgram.figure
    
    return Plot

















