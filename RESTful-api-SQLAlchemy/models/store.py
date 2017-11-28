from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # @OneToMany (1 to n) relashinship, one store has many items
    # back reference, allows store to see which items are in the items table
    # if store id in item equals its own id

    # says: we have a relashinship with ItemModel. to figure out relashionship it goes into the ItemModel
    # and sees the store id there(ForeignKey), which means one item is related to a store, 
    # therefore there could be more than one item related to the same store
    # therefore items is a list of item models 
    items = db.relationship('ItemModel', lazy='dynamic')
    # lazy='dynamic': 
    # do not go into item table and do not load each object for each table unless we specify
    # use self.items.all() instead of self.items
    # until we call json() method we are not looking into the table, so we can easily create stores

    # hence
    # creation of store is fast, calling json() method is slow

    def __init__(self, name):
        self.name = name


    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
