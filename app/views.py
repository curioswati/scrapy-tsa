from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ml import test_sentiment
import get_twitter_data
import tweepy


def index(request):
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(request))


def healthcheck(request):
    '''
    return healthcheck status = 200
    '''
    response =  {
        'status' : "success"
    }
    return JsonResponse(response)

@csrf_exempt
def get_mood(request):
    '''
    return twitter_mood for a screen_name
    '''
    # import ipdb;  ipdb.set_trace()
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('app:index'))

    if request.method == 'POST':
        try:
            screen_name = request.POST.get('screen_name')
            if "@" in screen_name :
                screen_name = screen_name.split("@")[-1]

            status, tweets = get_twitter_data.get_all_tweets(screen_name)
            # status = 1
            # tweets = ['God is love', 'OpenGL on the GPU is fast', "it was a very fantastic experience"]
            if len(tweets) > 0 :
                mood = test_sentiment.call_senti(tweets)
                # mood = 0.4
                response = {"status":1001, "mood": mood}
            elif status == 2 :
                # defines that user do not have any tweets
                mood = test_sentiment.call_senti(tweets)
                response = {"status":1002, "mood": mood}
            else :
                # defines we have hit a rate limit
                mood = 0
                response = {"status":1000, "mood": mood}
            return render_to_response('app/result.html', response, context_instance=RequestContext(request))
        except tweepy.error.TweepError:
            # raise
            response = { 'status':1004 , "mood": 0 }
            return render_to_response('app/result.html', response, context_instance=RequestContext(request))

    return JsonResponse(response)
