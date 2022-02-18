from modules import misc
from modules import arg_parser

filtering_directories = ['/ticket', '/metadata', '/pipeline', '/index.yaml']

def fetch_latest_version(args):
    try:
        response = misc.fetch_all_versions(args)
        response = misc.filter_directories(response, filtering_directories)
        return misc.latest_sorted_response(response)
    except Exception as ex:
        raise ex

def fetch_old_versions(args):
    try:
        response = misc.fetch_all_versions(args)
        response = misc.filter_directories(response, filtering_directories)
        return misc.n_days_old_version(response, args.days)
    except Exception as ex:
        raise ex

def filter_version_do_not_delete_all_versions(args, old_versions):
    try:
        versions_list = []
        response = misc.fetch_all_versions(args)
        versions_list = response['files']
        length_of_version_list = len(versions_list)
        length_of_old_versions = len(old_versions)
        if length_of_version_list == length_of_old_versions:
            print("All Version all included in Old version so removing newest among oldest")
            del old_versions[0]
        return old_versions
    except Exception as ex:
        raise ex

def main():
    args = arg_parser.parse_args()
    if "fetch_latest_version" in args.Operation:
        version = fetch_latest_version(args)
        print("%s" % (version))
    elif "fetch_old_versions" in args.Operation:
        old_versions = fetch_old_versions(args)
        print(old_versions)
    elif "delete_old_versions" in args.Operation:
        old_versions = fetch_old_versions(args)
        if len(old_versions) > 2:
            old_versions = filter_version_do_not_delete_all_versions(args, old_versions)
            misc.delete_versions(args, old_versions)
            print(old_versions)
        else:
            print("No Old Version is present to delete")

if __name__ == "__main__":
    main()
