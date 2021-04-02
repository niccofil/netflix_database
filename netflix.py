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
# Create actors table
cursor.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT)")
# Link shows table to actors table
cursor.execute("""CREATE TABLE shows_actors (
    show_id INTEGER,
    actor_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES shows (id),
    FOREIGN KEY(actor_id) REFERENCES people(id)) """)
# Link shows to directors table
cursor.execute("""CREATE TABLE shows_directors (
    show_id INTEGER,
    director_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES shows (id),
    FOREIGN KEY(director_id) REFERENCES people(id)) """)
with open("netflix_titles.csv") as file:
    people = {} 
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
        # Add names with unique id to people table
        for name in names:
            if name.strip() not in people.keys():
                cursor.execute("INSERT INTO people (name) VALUES(?)", (name.strip(),))
                people[name.strip()] = cursor.lastrowid
        # Add to joint table show_id and actor_id        
        for i in range(len(actors)):
                    cursor.execute("INSERT INTO shows_actors (show_id, actor_id) VALUES(?,?)", (show_id, people[actors[i].strip()]))
        # Add to joint table show_id and director_id  
        for i in range(len(directors)):
                cursor.execute("INSERT INTO shows_directors (show_id, director_id) VALUES(?,?)", (show_id, people[directors[i].strip()]))
con.commit()
con.close()