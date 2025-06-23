from alembic import op
import sqlalchemy as sa


revision = '621b4946cb41'
down_revision = 'f4646731bfce'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('users_pkey', 'users', type_='primary')
    op.add_column('users', sa.Column('user_id', sa.BigInteger(), primary_key=True, autoincrement=True))
    op.create_primary_key('users_pkey', 'users', ['user_id'])
    op.drop_column('users', 'users_id')


def downgrade():
    op.drop_constraint('users_pkey', 'users', type_='primary')
    op.add_column('users', sa.Column('users_id', sa.BigInteger(), primary_key=True, autoincrement=True))
    op.create_primary_key('users_pkey', 'users', ['users_id'])
    op.drop_column('users', 'user_id')
