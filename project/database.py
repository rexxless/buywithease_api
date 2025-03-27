import psycopg2
db = psycopg2.connect("dbname = buy_with_ease")
cursor = db.cursor()
