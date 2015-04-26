from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
seller = Table('seller', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('about_us', String(length=140)),
)

sellers = Table('sellers', post_meta,
    Column('book_id', Integer),
    Column('seller_id', Integer),
)

users = Table('users', post_meta,
    Column('book_id', Integer),
    Column('user_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('about_me', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
    Column('isSeller', BOOLEAN),
)

book = Table('book', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('isbn', INTEGER),
    Column('title', VARCHAR(length=140)),
    Column('author', VARCHAR(length=64)),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['seller'].create()
    post_meta.tables['sellers'].create()
    post_meta.tables['users'].create()
    pre_meta.tables['user'].columns['isSeller'].drop()
    pre_meta.tables['book'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['seller'].drop()
    post_meta.tables['sellers'].drop()
    post_meta.tables['users'].drop()
    pre_meta.tables['user'].columns['isSeller'].create()
    pre_meta.tables['book'].columns['user_id'].create()
