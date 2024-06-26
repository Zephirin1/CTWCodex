"""Changing to storing specific stats instead of JSON

Revision ID: 3c54bb041907
Revises: a56c237ebbd8
Create Date: 2024-05-21 15:27:11.393515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c54bb041907'
down_revision = 'a56c237ebbd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('displayName', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('pageTitle', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('winPercent', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('winRatio', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('wins', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('losses', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('capDeathRatio', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('caps', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('woolsStolen', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('capSuccessRate', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('capsPerGame', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('kdr', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('kills', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('deaths', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('assists', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('killsPerGame', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('huntingKDR', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('huntingKills', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('huntingDeaths', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('huntingKillsPerGame', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('woolholderKDR', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('woolholderKills', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('woolholderDeaths', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('capPR', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('winPR', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('draws', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage1', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage2', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage3', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage4', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage5', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage6', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage7', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage8', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarImage9', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt1', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt2', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt3', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt4', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt5', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt6', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt7', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt8', sa.String(length=32), nullable=False))
        batch_op.add_column(sa.Column('hotbarAlt9', sa.String(length=32), nullable=False))
        batch_op.drop_index('ix_player_arcadeData')
        batch_op.create_index(batch_op.f('ix_player_assists'), ['assists'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_capDeathRatio'), ['capDeathRatio'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_capPR'), ['capPR'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_capSuccessRate'), ['capSuccessRate'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_caps'), ['caps'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_capsPerGame'), ['capsPerGame'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_deaths'), ['deaths'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_displayName'), ['displayName'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_draws'), ['draws'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt1'), ['hotbarAlt1'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt2'), ['hotbarAlt2'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt3'), ['hotbarAlt3'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt4'), ['hotbarAlt4'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt5'), ['hotbarAlt5'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt6'), ['hotbarAlt6'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt7'), ['hotbarAlt7'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt8'), ['hotbarAlt8'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarAlt9'), ['hotbarAlt9'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage1'), ['hotbarImage1'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage2'), ['hotbarImage2'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage3'), ['hotbarImage3'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage4'), ['hotbarImage4'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage5'), ['hotbarImage5'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage6'), ['hotbarImage6'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage7'), ['hotbarImage7'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage8'), ['hotbarImage8'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_hotbarImage9'), ['hotbarImage9'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_huntingDeaths'), ['huntingDeaths'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_huntingKDR'), ['huntingKDR'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_huntingKills'), ['huntingKills'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_huntingKillsPerGame'), ['huntingKillsPerGame'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_kdr'), ['kdr'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_kills'), ['kills'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_killsPerGame'), ['killsPerGame'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_losses'), ['losses'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_pageTitle'), ['pageTitle'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_winPR'), ['winPR'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_winPercent'), ['winPercent'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_winRatio'), ['winRatio'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_wins'), ['wins'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_woolholderDeaths'), ['woolholderDeaths'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_woolholderKDR'), ['woolholderKDR'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_woolholderKills'), ['woolholderKills'], unique=False)
        batch_op.create_index(batch_op.f('ix_player_woolsStolen'), ['woolsStolen'], unique=False)
        batch_op.drop_column('arcadeData')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('arcadeData', sa.VARCHAR(length=131072), nullable=False))
        batch_op.drop_index(batch_op.f('ix_player_woolsStolen'))
        batch_op.drop_index(batch_op.f('ix_player_woolholderKills'))
        batch_op.drop_index(batch_op.f('ix_player_woolholderKDR'))
        batch_op.drop_index(batch_op.f('ix_player_woolholderDeaths'))
        batch_op.drop_index(batch_op.f('ix_player_wins'))
        batch_op.drop_index(batch_op.f('ix_player_winRatio'))
        batch_op.drop_index(batch_op.f('ix_player_winPercent'))
        batch_op.drop_index(batch_op.f('ix_player_winPR'))
        batch_op.drop_index(batch_op.f('ix_player_pageTitle'))
        batch_op.drop_index(batch_op.f('ix_player_losses'))
        batch_op.drop_index(batch_op.f('ix_player_killsPerGame'))
        batch_op.drop_index(batch_op.f('ix_player_kills'))
        batch_op.drop_index(batch_op.f('ix_player_kdr'))
        batch_op.drop_index(batch_op.f('ix_player_huntingKillsPerGame'))
        batch_op.drop_index(batch_op.f('ix_player_huntingKills'))
        batch_op.drop_index(batch_op.f('ix_player_huntingKDR'))
        batch_op.drop_index(batch_op.f('ix_player_huntingDeaths'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage9'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage8'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage7'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage6'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage5'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage4'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage3'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage2'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarImage1'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt9'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt8'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt7'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt6'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt5'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt4'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt3'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt2'))
        batch_op.drop_index(batch_op.f('ix_player_hotbarAlt1'))
        batch_op.drop_index(batch_op.f('ix_player_draws'))
        batch_op.drop_index(batch_op.f('ix_player_displayName'))
        batch_op.drop_index(batch_op.f('ix_player_deaths'))
        batch_op.drop_index(batch_op.f('ix_player_capsPerGame'))
        batch_op.drop_index(batch_op.f('ix_player_caps'))
        batch_op.drop_index(batch_op.f('ix_player_capSuccessRate'))
        batch_op.drop_index(batch_op.f('ix_player_capPR'))
        batch_op.drop_index(batch_op.f('ix_player_capDeathRatio'))
        batch_op.drop_index(batch_op.f('ix_player_assists'))
        batch_op.create_index('ix_player_arcadeData', ['arcadeData'], unique=False)
        batch_op.drop_column('hotbarAlt9')
        batch_op.drop_column('hotbarAlt8')
        batch_op.drop_column('hotbarAlt7')
        batch_op.drop_column('hotbarAlt6')
        batch_op.drop_column('hotbarAlt5')
        batch_op.drop_column('hotbarAlt4')
        batch_op.drop_column('hotbarAlt3')
        batch_op.drop_column('hotbarAlt2')
        batch_op.drop_column('hotbarAlt1')
        batch_op.drop_column('hotbarImage9')
        batch_op.drop_column('hotbarImage8')
        batch_op.drop_column('hotbarImage7')
        batch_op.drop_column('hotbarImage6')
        batch_op.drop_column('hotbarImage5')
        batch_op.drop_column('hotbarImage4')
        batch_op.drop_column('hotbarImage3')
        batch_op.drop_column('hotbarImage2')
        batch_op.drop_column('hotbarImage1')
        batch_op.drop_column('draws')
        batch_op.drop_column('winPR')
        batch_op.drop_column('capPR')
        batch_op.drop_column('woolholderDeaths')
        batch_op.drop_column('woolholderKills')
        batch_op.drop_column('woolholderKDR')
        batch_op.drop_column('huntingKillsPerGame')
        batch_op.drop_column('huntingDeaths')
        batch_op.drop_column('huntingKills')
        batch_op.drop_column('huntingKDR')
        batch_op.drop_column('killsPerGame')
        batch_op.drop_column('assists')
        batch_op.drop_column('deaths')
        batch_op.drop_column('kills')
        batch_op.drop_column('kdr')
        batch_op.drop_column('capsPerGame')
        batch_op.drop_column('capSuccessRate')
        batch_op.drop_column('woolsStolen')
        batch_op.drop_column('caps')
        batch_op.drop_column('capDeathRatio')
        batch_op.drop_column('losses')
        batch_op.drop_column('wins')
        batch_op.drop_column('winRatio')
        batch_op.drop_column('winPercent')
        batch_op.drop_column('pageTitle')
        batch_op.drop_column('displayName')

    # ### end Alembic commands ###
