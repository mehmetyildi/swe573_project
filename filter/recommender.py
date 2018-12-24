from filter.models import AreaHit,KeywordHit,UserMarketSettings

def areaRecommendation(setting):#Recommender for area. This will be used in creating filter
    area=setting.location#take the user's area
    settings=UserMarketSettings.objects.filter(location=area)#take the settings with the users area
    filtered_hits=[]
    areas=[]
    for set in settings:#Take the area_hits for the settings and store it in filtered_hits
        hits=AreaHit.objects.filter(setting=set)
        for hit in hits:
            filtered_hits.append(hit)
    filtered_hits.sort(key=lambda x:x.hit, reverse=True)#sort the hits according to hit values.
    for hit in filtered_hits:#put the area values of areahit records stored in filtered_hits in areas array.
        recommended=hit.area
        areas.append(recommended)
    return areas[:5]#return top 5


def keywordRecommendation(setting):#Similar to area recommendation.
    market=setting.market
    settings=UserMarketSettings.objects.filter(market=market).all()
    filtered_hits=[]
    keywords=[]
    for set in settings:
        hits=KeywordHit.objects.filter(setting=set)
        for hit in hits:
            filtered_hits.append(hit)
    filtered_hits.sort(key=lambda x:x.hit, reverse=True)
    for hit in filtered_hits:
        recommended=hit.keyword
        keywords.append(recommended)
    return keywords[:5]
