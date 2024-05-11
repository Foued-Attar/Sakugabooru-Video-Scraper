import requests
from bs4 import BeautifulSoup
import mysql.connector

headers = {'User-Agent': 'Mozilla/5.0'}

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password.",
        database="your_database_name"
    )

def extract_video_url(post_id):
    url = f"https://www.sakugabooru.com/post/show/{post_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        highres_link = soup.find('a', id='highres')
        if highres_link and highres_link.get('href'):
            artiste_name, anime_title = extract_artiste_and_anime_info(soup)
            return highres_link['href'], artiste_name, anime_title
    else:
        print(f"HTTP Error {response.status_code} for URL {url}")
    return None, None, None

def extract_artiste_and_anime_info(soup):
    artiste_tag = soup.find('li', class_='tag-type-artist')
    artiste_name = artiste_tag.find_all('a')[1].text.strip() if artiste_tag else None

    anime_tag = soup.find('li', class_='tag-type-copyright')
    anime_title = anime_tag.find_all('a')[1].text.strip() if anime_tag else None

    return artiste_name, anime_title

def manage_database_entries(conn, artiste_name, anime_title, video_url):
    cursor = conn.cursor()
    cursor.execute('SELECT video_id FROM videos WHERE url = %s', (video_url,))
    if cursor.fetchone():
        print(f"URL already exists in the database: {video_url}")
    else:
        if artiste_name is not None and anime_title is not None:
            artiste_id = manage_artiste(cursor, artiste_name, conn)
            anime_id = manage_anime(cursor, anime_title, conn)
            if artiste_id and anime_id:
                cursor.execute('INSERT INTO videos (url, artiste_id, anime_id) VALUES (%s, %s, %s)', (video_url, artiste_id, anime_id))
                conn.commit()
                print(f"URL inserted into the database: {video_url}")
        else:
            print("Error: Artist name or anime title missing.")
    cursor.close()

def manage_artiste(cursor, artiste_name, conn):
    cursor.execute('SELECT artiste_id FROM artistes WHERE nom_principal = %s', (artiste_name,))
    row = cursor.fetchone()
    if not row:
        cursor.execute('INSERT INTO artistes (nom_principal) VALUES (%s)', (artiste_name,))
        conn.commit()
        artiste_id = cursor.lastrowid
        print(f"New artist added with ID {artiste_id}: {artiste_name}")
        return artiste_id
    else:
        print(f"Artist already exists retrieved with ID {row[0]}: {artiste_name}")
    return row[0]

def manage_anime(cursor, anime_title, conn):
    cursor.execute('SELECT anime_id FROM animes WHERE titre_principal = %s', (anime_title,))
    row = cursor.fetchone()
    if not row:
        cursor.execute('INSERT INTO animes (titre_principal) VALUES (%s)', (anime_title,))
        conn.commit()
        anime_id = cursor.lastrowid
        print(f"New anime added with ID {anime_id}: {anime_title}")
        return anime_id
    else:
        print(f"Anime already exists retrieved with ID {row[0]}: {anime_title}")
    return row[0]

def main():
    with connect_db() as conn:
        for post_id in range(2, 29): # Modifiez la plage en conséquence
            video_url, artiste_name, anime_title = extract_video_url(post_id)
            if video_url:
                manage_database_entries(conn, artiste_name, anime_title, video_url)

if __name__ == "__main__":
    main()
