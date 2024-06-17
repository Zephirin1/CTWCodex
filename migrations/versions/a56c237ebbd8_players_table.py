"""players table

Revision ID: a56c237ebbd8
Revises: 
Create Date: 2024-05-18 17:35:15.303258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a56c237ebbd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('playerName', sa.String(length=32), nullable=False),
    sa.Column('uuid', sa.String(length=256), nullable=False),
    sa.Column('arcadeData', sa.String(length=131072), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_player_arcadeData'), ['arcadeData'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_playerName'), ['playerName'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_uuid'), ['uuid'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_player_uuid'))
        batch_op.drop_index(batch_op.f('ix_player_playerName'))
        batch_op.drop_index(batch_op.f('ix_player_arcadeData'))

    op.drop_table('player')
    # ### end Alembic commands ###