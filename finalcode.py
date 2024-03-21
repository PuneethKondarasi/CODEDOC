from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import webbrowser
from googleapiclient.discovery import build
syllabus=""
nltk.download('stopwords')

reader = PdfReader("syllabus4.pdf")
number_of_pages = len(reader.pages) 

for i in range(number_of_pages):
    page = reader.pages[i] 
    text = page.extract_text()  
    syllabus=syllabus+text

index_start_module= syllabus.find("Module:1")
index_end_module=syllabus.find("Text Book")
index_end_module_books=syllabus.find("Mode of Evaluation :")
module_NAME_index_start=syllabus.find("L T P C")
module_NAME_index_end=syllabus.find("Pre-requisite")
module_name=(syllabus[module_NAME_index_start+17:module_NAME_index_end-8])



module_content_keeper=syllabus[index_start_module:index_end_module]
book_content_keeper=syllabus[index_end_module:index_end_module_books]

lines = book_content_keeper.split('\n')
text_books = []
for line in lines:
    if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
        text_books.append(line.strip())


def extract_keywords(text, ignore_words, verbose=False):
    words = [word.strip() for word in text.split('\n')]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    

    keywords = []
    for word in words:
        if ( word.startswith('Module:')):
            if ( not word.startswith('Module:8')):
                if (not word.startswith('Total Lecture')):
                    keywords.append(word)
        elif verbose: 
            print(f"Ignored module header: {word}")

    keywords = [word for word in keywords if word.lower() not in [ignore.lower() for ignore in ignore_words]]

    return keywords
text = module_content_keeper
ignore_words = ['Proceedings of the 65th Academic Council (17.03.2022) 992Total Lecture hours: 45 hours','']
module_list = extract_keywords(text, ignore_words)  
module_list_without_hours = [module[:-7].strip() if module.endswith(' hours') else module for module in module_list] 
print(module_list_without_hours)

def open_amazon_search(search_term):
  escaped_query = search_term.replace(" ", "+") 
  url = f"https://www.amazon.com/s?k={escaped_query}"
  webbrowser.open(url) 

a = len(text_books)
if a < 4:
    pass
else:
    a = 4

for i in range(a):
    open_amazon_search(text_books[i])



API_KEY = 'AIzaSyAVMO6fN7rt6dA6_zWRs-TFlCYHchmnpqs'

def search_youtube_playlists(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    search_response = youtube.search().list(
        q=module_name + query,
        part='id,snippet',
        type='playlist',
        maxResults=2
    ).execute()

    playlists = []

    for search_result in search_response.get('items', []):
        playlist_id = search_result['id']['playlistId']
        title = search_result['snippet']['title']
        playlists.append({'title': title,
                          'playlist_id': "https://www.youtube.com/playlist?list=" + playlist_id})

    return playlists


chapter_names = module_list_without_hours
output_text = ''

for chapter_name in chapter_names:
    playlists = search_youtube_playlists(chapter_name)
    for playlist in playlists:
        output_text += f"{playlist['playlist_id']}\n"

with open('output.txt', 'w',encoding='utf-8') as file:
    file.write(output_text)