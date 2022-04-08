# Byond-API
A simple and convenient extension that can be used to work with the servers of the game Space Station 13 based on the BayStation build.

## Examples
```
from Byond_API import ByondAPI
servers = ByondAPI()
servers.add_server("ss220", ('game.ss220.space' ,7725))
server_info = servers.get_server_info("ss220")
server_revision = servers.get_server_revision("ss220")
server_manifest = servers.get_server_manifest("ss220")
```

## Info object
Vars:
    Type - Type of Info object (Info, Revision, Manifest)
    raw_data - Raw dict of data

    for Info:
        version
        mode
        can_respawn 
        can_enter
        can_vote
        ai
        host
        players_num
        station_time
        round_duration
        round_time
        map
        ticker_state
        admins_num
        players	
        admins
        active_players
    for Revision:
        gameid
        dm_version
        dm_build
        dd_verion 
        dd_build
        revision
        git_branch
        date
    for Manifest:
        manifest