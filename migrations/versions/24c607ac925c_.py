"""empty message

Revision ID: 24c607ac925c
Revises: e4e8ae5c36d5
Create Date: 2021-12-11 13:13:04.806256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24c607ac925c"
down_revision = "e4e8ae5c36d5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quote_id", sa.String(length=100), nullable=False),
        sa.Column("transfer_id", sa.String(length=100), nullable=False),
        sa.Column("target_account_id", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column(
            "create_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("complaint_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    # ### end Alembic commands ###
