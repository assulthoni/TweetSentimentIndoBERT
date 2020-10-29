from django.shortcuts import render, redirect
from .crawl_tweet import *
from .models import classifier

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index-search.html')

def crawl(request):
    if request.method == 'POST':
        query = request.POST['query']
        data = get_data(query, maxTweets=10)
        if len(data) != 0:
            clf = classifier
            clf.process_tweets(tweets=data)
            result = clf.export()
            print(result)
            context = {
                'status' : f'Success got {len(data)} tweets',
                'query' : query,
                'sentiment' : result,
            }
            clf.reset()
            return render(request, 'result.html', context=context)
        else:
            context = {
                'status' : f'There is No tweet with query: {query}',
                'query' : query,
                'sentiment' : None
            }
            return render(request, 'result.html', context=context)
    else:
        return redirect('/')