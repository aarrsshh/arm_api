import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--user',
                        help="Authenicated User for ARM URL.",
                        default=None, required=True)
    common_parser.add_argument('--apikey',
                        help="API key of user to be used for authentication",
                        default=None, required=True)
    common_parser.add_argument('--armurl', required=True
                        help="JFrog ARM Server URL.")
    common_parser.add_argument('--repopath',
                        help="Repository Path where artifacts are stored",
                        default="", required=True)

    common_parser_days = argparse.ArgumentParser(add_help=False)
    common_parser_days.add_argument('--days',
                                    help='Enter the number of days. (Default is 60)',
                                    default=60)

    subparsers = parser.add_subparsers(dest="Operation")
    subparsers.add_parser('fetch_latest_version', parents=[common_parser],
                          help='Fetches the latest version on Repopath.')

    subparsers.add_parser('fetch_old_versions', parents=[common_parser, common_parser_days],
                          help='Fetches Older version from Repopath')

    subparsers.add_parser('delete_old_versions', parents=[common_parser, common_parser_days],
                          help='Deletes Older version from Repopath')
    subparsers.required = True

    args = parser.parse_args()
    return args
