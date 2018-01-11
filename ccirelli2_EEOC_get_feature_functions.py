import re
import bs4
from bs4 import BeautifulSoup
import string

def get_Dates(Dir_list):
    
    # Regex to ID Date
    Date_regex = re.compile('[0-9]*-[0-9]*-[0-9]*')
        
    # List to Catch Date    
    List_date = []
    
    # Get Dates
    for x in Dir_list:    
        File = open(x, 'rb')                                # Read file
        bsObj = BeautifulSoup(File.read(), 'lxml')    # Create bs4 object
        P1 = bsObj.find('p')                          # Obtain first <p>
        if P1 != None:
            P1_text = P1.get_text()                       # Obtain txt from first <p>
            Date_search = re.search(Date_regex, P1_text)    
            if Date_search == None:
                List_date.append('None Value')
            else:
                Date_match = Date_search.group()              # Resulting date
                List_date.append(Date_match)                  # Append result to list. 
    
    return List_date


def get_Titles(Dir_list):
    
    # List to Catch Date    
    List_titles = []

    for x in Dir_list:
        File = open(x, 'rb')                                # Read file
        bsObj = BeautifulSoup(File.read(), 'lxml')    # Create bs4 object
        p1 = bsObj.find('h1')                          # Obtain first <p>
        
        if p1 == None:
            List_titles.append('None Value')
        else:
            #Drop tags
            Title_1 = str(p1)
            Title_2 = Title_1.replace('<h1>', '')
            Title_3 = Title_2.replace('</h1>', '')   
            List_titles.append(Title_3)
            
    return List_titles



def get_Company_Name(Dir_list):
    # List Catch Company Name
    Company_name = []
    Pattern_name = []
    
    # List Word Expressions
    List_Word_expr = ['sued by', 'sued', 'sues', 'sued by', 'sued for', 'agrees', 'to pay', 'pays', 'settles', 'will pay', 
                        'to settle', 'pays', 'refused to', 'agrees to', 'against', 'accuses', 
                     'reach settlement', 'settle', 'resolves', 'EEOC and', 'and EEOC', 
                      'failed to hire', 'in contempt', 'Court Orders', 'Pagará', 'Pagara', 'Resuelve', 
                     'Demandado por', 'Demandada por', 'EEOC Sues', 'EEOC acuses', 'EEOC Alleges']
    
    # List Regex Expressions
    List_Regex_exp = ['v\..*No\.']
        
    # Create bs4Obj
    for x in Dir_list:
        File = open(x, 'rb')
        bs4Obj = BeautifulSoup(File.read(), 'lxml')
        
        # Create Objects
        text = bs4Obj.get_text().lower()
        h1 = bs4Obj.find('h1')
        if h1 != None:
            h1_text = h1.get_text().lower()                                # Used for word search. 
        else:
            Company_name.append('None Type Found')
        
        # Set Match
        match = False
                
        # Word Expression Search
        for expression in List_Word_expr:
            expression = expression.lower()
            if expression in h1_text:
                Split_h1 = h1_text.split(expression)
                if expression == 'against' or 'eeoc alleges':
                    #or 'court orders' or 'eeoc sues' or 'eeoc acuses' or 'eeoc alleges' or 'eeoc and'
                    Company_name.append(string.capwords(Split_h1[1]))
                    Pattern_name.append(expression)
                    match = True
                    break
                else:
                    Company_name.append(string.capwords(Split_h1[0]))                  # If not against, capture the break on 0. 
                    Pattern_name.append(expression)
                    match = True
                    break
        
        # Regex Expression Search:
        if match == False:  
            for expression in List_Regex_exp:
                expression = expression.lower()
                Regex = re.compile(expression)
                Regex_search_eeoc = re.search(Regex, text)
    
                if Regex_search_eeoc != None:                           # If equal to None, go to Word Exp Search.  
                    Regex_group_eeoc = Regex_search_eeoc.group()
                    Clean_group_1 = Regex_group_eeoc.replace('v.', '')
                    Clean_group_2 = Clean_group_1.replace('civil action', '')
                    Clean_group_3 = Clean_group_2.replace('No.', '')
                    Company_name.append(string.capwords(Clean_group_3))
                    Pattern_name.append(str(Regex))                       # Capture pattern that generated the match
                    match = True
                    break         
        
        # Match still False
        if match == False:
            Company_name.append('No Match Found')
            Pattern_name.append('No Match Found')

        
        # Note that this structure allows us to plug in an inumerable number of expression searches without breaking the code. 
        # The for statement just runs the list.  None of our lead in if statements has an else, so the code just dies if 
        # no match is found and goes to the next for expression. 
    
    # Create Dataframe
    
    #df = pd.DataFrame(Company_name, Pattern_name)
    
    return Company_name


def get_Location(Dir_list):
    
    List_company_locations = []
    
    for x in Dir_list:       
        File_open = open(x, 'rb')
        File = File_open.read()
        File_text = str(File)
        
        Regex_exp_list = []
        
        Regex_exp = re.compile(r'<p>[A-Za-z.]+.[A-Za-z]+')
        Regex_search = re.search(Regex_exp, File_text)
            
        if Regex_search != None:
            Regex_group = Regex_search.group()
            Company_name = Regex_group.replace('<p>', '')
            List_company_locations.append(Company_name)
        else:
            List_company_locations.append('None Value')
        
    return List_company_locations



def get_loss_value(Dir_list):
    
    # List to append values
    List = []
    
    # Open Text
    for x in Dir_list:       
        File_open = open(x, 'rb')
        File = File_open.read()
        File_text = str(File)
        match = False
        
        # Try Expression #1
        Regex_exp_1 = re.compile('\$[0-9]+,[0-9]+,*[0-9]*')
        Regex_search_1 = re.search(Regex_exp_1, File_text)
        
        if Regex_search_1 != None:
            Loss_value = Regex_search_1.group()
            List.append(Loss_value)
            match = True
                
        # Try Expression #2
        if match == False:
            Regex_exp_2 = re.compile('\$[0-9]+.Million')
            Regex_search_2 = re.search(Regex_exp_2, File_text)
            
            if Regex_search_2 != None:
                Loss_value = Regex_search_2.group()
                List.append(Loss_value)
                match = True

        # Try Expression #3
        if match == False:
            Regex_exp_2 = re.compile('\$[0-9]+\.[0-9]+.Million')
            Regex_search_2 = re.search(Regex_exp_2, File_text)
            
            if Regex_search_2 != None:
                Loss_value = Regex_search_2.group()
                List.append(Loss_value)
                match = True
        
        
        # Match Not found
        if match == False:
            List.append('No Value Found') 
            
    return List







