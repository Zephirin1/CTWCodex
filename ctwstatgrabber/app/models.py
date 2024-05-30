from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Player(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    playerName: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    uuid: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True)
    
    displayName: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    pageTitle: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    
    winPercent: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    winRatio: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    wins: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    losses: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    
    capDeathRatio: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    caps: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    woolsStolen: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    capSuccessRate: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    capsPerGame: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)

    kdr: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    kills: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    deaths: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    assists: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    killsPerGame: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)

    huntingKDR: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    huntingKills: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    huntingDeaths: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    huntingKillsPerGame: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)

    woolholderKDR: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    woolholderKills: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    woolholderDeaths: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)

    capPR: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    winPR: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    draws: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)

    hotbarImage1: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage2: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage3: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage4: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage5: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage6: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage7: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage8: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarImage9: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)

    hotbarAlt1: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt2: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt3: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt4: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt5: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt6: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt7: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt8: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    hotbarAlt9: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)


    def __repr__(self):
        return '<Player {}>'.format(self.playerName)