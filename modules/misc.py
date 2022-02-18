from datetime import datetime, timedelta
import os
from modules import rest_api

def get_auth(args):
    auth = None
    if args.user and args.apikey:
        auth = (args.user, args.apikey)
    elif os.environ.get('ARM_USER') and os.environ.get('ARM_APIKEY'):
        auth = (os.environ.get('ARM_USER'), os.environ.get('ARM_APIKEY'))
    return auth

def sort_response(response):
    response = sorted(response, key=lambda k: k.get('lastModified', 0), reverse=True)
    return response

def latest_sorted_response(response):
    sorted_response = sort_response(response)
    return sorted_response[0]['uri']

def fetch_all_versions(args):
    auth = get_auth(args)
    try:
        api = "?list&deep=0&listFolders=1&mdTimestamps=1"
        response = rest_api.http_get("%s/api/storage/%s" % (args.armurl, args.repopath),
                                     api, auth=auth)
        return response
    except rest_api.HttpException as http_exc:
        raise ArmHttpError(http_exc) from http_exc
    except rest_api.HttpError as http_error:
        raise ArmHttpError(http_error) from http_error

def n_days_old_version(response, days):
    try:
        versions_list = []
        timestamp = datetime.now() - timedelta(days=int(days))
        timestamp = timestamp.strftime("%Y-%m-%d")
        timestamp = datetime.strptime(timestamp,"%Y-%m-%d")
        version_list = response
        for versions in version_list:
            versions['lastModified'] = versions['lastModified'].split("T")[0]
            versions['lastModified'] = datetime.strptime(versions['lastModified'],"%Y-%m-%d")
            if versions['lastModified'] <= timestamp:
                versions_list.append(versions['uri'])
        return versions_list
    except Exception as ex:
        raise ex

def filter_directories(response, filtering_directories):
    try:
        filtered_response = []
        for data in response['files']:
            if data['uri'] not in filtering_directories:
                filtered_response.append(data)
        return filtered_response
    except Exception as ex:
        raise ex

def delete_versions(args, versions):
    auth = get_auth(args)
    try:
        for version in versions:
            rest_api.http_delete("%s/%s/%s" % (args.armurl, args.repopath, version),
                                            auth=auth)
            continue
    except rest_api.HttpException as http_exc:
        raise ArmHttpError(http_exc) from http_exc
    except rest_api.HttpError as http_error:
        raise ArmHttpError(http_error) from http_error
