"""Initial migration - create jobs table

Revision ID: 001
Revises: 
Create Date: 2025-12-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create jobs table
    op.create_table(
        'jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('num_images', sa.Integer(), nullable=False),
        sa.Column('animal', sa.String(), nullable=True),
        sa.Column('image_urls', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_jobs_id', 'jobs', ['id'])
    op.create_index('ix_jobs_status', 'jobs', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_jobs_status', table_name='jobs')
    op.drop_index('ix_jobs_id', table_name='jobs')
    
    # Drop table
    op.drop_table('jobs')
