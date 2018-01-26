# coding=utf-8
import datetime
from gmusicapi import Mobileclient
import sys
import os

def formatTrack(track, encoding):
    """Set the track in the correct iTunes format.

    Parameters
    ----------
    track : Dictionary
        All information about the track.
    encoding : String
        Indicates which encoding to use.

    Returns
    -------
    String
        The track in iTunes format.

    """
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
    """Return a short summary of the function.

    Parameters
    ----------
    failed : Array
        Array of failed to download/create playlists.
    succes : Array
        Array of successfully created playlists.

    Returns
    -------
    None

    """
    if(len(succes)>0):
        print('Following playlists succeeded:')
        for playlist in succes:
            print('\t--> {}'.format(playlist))
        print('')
    else:
        print('No playlists succeeded.')

    if(len(failed) > 0):
        print('Following playlists failed:')
        for playlist in failed:
            print('\t--> {}'.format(playlist))
        print('\nHINT: Change the name of the failed playlists and try again!')
    else:
        print('No playlists failed.')

def login(account, password):
    """Log in to Mobile Client on Google Music.

    Parameters
    ----------
    account : String
        Account used to access the music on Google account.
    password : String
        Password generated on the security page of the Google account.

    Returns
    -------
    Bool, MobileClient
        Whether we successfully logged in and the mobile client.

    """
    api = Mobileclient()
    logged_in = api.login(account, password, Mobileclient.FROM_MAC_ADDRESS)
    return logged_in, api


def fetchPlaylists(account, password, verbose_bool):
    """Fetch the actual playlists from Google Play and save them as .txt files.

    Parameters
    ----------
    account : String
        Account used to access the music on Google account.
    password : String
        Password generated on the security page of the Google account.
    verbose_bool : Bool
        Set to True if there needs to be more output.

    Returns
    -------
    None

    """

    # Set to True if you want extra information about what's happening
    VERBOSE = verbose_bool

    # Parameters for the playlist files
    XMLs = []
    Header = 'Name	Artist	Composer	Album	Grouping	Work	Movement Number	Movement Count	Movement Name	Genre	Size	Time	Disc Number	Disc Count	Track Number	Track Count	Year	Date Modified	Date Added	Bit Rate	Sample Rate	Volume Adjustment	Kind	Equaliser	Comments	Plays	Last Played	Skips	Last Skipped	My Rating	Location'
    encoding = 'utf-8'

    # Try to log in
    logged_in, api = login(account,password)

    # logged_in is True if login was successful
    if logged_in:
        if VERBOSE:
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
            if VERBOSE:
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

        # Create subdirectory for the playlists
        directory = 'Playlists'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Start putting the tracks to the playlists
        for i, playlist in enumerate(playlists):
            try:
                # Open textfile
                myfile = open(directory + '/' + XMLs[i], 'w')

                # If file is open
                if VERBOSE:
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
                else:
                    sys.stdout.write(i*'.' + '\r')
                    sys.stdout.flush()

                succes.append(XMLs[i])

            except IOError as e:
                # If file could not be opened
                print ("Error for playlist {}!".format(XMLs[i]))
                print(e)
                print('---------------------------------------')
                failed.append(XMLs[i])
        print('')
        returnStats(failed, succes)

    else:
        print('Failed to log in. Please check your credentials')
