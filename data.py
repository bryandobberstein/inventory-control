from models import Item, User
from inventory_control import db


base_data = (
    ("Infomacracy", "Malka Older", "Infomacracy by Malka Older. A scifi political thriller. ISBN: 0765392364 Price: $10.99", "0765392364", 10.99, 4, "Warehouse: 13O Shelf: Science Fiction"),
    ("Think Python", "Allen Downey", "Think Python by Allen Downey. A book about Python. ISBN: 1491939362 Price: $35.99", "1491939362", 35.99, 7, "Warehouse:13A Shelf: Computer Science"),
    ("How Not To Be a Boy", "Robert Webb", "How Not To Be a Boy by Robert Webb. A memoir and commentary on gender sterotypes. ISBN: 1786890097. Price $20.63.", "1786890097", 20.63, 2, "Warehouse: 16W Shelf: Memoir"),
    ("My Father's Dragon", "Ruth Stiles Gannet", "My Father's Dragon by Ruth Stiles Gannet. A boy risks his life to free a flying dragon in this beloved children’s classic and Newbery Honor Book. ISBN: 1494915049. Price $4.99", "1494915049", 4.99, 8, "Warehouse: 16G Shelf: Fantasy"),
    ("The Martian Chronicles", "Ray Bradbury", "The Martian Chronicles by Ray Bradbury. The Martian Chronicles, a seminal work in Ray Bradbury's career, whose extraordinary power and imagination remain undimmed by time's passage, is available from Simon & Schuster for the first time. ISBN: 1451678193. Price: $7.04", "1451678193", 7.04, 6, "Warehouse: 16B Shelf: Science Fiction"),
    ("Null States", "Malka Older", "Null States by Malka Older. Null States continues Campbell Award finalist Malka Older's Centenal Cycle, the near-future science fiction trilogy beginning with Infomocracy. ISBN: 0765393387 Price: $17.45.", "0765393387", 17.46, 10, "Warehouse: 13O Shelf: Science Fiction")
)

def load_data():
    for i in base_data:
        newitem = Item(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        db.session.add(newitem)
        db.session.commit()

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    load_data()

    new_user = User("Admin", "password", 1, 0)
    db.session.add(new_user)
    db.session.commit()
