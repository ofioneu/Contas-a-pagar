"""empty message

Revision ID: 98a26c16b790
Revises: 23d34429e96a
Create Date: 2020-10-14 23:04:46.341634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98a26c16b790'
down_revision = '23d34429e96a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('historico_contas', sa.Column('data_alt', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('historico_contas', 'data_alt')
    # ### end Alembic commands ###