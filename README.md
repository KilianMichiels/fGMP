# fetchGoogleMusicPlaylists
Small program to fetch the google play music playlists and format them to iTunes playlists.

This program uses the [gmusicapi](https://pypi.python.org/pypi/gmusicapi/10.1.2) from [Simon Weber](https://github.com/simon-weber) to fetch the correct data.

# Use
- Simply create a password on your [google account security page](https://myaccount.google.com/security) for less secure apps.
- Run the script as follows: ```python fetchPlaylists.py --account ACCOUNT --password PASSWORD```
- Your playlists will be written to textfiles which you can add to iTunes.

## Help
For more help, simply type ```python fetchPlaylists.py -h``` in your terminal.
