"""Populate only the disposable Compose volume, with Bazarr stopped."""
import datetime
import json
import re
import sqlite3
from pathlib import Path

config = Path('/config/config/config.yaml')
s = config.read_text()
for key, value in {'theme': 'dark', 'use_sonarr': 'true', 'use_radarr': 'true'}.items():
    s, count = re.subn(rf'^  {key}: .*$', f'  {key}: {value}', s, flags=re.M)
    assert count == 1, key
s = re.sub(r'(analytics:\n  enabled:) true', r'\1 false', s)
db = sqlite3.connect('/config/db/bazarr.db')
# Refuse to alter a library that was not created by this fixture.
for table, column in [('table_shows', 'path'), ('table_movies', 'path')]:
    if db.execute(f"SELECT count(*) FROM {table} WHERE {column} NOT LIKE '/themepark-fixtures/%'").fetchone()[0]:
        raise SystemExit('Refusing to seed an existing library')

config.write_text(s)

def insert(table, **row):
    available = {r[1] for r in db.execute(f'PRAGMA table_info({table})')}
    if not available and table.endswith('_subtitles'):
        parent = 'table_episodes' if table == 'table_episodes_subtitles' else 'table_movies'
        key = 'sonarrEpisodeId' if parent == 'table_episodes' else 'radarrId'
        db.execute(f'UPDATE {parent} SET subtitles=? WHERE {key}=?',
                   (repr([[row['language'], row['path'], row['size']]]), row[key]))
        return
    row = {k: v for k, v in row.items() if k in available}
    if 'subtitles' in available:
        row.setdefault('subtitles', '[]')
    columns = ','.join(f'"{k}"' for k in row)
    db.execute(f'INSERT OR REPLACE INTO {table} ({columns}) VALUES ({",".join("?" for _ in row)})', list(row.values()))

insert('table_languages_profiles', profileId=1, name='English + Norwegian', cutoff=None,
       originalFormat=0, items=json.dumps([
           dict(id=1, language='en', hi='False', forced='False', audio_exclude='False'),
           dict(id=2, language='nb', hi='False', forced='False', audio_exclude='False')]),
       mustContain='[]', mustNotContain='[]')
db.execute("UPDATE table_settings_languages SET enabled=1 WHERE code2 IN ('en','nb')")
now = datetime.datetime.now()
for i in range(1, 36):
    title = f'Sample series {i:02}'
    common = dict(title=title, sortTitle=title.lower(), path=f'/themepark-fixtures/series/{i}',
                  profileId=1, audio_language="['English']", tags='[]', alternativeTitles='[]',
                  monitored='True' if i % 3 else 'False', year='2025', poster='', fanart='',
                  overview='Disposable theme.park sample data. No media files or external services are connected.')
    insert('table_shows', sonarrSeriesId=i, tvdbId=i, seriesType='standard', ended='False', **common)
    for j in range(1, 4):
        eid = i * 10 + j
        path = f'{common["path"]}/S01E{j:02}.mkv'
        insert('table_episodes', sonarrEpisodeId=eid, sonarrSeriesId=i, season=1, episode=j,
               title=f'Sample episode {j}', path=path, audio_language="['English']", monitored='True',
               missing_subtitles="['en', 'nb']" if j == 1 else "['nb']" if j == 2 else '[]',
               file_size=1500000000, resolution='1080p', video_codec='h264', audio_codec='aac', format='WEB-DL')
        if j > 1:
            insert('table_episodes_subtitles', id=eid, language='en', hi=False, forced=False,
                   path=path.replace('.mkv','.en.srt'), size=12000, sonarrEpisodeId=eid, sonarrSeriesId=i)
        insert('table_history', id=eid, action=1, description='English subtitles downloaded for the sample episode',
               language='en', provider='opensubtitlescom', score=345, score_out_of=360,
               sonarrEpisodeId=eid, sonarrSeriesId=i, timestamp=str(now-datetime.timedelta(days=i%7)),
               video_path=path, subtitles_path=path.replace('.mkv','.en.srt'), matched="['series', 'season', 'episode']", not_matched="['release_group']")
    common.update(title=f'Sample movie {i:02}', sortTitle=f'sample movie {i:02}', path=f'/themepark-fixtures/movies/{i}.mkv')
    insert('table_movies', radarrId=i, tmdbId=str(i), missing_subtitles="['en', 'nb']" if i%2 else '[]',
           file_size=3000000000, resolution='1080p', video_codec='h264', audio_codec='aac', format='BluRay', **common)
    if not i%2:
        insert('table_movies_subtitles', id=i, radarrId=i, language='en', hi=False, forced=False,
               path=common['path'].replace('.mkv','.en.srt'), size=14000)
    insert('table_history_movie', id=i, radarrId=i, action=1, description='English subtitles downloaded for the sample movie',
           language='en', provider='opensubtitlescom', score=110, score_out_of=120,
           timestamp=str(now-datetime.timedelta(days=i%7)), video_path=common['path'],
           matched="['title', 'year']", not_matched="['release_group']")
db.commit()
print('Seeded 35 series, 105 episodes, 35 movies, history and a language profile.')
