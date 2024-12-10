import sqlite3
import pandas as pd
import json

def parse_text_file(filename):
    records = []
    current_record = {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '=====':
                if current_record:
                    records.append(current_record)
                    current_record = {}
            elif '::' in line:
                key, value = line.split('::', 1)
                current_record[key] = value
    
    if current_record:
        records.append(current_record)
    
    return pd.DataFrame(records)



conn = sqlite3.connect('music.db')
cursor = conn.cursor()

# Создание бд

cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    artist TEXT,
    song TEXT,
    duration_ms INTEGER,
    year INTEGER,
    tempo FLOAT,
    genre TEXT,
    loudness FLOAT,
    instrumentalness FLOAT,
    explicit BOOLEAN
)
''')

# Парсинг данных

df1 = parse_text_file('_part_1.text')
df1['explicit'] = df1['explicit'].map({'True': 1, 'False': 0})
df1['duration_ms'] = pd.to_numeric(df1['duration_ms'])
df1['year'] = pd.to_numeric(df1['year'])
df1['tempo'] = pd.to_numeric(df1['tempo'])
df1['loudness'] = pd.to_numeric(df1['loudness'])
df1['instrumentalness'] = pd.to_numeric(df1['instrumentalness'])

df2 = pd.read_csv('_part_2.csv', sep=';')
df2['explicit'] = False 
df2['instrumentalness'] = 0.0

for df in [df1, df2]:
    df[['artist', 'song', 'duration_ms', 'year', 'tempo', 'genre', 'loudness', 'instrumentalness', 'explicit']].to_sql(
        'songs', conn, if_exists='append', index=False
    )

# Составление запросов к бд

query1 = '''
SELECT *
FROM songs
ORDER BY duration_ms DESC
LIMIT 37
'''
result1 = pd.read_sql_query(query1, conn)
result1.to_json('query1_result.json', orient='records', indent=1)


query2 = '''
SELECT 
    SUM(duration_ms) as total_duration,
    MIN(duration_ms) as min_duration,
    MAX(duration_ms) as max_duration,
    AVG(duration_ms) as avg_duration
FROM songs
'''
result2 = pd.read_sql_query(query2, conn)
print("\nStatistics on duration_ms:")
print(result2)


query3 = '''
SELECT genre, COUNT(*) as frequency
FROM songs
GROUP BY genre
ORDER BY frequency DESC
'''
result3 = pd.read_sql_query(query3, conn)
print("\nGenre frequency:")
print(result3)


query4 = '''
SELECT *
FROM songs
WHERE tempo > 60
ORDER BY loudness DESC
LIMIT 42
'''
result4 = pd.read_sql_query(query4, conn)
result4.to_json('query4_result.json', orient='records', indent=1)

conn.close()