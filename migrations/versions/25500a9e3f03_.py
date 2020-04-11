"""empty message

Revision ID: 25500a9e3f03
Revises:
Create Date: 2020-04-11 12:14:55.146243

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '25500a9e3f03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cast_member',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('full_name', sa.String(length=240), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('first_name'),
    sa.UniqueConstraint('full_name'),
    sa.UniqueConstraint('last_name')
    )
    op.create_table('director',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('full_name', sa.String(length=240), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('first_name'),
    sa.UniqueConstraint('full_name'),
    sa.UniqueConstraint('last_name')
    )
    op.create_table('genre',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('genre', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('genre')
    )
    op.create_table('movie_origin',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('origin', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('origin')
    )
    op.create_table('movie',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('release_year', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('wikipedia_link', sa.String(length=500), nullable=True),
    sa.Column('director_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('origin_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('genre_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['director.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['origin_id'], ['movie_origin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie_cast_member',
    sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('cast_member_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['cast_member_id'], ['cast_member.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'cast_member_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_cast_member')
    op.drop_table('movie')
    op.drop_table('movie_origin')
    op.drop_table('genre')
    op.drop_table('director')
    op.drop_table('cast_member')
    # ### end Alembic commands ###