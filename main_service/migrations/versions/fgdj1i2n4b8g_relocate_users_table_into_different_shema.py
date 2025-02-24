"""Relocate users table into different schema

Revision ID: 1f0ede57ccde
Revises: 9321ae1684aa
Create Date: 2025-02-06 09:24:35.461582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fgdj1i2n4b8g'
down_revision = '9321ae1684aa'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE comments DROP CONSTRAINT IF EXISTS comments_author_nickname_fkey')
    op.execute('ALTER TABLE movie_status DROP CONSTRAINT IF EXISTS movie_status_user_id_fkey')

    op.execute('DROP INDEX IF EXISTS public.ix_users_nickname CASCADE')
    op.execute('DROP INDEX IF EXISTS public.ix_users_email CASCADE')

    op.execute('DROP TABLE public.users CASCADE')

    op.execute('CREATE SCHEMA IF NOT EXISTS users_schema')

    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('nickname', sa.String(length=64), nullable=True),
        sa.Column('password', sa.String(length=512), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        schema='users_schema'
    )

    with op.batch_alter_table('users', schema='users_schema') as batch_op:
        batch_op.create_index(batch_op.f('ix_users_schema_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_schema_users_nickname'), ['nickname'], unique=True)

    op.execute(
        'ALTER TABLE comments ADD CONSTRAINT comments_author_nickname_fkey FOREIGN KEY (author_nickname) REFERENCES users_schema.users(nickname)'
    )
    op.execute(
        'ALTER TABLE movie_status ADD CONSTRAINT movie_status_user_id_fkey FOREIGN KEY (user_id) REFERENCES users_schema.users(user_id)'
    )


def downgrade():
    op.execute('ALTER TABLE comments DROP CONSTRAINT IF EXISTS comments_author_nickname_fkey')
    op.execute('ALTER TABLE movie_status DROP CONSTRAINT IF EXISTS movie_status_user_id_fkey')

    with op.batch_alter_table('users', schema='users_schema') as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_schema_users_nickname'))
        batch_op.drop_index(batch_op.f('ix_users_schema_users_email'))

    op.execute('DROP TABLE users_schema.users CASCADE')

    op.execute('DROP SCHEMA IF EXISTS users_schema')

    op.create_table('users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('nickname', sa.String(length=64), nullable=True),
        sa.Column('password', sa.String(length=512), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        schema = 'public'
    )

    with op.batch_alter_table('users', schema="public") as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_nickname'), ['nickname'], unique=True)

    op.create_foreign_key('movie_status_user_id_fkey', 'movie_status', 'users', ['user_id'], ['user_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key('comments_user_id_fkey', 'comments', 'users', ['user_id'], ['user_id'], source_schema='public', referent_schema='public')