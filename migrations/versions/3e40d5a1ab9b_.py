"""empty message

Revision ID: 3e40d5a1ab9b
Revises: 94454da7206c
Create Date: 2020-04-11 14:03:19.754863

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3e40d5a1ab9b'
down_revision = '94454da7206c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie_director',
    sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('director_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['director_id'], ['director.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'director_id')
    )
    op.drop_constraint('movie_director_id_fkey', 'movie', type_='foreignkey')
    op.drop_column('movie', 'director_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('director_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('movie_director_id_fkey', 'movie', 'director', ['director_id'], ['id'])
    op.drop_table('movie_director')
    # ### end Alembic commands ###
