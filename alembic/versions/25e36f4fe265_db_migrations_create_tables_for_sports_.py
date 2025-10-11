"""db(migrations): create tables for sports and tournaments management

Revision ID: 25e36f4fe265
Revises: 1f88221841d6
Create Date: 2025-09-15 22:49:51.226249

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '25e36f4fe265'
down_revision: Union[str, None] = '1f88221841d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('academic_years',
    sa.Column('academic_year_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('academic_year_id')
    )
    op.create_table('age_categories',
    sa.Column('age_category_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('min_age', sa.Integer(), nullable=False),
    sa.Column('max_age', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('age_category_id')
    )
    op.create_table('rules',
    sa.Column('rule_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('unit', sa.Enum('MINUTES', 'SECONDS', 'METERS', 'PLAYERS', 'POINTS', name='unit_type_enum'), nullable=False),
    sa.PrimaryKeyConstraint('rule_id')
    )
    op.create_table('sports',
    sa.Column('sport_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('sport_id')
    )
    op.create_table('modalities',
    sa.Column('modality_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('is_team', sa.Boolean(), nullable=True),
    sa.Column('scoring_system', sa.Enum('GOALS', 'POINTS', 'TIME', 'MEDALS', name='scoring_system_enum'), nullable=False),
    sa.Column('sport_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sport_id'], ['sports.sport_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('modality_id')
    )
    op.create_table('sports_categories',
    sa.Column('sport_category_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHER', name='gender_enum', create_type=False), nullable=False),
    sa.Column('age_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['age_category_id'], ['age_categories.age_category_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('sport_category_id')
    )
    op.create_table('tournaments',
    sa.Column('tournament_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('level', sa.Enum('DISTRICT', 'PROVINCIAL', 'NATIONAL', name='tournament_level_type_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('academic_year_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['academic_year_id'], ['academic_years.academic_year_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('tournament_id')
    )
    op.create_table('venues',
    sa.Column('venue_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('venue_id')
    )
    op.create_table('disciplines',
    sa.Column('discipline_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sport_category_id', sa.Integer(), nullable=True),
    sa.Column('modality_id', sa.Integer(), nullable=True),
    sa.Column('rule_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['modality_id'], ['modalities.modality_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rule_id'], ['rules.rule_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['sport_category_id'], ['sports_categories.sport_category_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('discipline_id')
    )
    op.create_table('tournament_events',
    sa.Column('tournament_event_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('status', sa.Enum('SCHEDULED', 'ONGOING', 'COMPLETED', 'CANCELED', 'POSTPONED', name='event_status_type_enum'), nullable=False),
    sa.Column('registration_start', sa.DateTime(), nullable=False),
    sa.Column('registration_end', sa.DateTime(), nullable=False),
    sa.Column('tournament_id', sa.UUID(), nullable=False),
    sa.Column('discipline_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['discipline_id'], ['disciplines.discipline_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.tournament_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.venue_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('tournament_event_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    
    bind = op.get_bind()
    postgresql.ENUM('MINUTES', 'SECONDS', 'METERS', 'PLAYERS', 'POINTS', name='unit_type_enum').drop(bind, checkfirst=True)
    postgresql.ENUM('GOALS', 'POINTS', 'TIME', 'MEDALS', name='scoring_system_enum').drop(bind, checkfirst=True)
    postgresql.ENUM('MALE', 'FEMALE', 'OTHER', name='gender_enum').drop(bind, checkfirst=True)
    postgresql.ENUM('DISTRICT', 'PROVINCIAL', 'NATIONAL', name='tournament_level_type_enum').drop(bind, checkfirst=True)
    postgresql.ENUM('SCHEDULED', 'ONGOING', 'COMPLETED', 'CANCELED', 'POSTPONED', name='event_status_type_enum').drop(bind, checkfirst=True)
    
    op.drop_table('tournament_events')
    op.drop_table('disciplines')
    op.drop_table('venues')
    op.drop_table('tournaments')
    op.drop_table('sports_categories')
    op.drop_table('modalities')
    op.drop_table('sports')
    op.drop_table('rules')
    op.drop_table('age_categories')
    op.drop_table('academic_years')
    # ### end Alembic commands ###
