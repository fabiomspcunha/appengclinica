"""att

Revision ID: 6da3afafd647
Revises: 
Create Date: 2025-02-13 12:24:48.136654

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '6da3afafd647'
down_revision = None
branch_labels = None
depends_on = None
now = datetime.utcnow()


def upgrade():
    # Adiciona a nova coluna com um valor padrão
    op.add_column('equipamentos', sa.Column('data_cadastro', sa.DateTime(), nullable=False, server_default=str(now)))

def downgrade():
    op.drop_column('equipamentos', 'data_cadastro')
