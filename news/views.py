from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob            #library useful in processing textual data
from nltk.corpus import stopwords
import re
import nltk
from nltk.stem.porter import PorterStemmer



def home(request):
    return render(request, 'news/home.html')


# Data Cleaning
port_stem=PorterStemmer()
def stemming(content):
  stemmed_content=re.sub('[^a-zA-Z]',' ',str(content))
  stemmed_content=stemmed_content.lower()
  stemmed_content=stemmed_content.split()
  stemmed_content=[port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content=' '.join(stemmed_content)
  return stemmed_content



def get_google_news(query, num_articles=20):
    url = f"https://news.google.com/search?q={query}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve news articles: Status code {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    articles = soup.find_all('article', limit=num_articles)
    
    if not articles:
        print("No articles found. Please check the HTML structure or the search query.")
        return []
    
    news_metadata = []
    
    for idx, article in enumerate(articles, 1):
        title_tag = article.find('a', {'class': 'JtKRv'})
        if title_tag:
            title = title_tag.get_text()
            link = 'https://news.google.com' + title_tag['href'][1:]

            article_response = requests.get(link)
            if article_response.status_code != 200:
                continue
    
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
   
            paragraphs = article_soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])
            article_text_stemmed = stemming(article_text)
            
            news_metadata.append({
                'title': title,
                'link': link,
                'article_text': article_text_stemmed[:300],
            })
        else:
            print(f"Article {idx}: Title tag not found")
    
    return news_metadata



def result(request):
    if request.method == 'POST':
        key = request.POST.get('Keywords')
        if key:
            news_data = get_google_news(key)

            news_info = []
            l1 = []
            l2 = []
            l3 = []

            for idx, news in enumerate(news_data, 1):
                heading=news['article_text']
                blob=TextBlob(heading)
                a = blob.sentiment.polarity
                if a > 0:
                    senti = "Positive"
                elif a < 0:
                    senti = "Negative"
                else:
                    senti = "Neutral"
                l1.append(news['title'])
                l2.append(news['link'])
                l3.append(senti)
                
            news_info = zip(l1, l2, l3)

            context={'Headline':news_info}

            return render(request, 'news/result.html', context)
        
        else:
            return render(request, 'news/result.html', {'result': 'Key is not provided correctly'})
        
    else:
        return HttpResponse("Invalid request method", status=405)


    