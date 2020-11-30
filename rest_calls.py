from contributor import Contributor
from metric import Metric
from exceptions import TeamFilterError, TeamMemberQueryError, UserQueryError

from functools import reduce
import json
import urllib.request
import ssl
import sys

base_url = "not_initialised" 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_results(url, token, results = []):
    if(url == None):
        return results

    headers = get_headers(token)
    req = urllib.request.Request(url, data=None, headers=headers, origin_req_host=None, unverifiable=True, method='GET')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())

        if data["count"] > 0:
            results.extend(data["results"])

        return get_results(data["next"], token, results)

    except  Exception as e:
        print("An error occurred retrieving metrics for Apex users: "+url)
        raise

def get_team(team_name, token):
    # Retrieve team details
    url = base_url + "/teams/?name="+team_name 
    headers = get_headers(token)
    req = urllib.request.Request(url, data=None, headers=headers, origin_req_host=None, unverifiable=True, method='GET')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            team_data = json.loads(response.read())
            if team_data['count'] == 1:
                return team_data['results'][0]
            else:
                raise TeamFilterError("Team request returned either zero or more than one result")
    except  Exception as e:
        print("An error occurred retrieving the team (" + team_name + ")")
        raise


def get_contributors(team, token):
    url = base_url + "/users/?team__name="+str(team["name"])
    headers = get_headers(token)
    req = urllib.request.Request(url, data=None, headers=headers, origin_req_host=None, unverifiable=True, method='GET')

    contributors = []
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            team_users = json.loads(response.read())
            if team_users['count'] != 0:
                for user in team_users['results']:
                    contributors.append(Contributor(user["id"], user["name"], user["email"], user["last_activity_at"]))

                return sorted(contributors, key=lambda k: k.name) 
            else:
                raise TeamMemberQueryError("Team member request returned zero results")
    except  Exception as e:
        print("An error occurred retrieving members for the team the team (" + team["name"] + "): ")
        raise

def add_metrics_to_all(contributors, from_date, to_date, token, date_fmt):
    ids_str = reduce(lambda id1,id2 : id1+","+id2, map(lambda contrib: str(contrib.id), contributors))
    try:
        metrics = get_metrics(ids_str, from_date, to_date, token)
        if metrics != None:
            for metric in metrics:
                user_id = metric["apex_user_id"]
                contributor = next(filter(lambda a: a.id==user_id, contributors), None)
                if contributor != None:
                    contributor.metrics.append(Metric(metric["churn_sum"], metric["haloc_sum"], metric["id_count"], metric["author_local_date_date"], metric["impact_sum"], date_fmt))
                else:
                    print(user_id)

        return contributors

    except  Exception as e:
        print("An error occurred retrieving metrics for Apex users: "+str(ids_str))
        raise

def get_metrics(user_ids, from_date, to_date, token):
    url = base_url + "/commits.agg/?limit=5000&is_merge=false&is_pr_orphan=false&haloc__lt=10000&exclude_outliers=true&smart_dedupe=true&aggregate[count]=id&aggregate[sum]=haloc,churn,impact&group_by[apex_user_id,author_local_date__date]&author_local_date__gte=" + from_date +"&author_local_date__lte=" + to_date + "&apex_user_id__in="+user_ids
    return get_results(url, token, [])

def get_headers(token):
    return {
                'Accept': 'application/json','X-CSRFToken': 'BQorR1eLLsLRozjFf4aZaAi1ZVpYvMulNkbUDJCHhRA3nc7LtuZOs3xnazaXabxB',
                'Authorization': 'Bearer '+token, 
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Host': 'flow.pluralsight.com', 
                'Cache-Control': 'no-cache'
            }

