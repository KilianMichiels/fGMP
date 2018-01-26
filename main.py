import sys
import argparse
import fetchPlaylists as fGMP

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Create parser
    parser = argparse.ArgumentParser(description='Short program with missing but useful functions for Google Play Music.')

    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('-a', '--account', help='Your email address for logging in to Google Play Music', required=True)
    required.add_argument('-p', '--password', help='Your password, generated on the security page. This is NOT your default google password.', required=True)
    required.add_argument('-f', '--function', help='The function you would like to execute.', choices=['fetch'], required=True)

    # Optional arguments
    parser.add_argument('-v', '--verbose', help='If you want to see what is happening.', action="store_true", required=False)

    # Read arguments
    args = vars(parser.parse_args())
    if args['function'] == 'fetch':
        if args['verbose']:
            fGMP.fetchPlaylists(args['account'], args['password'], True)
        else:
            fGMP.fetchPlaylists(args['account'], args['password'], False)
