from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # know what store the item belongs to
    # (do not cascade on delete, if remove corresponding store will not remove item)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # no ned to use JOINS. sees our store id, therefore we can find store in db that matches this store id
    # ManyToOne - many items to one store
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # SQLite old code:
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # SQLAlchemy:
        # SELECT * FROM items WHERE name=name LIMIT 1
        # LIMIT or .first() returns the first row only
        #returns an item model object
        return cls.query.filter_by(name=name).first()

    # for update AND insert
    def save_to_db(self):
        # aession a collection of ojects we will write to the db
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
