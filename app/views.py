import json
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from app.utils import twitter_api


def index(request):
    return render(request, 'app/index.html')


def healthcheck(request):
    '''
    return healthcheck status = 200
    '''
    response = {
        'status': "success"
    }
    return JsonResponse(response)


@csrf_exempt
def result(request):
    '''
    return twitter_mood for a screen_name
    '''
    # import ipdb;  ipdb.set_trace()
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('app:index'))

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if "@" in keyword:
            keyword = keyword.split("@")[-1]

        date_diff = timedelta(days=7)
        to_date = datetime.today().date()
        from_date = to_date - date_diff

        # tweets = twitter_api.get_twitter_data(keyword, from_date, to_date)
        tweets = [1]
        # status = 1
        if len(tweets) > 0:
            # results = twitter_api.get_sentiments(tweets)
            # [neg, neut, pos]
            results = [['d1', 3, 3, 5], ['d2', 2, 7, 7],
                       ['d3', 4, 2, 4], ['d4', 2, 5, 4],
                       ['d5', 2, 6, 4], ['d6', 3, 5, 4], ['d7', 3, 7, 6]]
        else:
            # defines we have hit a rate limit
            response = {"status": 501, "error": "Could not find any tweets!"}
        return render_to_response('app/result.html', {'data': json.dumps(results)},
                                  context_instance=RequestContext(request))

    return JsonResponse(response)
