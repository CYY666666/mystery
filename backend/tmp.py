import sqlite3

from crud.answer import answer_crud
from model import SessionLocal

conn = sqlite3.connect('qmyz1.db')
cursor = conn.cursor()
subject_id = 9

db = SessionLocal()
cursor.execute('SELECT * FROM id{}'.format(subject_id))
results = cursor.fetchall()
for it in results:
    dict_ = {
        'question': it[0],
        'choice': it[1],
        'subject_id': subject_id
    }
    answer_crud.create_or_update(db, dict_)

db.close()
