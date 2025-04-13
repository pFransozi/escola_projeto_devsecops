"""Migração inicial automática

Revision ID: ec7195b08e61
Revises: 
Create Date: 2025-04-13 20:46:37.722513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec7195b08e61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('ultimo_nome', sa.String(length=50), nullable=False),
    sa.Column('usuario', sa.String(length=255), nullable=False),
    sa.Column('senha', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('data_nascimento', sa.Date(), nullable=False),
    sa.Column('sexo', sa.String(length=1), nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('endereco', sa.String(length=255), nullable=False),
    sa.Column('tipo', sa.Enum('Admin', 'Secretario', 'Professor', name='user_tipo_enum', native_enum=False), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('usuario')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    # ### end Alembic commands ###
