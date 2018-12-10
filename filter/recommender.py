from filter.models import AreaHit,KeywordHit,UserMarketSettings

def areaRecommendation(setting):
    area=setting.location
    settings=UserMarketSettings.objects.filter(location=area)
    filtered_hits=[]
    areas=[]
    for set in settings:
        hits=AreaHit.objects.filter(setting=set)
        for hit in hits:
            filtered_hits.append(hit)
    filtered_hits.sort(key=lambda x:x.hit, reverse=True)
    for hit in filtered_hits:
        recommended=hit.area
        areas.append(recommended)
    return areas[:5]


def keywordRecommendation(setting):
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
