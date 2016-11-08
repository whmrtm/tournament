#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    pg = connect()
    cursor = pg.cursor()
    cursor.execute("delete from match;")
    pg.commit()
    pg.close()


def deletePlayers():
    """Remove all the player records from the database."""
    pg = connect()
    cursor = pg.cursor()
    cursor.execute("delete from player;")
    pg.commit()
    pg.close()

def countPlayers():
    """Returns the number of players currently registered."""
    pg = connect()
    cursor = pg.cursor()
    cursor.execute(
        "select count(p_id) from player;")
    result = int(cursor.fetchone()[0])
    pg.close()
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    pg = connect()
    cursor = pg.cursor()
    cursor.execute("insert into player (name) values (%s)",(name,))
    pg.commit()
    pg.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    pg = connect()
    cursor = pg.cursor()
    cursor.execute("""
                    select p_id, 
                           name,
                           sum(case when p_id = win_id then 1 else 0 end) as wins,
                           count(match_id) as match_count
                    from player left join match
                    on p_id = win_id or p_id = lost_id
                    group by p_id
                    order by wins desc,
                             match_count asc;
                             """)
    
    result = cursor.fetchall()
    pg.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pg = connect()
    cursor = pg.cursor()
    cursor.execute(
        "insert into match (win_id, lost_id) values(%d, %d)" % (winner, loser))
    pg.commit()
    pg.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    result = []
    pS = playerStandings()
    
    for i in range(0, len(pS), 2):
            p_id1 = pS[i][0]
            name1 = pS[i][1]
            p_id2 = pS[i+1][0]
            name2 = pS[i+1][1]

            result.append((p_id1, name1, p_id2, name2))
    return result


