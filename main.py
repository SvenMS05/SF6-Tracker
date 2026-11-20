import googleapiclient.discovery
from dotenv import load_dotenv
import os
import json
import sqlite3
import re

db_connect = sqlite3.connect('Video DataBase/sf6replays.db')
cursor = db_connect.cursor()

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

SF6_characters = ["Akuma", "Blanka", "Cammy", "Chun-Li", "Dhalsim", "E. Honda", "Guile", "Ken", "M. Bison", "Ryu", "Sagat", "Zangief", "Ed", "Juri", "Luke", "Marisa,", "Rashid", "Manon", "Jamie", "Kimberly", "Lily", "JP", "Dee Jay", "Mai", "Terry", "A.K.I", "Elena", "C.Viper", "Alex", "Ingrid", "Yasmine", "Arjun"]
SF6_Pro_Players = ['MenaRD', 'Shuto', 'Booce_Lee', 'KAMI', 'Punk', 'Mikex', 'Dual Kevin', 'Caba', 'NoahTheProdigy', 'LemonSoda', 'Leshar', 'Rainpro', 'kobayan', 'dible', 'AngryBird', 'Star Platinum', 'Craime', 'Dudesickle', 'NuckleDu', 'GO1', 'Bloo', 'Fuudo', 'Micky', 'えびはら', 'Lexx', 'Oil King', 'Blaz', 'Jr.', 'Hinao', 'Fujimura', 'LUGABO', 'Phenom', 'cosa', 'tako', 'Enzo', 'Shine', 'Higuchi', 'Shigematsu', 'Brayan_Job', 'DCQ', 'Wabiichi', 'Azan', 'Kawano', 'KT_DakCorgi', 'ChrisCCH', 'JAK', 'xiaohai', 'Ryukichi', 'Kazunoko', 'AdrianRD', 'NYChrisG', 'HotDog29', 'Vxbao', 'Hamad', 'Big Bird', 'Mister Crimson', 'Hikaru', 'Hibiki', 'Psycho', 'zMetra', 'あでりい', 'LeviHakai', 'JB', 'TANTANMEN', 'zabutonn', 'Kyuki', 'NL', 'Riddles', 'Zhen', 'QuetzalStrike', 'Tachikawa', 'EndingWalker', 'Chris Wong', 'Otani', 'Axel', 'inaba', 'Dogura', 'NotPedro', 'Tokido', 'Machabo', 'Torimeshi', 'kingsvega', 'Yamaguchi', 'Momochi', 'iDom', 'Noble', 'Stealth', 'ChrisT', 'Ferreras', 'Bonchan', 'Paladin', 'Kilzyou', 'SpaceBoy', 'YHC-mochi', 'gachikun', 'GranTODAKAI', 'Akutagawa', 'Nephew', 'ThatKidAusten', 'みすとめーる', 'Daigo', 'Daigo Umehara', 'Sako', 'Mago', 'Momochi', 'Nemo', 'Kazunoko', 'Itabashi Zangief', 'Bonchan', 'Gachikun', 'Problem X', 'Xian', "Itazan"]

def Youtube_Search(characters):
    for character in characters:
        youtube_request = youtube.search().list(
            part='snippet',
            q=f'{character} pro player replays sf6',
            maxResults=20,
            type='video'
        )
        response = youtube_request.execute()

        # print(response)

        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            publishTime = item['snippet']['publishTime']
            channelTitle = item['snippet']['channelTitle']
            thumbnail_url = item['snippet']['thumbnails']['maxres']['url']

            cursor.execute('''
                INSERT OR IGNORE INTO sf6replays (videoId, title, description, publishTime, channelTitle, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (video_id, title, description, publishTime, channelTitle, thumbnail_url))

def find_characters(title, characters):
    found_characters = []

    for character in characters:
        pattern = r'\b' + re.escape(character) + r'\b'

        if re.search(pattern, title, re.IGNORECASE):
            found_characters.append(character)

    return found_characters

def find_players(title, players):
    found_players = []

    for player in players:
        pattern = r'\b' + re.escape(player) + r'\b'

        if re.search(pattern, title, re.IGNORECASE):
            found_players.append(player)

    return found_players

video_cursor = cursor.execute("SELECT id, title FROM sf6replays")
videos_and_ids = video_cursor.fetchall()
for video_and_id in videos_and_ids:
    videoId = video_and_id[0]
    title = video_and_id[1]

    players_found = find_players(title, SF6_Pro_Players)
    characters_found = find_characters(title, SF6_characters)

    players_string = ", ".join(players_found)
    characters_string = ", ".join(characters_found)

    cursor.execute('''
    UPDATE sf6replays SET players = ?, characters = ? WHERE id = ?
''', (players_string, characters_string, videoId))


db_connect.commit()
db_connect.close()