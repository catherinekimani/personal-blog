"""delete Migration

Revision ID: 91b71e6aad72
Revises: a46610e833b9
Create Date: 2022-05-18 01:33:19.060084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b71e6aad72'
down_revision = 'a46610e833b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deletes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deletes')
    # ### end Alembic commands ###