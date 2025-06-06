from peewee import SqliteDatabase, Model, TextField, BigIntegerField

db = SqliteDatabase('db.sqlite3')


class User(Model):
    tg_id = BigIntegerField(unique=True)
    sub_id = TextField()

    def __repr__(self):
        return f"{self.tg_id} - {self.sub_id}"

    class Meta:
        database = db


class DBManager:

    @classmethod
    def add_user(cls, tg_id, sub_id) -> bool:
        try:
            chat, status = User.get_or_create(tg_id=tg_id, sub_id=sub_id)
            if not status:
                print(f'User {tg_id} already in db')
                return False  # чи додався - ні, постбек не відправляємо
            else:
                print(f'User {tg_id} added to database')
                return True  # чи додався - так, постбек відправляємо

        except Exception as e:
            print(f'Error: {e}')

    @classmethod
    def get_sub_id(cls, tg_id):
        user = User.get(tg_id=tg_id)
        return user.sub_id


if __name__ == "__main__":
    db.create_tables([User, ])
