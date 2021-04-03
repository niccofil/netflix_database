import sqlite3
import csv

# Connect to database
con = sqlite3.connect("netflix.db")
# Create cursor to navigate database
cursor = con.cursor()
# Create shows table
cursor.execute("""CREATE TABLE shows (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type TEXT,
    year INTEGER,
    rating TEXT) """)
# Create people table
cursor.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT)")
# Create countries table
cursor.execute("CREATE TABLE countries(id INTEGER PRIMARY KEY, country TEXT)")
# Link shows table to actors tables
cursor.execute("""CREATE TABLE shows_actors (
    show_id INTEGER,
    actor_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES shows (id),
    FOREIGN KEY(actor_id) REFERENCES people(id))""")
# Link shows to directors tables
cursor.execute("""CREATE TABLE shows_directors (
    show_id INTEGER,
    director_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES shows (id),
    FOREIGN KEY(director_id) REFERENCES people (id))""")
# Link shows to countries tables
cursor.execute("""CREATE TABLE shows_countries (
    show_id INTEGER,
    country_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES shows (id),
    FOREIGN KEY(country_id) REFERENCES countries (id))""")

with open("netflix_titles.csv") as file:
    people = {}
    countries = {} 
    reader = csv.DictReader(file)
    for row in reader:
        shows = [row["title"], row["type"], row["release_year"], row["rating"]]
        # Insert values into shows table
        cursor.execute("INSERT INTO shows (title, type, year, rating) VALUES (?,?,?,?)", shows)
        show_id = cursor.lastrowid
        # List of actors in a given show
        actors = row["cast"].split(",")
        # List  of directors in a given show
        directors = row["director"].split(",")
        # List of actors and directors
        names = actors + directors
        # List of countries
        ctries = row["country"].split(",")
        # Add names with unique id to people table
        for name in names:
            if name.strip() not in people.keys():
                cursor.execute("INSERT INTO people (name) VALUES(?)", (name.strip(),))
                people[name.strip()] = cursor.lastrowid
        # Add countris with unique id to countries table
        for country in ctries:
            if country.strip() not in countries.keys():
                cursor.execute("INSERT INTO countries(country) VALUES(?)", (country.strip(),))
                countries[country.strip()] = cursor.lastrowid
        # Add to joint table show_id and actor_id        
        for i in range(len(actors)):
                    cursor.execute("INSERT INTO shows_actors (show_id, actor_id) VALUES(?,?)", (show_id, people[actors[i].strip()]))
        # Add to joint table show_id and director_id  
        for i in range(len(directors)):
                cursor.execute("INSERT INTO shows_directors (show_id, director_id) VALUES(?,?)", (show_id, people[directors[i].strip()]))
        # Add to joint table show_id and country_id  
        for i in range(len(ctries)):
                cursor.execute("INSERT INTO shows_countries (show_id, country_id) VALUES(?,?)", (show_id, countries[ctries[i].strip()]))
con.commit()
con.close() 