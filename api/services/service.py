

def create_response_category_count(category, cnt):
    list_resp = []
    for cat in category:
        resp = dict()
        resp['id'] = cat[0]
        resp['title'] = cat[1]
        list_resp.append(resp)

    for i in list_resp:
        for j in cnt:
            if j[1] == i['id']:
                i.update({'count': j[0]})
    return list_resp



