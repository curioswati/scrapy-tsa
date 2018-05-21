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
        to_date = datetime(2017, 12, 8)
        from_date = to_date - date_diff

        date_format = '%Y-%m-%d'
        from_date = datetime.strftime(from_date, date_format)
        to_date = datetime.strftime(to_date, date_format)
        tweets = twitter_api.get_twitter_data(keyword, from_date, to_date)
        if len(tweets) > 0:
            results = twitter_api.get_sentiments(tweets)
        else:
            # defines we have hit a rate limit
            results = {"status": 501, "error": "Could not find any tweets!"}
        return render_to_response('app/result.html', {'data': json.dumps(results)},
                                  context_instance=RequestContext(request))

    return JsonResponse(response)
