"""empty message

Revision ID: b0b1fa34074d
Revises: b3b8b599713b
Create Date: 2023-11-17 22:00:19.216303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0b1fa34074d'
down_revision = 'b3b8b599713b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('评论',
    sa.Column('CommentID', sa.Integer(), nullable=False),
    sa.Column('Content', sa.String(length=200), nullable=True),
    sa.Column('CommentTime', sa.DateTime(), nullable=True),
    sa.Column('MusicID', sa.Integer(), nullable=True),
    sa.Column('UserID', sa.String(length=11), nullable=True),
    sa.ForeignKeyConstraint(['MusicID'], ['音乐.MusicID'], ),
    sa.ForeignKeyConstraint(['UserID'], ['用户.UserID'], ),
    sa.PrimaryKeyConstraint('CommentID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('评论')
    # ### end Alembic commands ###
