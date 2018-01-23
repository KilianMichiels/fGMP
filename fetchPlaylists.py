# coding=utf-8
import datetime
from gmusicapi import Mobileclient
import tqdm
import sys
import argparse

def formatTrack(track, encoding):
    # Fill in the necessary fields
    Name = track['title'].encode(encoding)          if 'title'      in track else ''
    Artist = track['artist'].encode(encoding)       if 'artist'     in track else ''
    Composer = track['composer'].encode(encoding)   if 'composer'   in track else ''
    Album = track['album'].encode(encoding)         if 'album'      in track else ''
    Grouping = ''
    Work = ''
    Movement_Number = ''
    Movement_Count = ''
    Movement_Name = ''
    Genre = track['genre'].encode(encoding)         if 'genre'      in track else ''
    Size = track['estimatedSize'].encode(encoding)  if 'estimatedSize' in track else ''
    Time = str(int(float(track['durationMillis'])/1000))
    Disc_Number = str(track['discNumber'])          if 'discNumber' in track else ''
    Disc_Count = str(track['totalDiscCount'])       if 'totalDiscCount' in track else ''
    Track_Number = str(track['trackNumber'])        if 'trackNumber' in track else ''
    Track_Count = str(track['totalTrackCount'])     if track['totalTrackCount'] else ''
    Year = str(track['year'])                       if 'year' in track else ''
    Date_Modified = datetime.datetime.fromtimestamp(int(track['lastModifiedTimestamp'])/1000000.0).strftime('%d-%m-%Y %H:%M')
    Date_Added = datetime.datetime.fromtimestamp(int(track['creationTimestamp'])/1000000.0).strftime('%d-%m-%Y %H:%M')
    Bit_Rate = ''
    Sample_Rate = ''
    Volume_Adjustment = ''
    Kind = ''
    Equaliser = ''
    Comments = track['comment'].encode(encoding)    if 'comment' in track else ''
    Plays = str(track['playCount'])                 if 'playCount' in track else ''
    Last_Played = datetime.datetime.fromtimestamp(int(track['recentTimestamp'])/1000000.0).strftime('%d-%m-%Y %H:%M')
    Skips = ''
    Last_Skipped = ''
    My_Rating = str(track['rating'])                if 'rating' in track else ''
    Location = ''
    return (Name + '\t' + Artist+ '\t' + Composer+ '\t' + Album+ '\t' + Grouping+ '\t' + Work+ '\t' + Movement_Number+ '\t' + Movement_Count+ '\t' +
            Movement_Name+ '\t' + Genre+ '\t' + Size+ '\t' + Time+ '\t' + Disc_Number+ '\t' + Disc_Count+ '\t' + Track_Number+ '\t' + Track_Count+ '\t' + Year+ '\t' +
            Date_Modified+ '\t' + Date_Added+ '\t' + Bit_Rate+ '\t' + Sample_Rate+ '\t' + Volume_Adjustment+ '\t' + Kind+ '\t' + Equaliser+ '\t' + Comments+ '\t' +
            Plays+ '\t' + Last_Played+ '\t' + Skips+ '\t' + Last_Skipped+ '\t' + My_Rating+ '\t' + Location + '\n').encode(encoding)

def returnStats(failed, succes):
    if(len(succes)>0):
        print('Following playlists succeeded:')
        for playlist in succes:
            print('--> {}'.format(playlist))
    else:
        print('No playlists succeeded.')

    if(len(failed) > 0):
        print('Following playlists failed:')
        for playlist in failed:
            print('--> {}'.format(playlist))
        print('Change the name of the failed playlists and try again!')
    else:
        print('No playlists failed.')

def main(account, password, verbose_bool):

    # Set to True if you want extra information about what's happening
    VERBOSE = verbose_bool

    # Parameters for the playlist files
    XMLs = []
    Header = 'Name	Artist	Composer	Album	Grouping	Work	Movement Number	Movement Count	Movement Name	Genre	Size	Time	Disc Number	Disc Count	Track Number	Track Count	Year	Date Modified	Date Added	Bit Rate	Sample Rate	Volume Adjustment	Kind	Equaliser	Comments	Plays	Last Played	Skips	Last Skipped	My Rating	Location'
    encoding = 'utf-8'

    api = Mobileclient()
    logged_in = api.login(account, password, Mobileclient.FROM_MAC_ADDRESS)
    # logged_in is True if login was successful

    if logged_in:

        print('----------------------------------------------------')
        print('                         START                      ')
        print('----------------------------------------------------')

        if VERBOSE:
            print('Verbosity turned on...')

        # Keep track of successful and failed playlists
        succes = []
        failed = []

        # Fetch my playlists with their tracks
        playlists = api.get_all_user_playlist_contents()
        for playlist in playlists:
            # Prepare the files to write
            XMLs.append(playlist['name'] + '.txt')

        if(len(XMLs) > 0):
            print('Fetched playlists...')
        else:
            print('Playlists not fetched.')
            exit(1)

        # Fecth al the songs
        all_tracks = api.get_all_songs()

        if len(all_tracks)>0:
            if VERBOSE:
                print('Fetched songs...')
        else:
            print('Songs not fetched.')
            exit(1)

        # Start putting the tracks to the playlists
        for i, playlist in enumerate(playlists):
            try:
                # Open textfile
                myfile = open(XMLs[i], 'w')

                # If file is open
                print('Successfully opened file.')

                # Create a new string to write to file
                XML = Header + '\n'

                # Get all tracks in the playlist
                tracks_in_playlist = playlist['tracks']

                # Run over the entire playlist
                if VERBOSE:
                    print('Running over playlist {}\n'.format(playlist['name']))

                for track in tracks_in_playlist:
                    if VERBOSE:
                        print('Currently looking for {}'.format(track['trackId']))

                    # Find the track in all tracks
                    found_track = False
                    counter = 0
                    while counter < len(all_tracks)-1 and found_track == False:
                        if all_tracks[counter]['id'] == track['trackId']:
                            found_track = True
                        else:
                            counter = counter + 1
                    # Inform
                    if VERBOSE:
                        if found_track:
                            print('--> Found track with ID: {}'.format(all_tracks[counter]['id']))
                            print('--> This song is: {}'.format(all_tracks[counter]['title'].encode(encoding)))
                            print('--> And can be found in the playlist: {}\n'.format(playlist['name'].encode(encoding)))
                        else:
                            print('--> Track not found.')

                    if found_track:
                        # Add track to XML File
                        XML += formatTrack(all_tracks[counter], encoding)

                if VERBOSE:
                    print('Writing to file...')
                myfile.write(XML)

                if VERBOSE:
                    print('Done with playlist {}.\n'.format(playlist['name']))
                succes.append(XMLs[i])

            except IOError as e:
                # If file could not be opened
                print ("Error for playlist {}!".format(XMLs[i]))
                print(e)
                print('---------------------------------------')
                failed.append(XMLs[i])

        returnStats(failed, succes)

    else:
        print('Failed to log in. Please check your credentials')

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    parser = argparse.ArgumentParser(description='Short program to retrieve your playlists from Google Play Music.')
    parser.add_argument('--account', help='Your email address for logging in to Google Play Music', required=True)
    parser.add_argument('--password', help='Your password, generated on the security page. This is NOT your default google password.', required=True)
    parser.add_argument('--verbose', help='If you want to see what is happening.', action="store_true", required=False)
    args = vars(parser.parse_args())
    if(args['account'] == None):
        print('usage: python fetchPlaylists.py --account <YOUR EMAIL> --password <YOUR PASSWORD>')
    elif(args['password'] == None):
        print('usage: python fetchPlaylists.py --account <YOUR EMAIL> --password <YOUR PASSWORD>')
    else:
        if args['verbose']:
            main(args['account'], args['password'], True)
        else:
            main(args['account'], args['password'], False)
