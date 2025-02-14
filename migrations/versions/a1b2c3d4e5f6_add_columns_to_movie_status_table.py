from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '1f0ede57ccde'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('movie_status', sa.Column('watched_date', sa.DateTime(), nullable=True))
    op.add_column('movie_status', sa.Column('movie_title', sa.String(length=256), nullable=True))

def downgrade():
    op.drop_column('movie_status', 'watched_date')
    op.drop_column('movie_status', 'movie_title')