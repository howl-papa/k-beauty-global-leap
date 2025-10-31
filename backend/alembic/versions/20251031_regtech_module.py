"""Add RegTech module tables

Revision ID: 20251031_regtech_module
Revises: 20251028_080000_add_instagram_auth_fields
Create Date: 2025-10-31 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251031_regtech_module'
down_revision = '20251028_080000_add_instagram_auth_fields'
branch_labels = None
depends_on = None


def upgrade():
    # Create regulation_documents table
    op.create_table(
        'regulation_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('regulation_type', sa.Enum('FDA_MOCRA', 'EU_CPNP', 'ASEAN', 'OTHER', name='regulationtype'), nullable=False),
        sa.Column('country_code', sa.String(length=10), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(length=1000), nullable=True),
        sa.Column('document_content', sa.Text(), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('version', sa.String(length=50), nullable=True),
        sa.Column('effective_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_regulation_documents_id'), 'regulation_documents', ['id'], unique=False)
    op.create_index(op.f('ix_regulation_documents_regulation_type'), 'regulation_documents', ['regulation_type'], unique=False)
    op.create_index(op.f('ix_regulation_documents_country_code'), 'regulation_documents', ['country_code'], unique=False)

    # Create prohibited_ingredients table
    op.create_table(
        'prohibited_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ingredient_name', sa.String(length=500), nullable=False),
        sa.Column('cas_number', sa.String(length=50), nullable=True),
        sa.Column('inci_name', sa.String(length=500), nullable=True),
        sa.Column('regulation_type', sa.Enum('FDA_MOCRA', 'EU_CPNP', 'ASEAN', 'OTHER', name='regulationtype'), nullable=False),
        sa.Column('country_code', sa.String(length=10), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('max_concentration', sa.String(length=100), nullable=True),
        sa.Column('restriction_notes', sa.Text(), nullable=True),
        sa.Column('prohibited_use_cases', sa.JSON(), nullable=True),
        sa.Column('hazard_category', sa.String(length=200), nullable=True),
        sa.Column('alternative_ingredients', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prohibited_ingredients_id'), 'prohibited_ingredients', ['id'], unique=False)
    op.create_index(op.f('ix_prohibited_ingredients_ingredient_name'), 'prohibited_ingredients', ['ingredient_name'], unique=False)
    op.create_index(op.f('ix_prohibited_ingredients_cas_number'), 'prohibited_ingredients', ['cas_number'], unique=False)
    op.create_index(op.f('ix_prohibited_ingredients_inci_name'), 'prohibited_ingredients', ['inci_name'], unique=False)
    op.create_index(op.f('ix_prohibited_ingredients_regulation_type'), 'prohibited_ingredients', ['regulation_type'], unique=False)
    op.create_index(op.f('ix_prohibited_ingredients_country_code'), 'prohibited_ingredients', ['country_code'], unique=False)

    # Create product_analyses table
    op.create_table(
        'product_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(length=500), nullable=False),
        sa.Column('product_category', sa.String(length=200), nullable=True),
        sa.Column('brand_name', sa.String(length=200), nullable=True),
        sa.Column('target_country', sa.String(length=10), nullable=False),
        sa.Column('regulation_type', sa.String(length=50), nullable=False),
        sa.Column('ingredients_list', sa.JSON(), nullable=False),
        sa.Column('full_ingredient_text', sa.Text(), nullable=True),
        sa.Column('compliance_status', sa.Enum('COMPLIANT', 'WARNING', 'NON_COMPLIANT', 'PENDING', name='compliancestatus'), nullable=False),
        sa.Column('compliance_score', sa.Float(), nullable=False),
        sa.Column('risk_level', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='risklevel'), nullable=False),
        sa.Column('prohibited_ingredients_found', sa.JSON(), nullable=True),
        sa.Column('restricted_ingredients_found', sa.JSON(), nullable=True),
        sa.Column('warnings', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('ai_analysis_summary', sa.Text(), nullable=True),
        sa.Column('ai_model_used', sa.String(length=100), nullable=True),
        sa.Column('report_pdf_url', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_analyses_id'), 'product_analyses', ['id'], unique=False)
    op.create_index(op.f('ix_product_analyses_user_id'), 'product_analyses', ['user_id'], unique=False)
    op.create_index(op.f('ix_product_analyses_target_country'), 'product_analyses', ['target_country'], unique=False)
    op.create_index(op.f('ix_product_analyses_compliance_status'), 'product_analyses', ['compliance_status'], unique=False)
    op.create_index(op.f('ix_product_analyses_created_at'), 'product_analyses', ['created_at'], unique=False)

    # Create compliance_alerts table
    op.create_table(
        'compliance_alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('regulation_type', sa.String(length=50), nullable=False),
        sa.Column('country_code', sa.String(length=10), nullable=False),
        sa.Column('severity', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='risklevel'), nullable=False),
        sa.Column('affected_ingredients', sa.JSON(), nullable=True),
        sa.Column('affected_categories', sa.JSON(), nullable=True),
        sa.Column('effective_date', sa.DateTime(), nullable=True),
        sa.Column('published_date', sa.DateTime(), nullable=True),
        sa.Column('source_url', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_compliance_alerts_id'), 'compliance_alerts', ['id'], unique=False)
    op.create_index(op.f('ix_compliance_alerts_regulation_type'), 'compliance_alerts', ['regulation_type'], unique=False)
    op.create_index(op.f('ix_compliance_alerts_country_code'), 'compliance_alerts', ['country_code'], unique=False)
    op.create_index(op.f('ix_compliance_alerts_created_at'), 'compliance_alerts', ['created_at'], unique=False)


def downgrade():
    # Drop tables in reverse order
    op.drop_index(op.f('ix_compliance_alerts_created_at'), table_name='compliance_alerts')
    op.drop_index(op.f('ix_compliance_alerts_country_code'), table_name='compliance_alerts')
    op.drop_index(op.f('ix_compliance_alerts_regulation_type'), table_name='compliance_alerts')
    op.drop_index(op.f('ix_compliance_alerts_id'), table_name='compliance_alerts')
    op.drop_table('compliance_alerts')
    
    op.drop_index(op.f('ix_product_analyses_created_at'), table_name='product_analyses')
    op.drop_index(op.f('ix_product_analyses_compliance_status'), table_name='product_analyses')
    op.drop_index(op.f('ix_product_analyses_target_country'), table_name='product_analyses')
    op.drop_index(op.f('ix_product_analyses_user_id'), table_name='product_analyses')
    op.drop_index(op.f('ix_product_analyses_id'), table_name='product_analyses')
    op.drop_table('product_analyses')
    
    op.drop_index(op.f('ix_prohibited_ingredients_country_code'), table_name='prohibited_ingredients')
    op.drop_index(op.f('ix_prohibited_ingredients_regulation_type'), table_name='prohibited_ingredients')
    op.drop_index(op.f('ix_prohibited_ingredients_inci_name'), table_name='prohibited_ingredients')
    op.drop_index(op.f('ix_prohibited_ingredients_cas_number'), table_name='prohibited_ingredients')
    op.drop_index(op.f('ix_prohibited_ingredients_ingredient_name'), table_name='prohibited_ingredients')
    op.drop_index(op.f('ix_prohibited_ingredients_id'), table_name='prohibited_ingredients')
    op.drop_table('prohibited_ingredients')
    
    op.drop_index(op.f('ix_regulation_documents_country_code'), table_name='regulation_documents')
    op.drop_index(op.f('ix_regulation_documents_regulation_type'), table_name='regulation_documents')
    op.drop_index(op.f('ix_regulation_documents_id'), table_name='regulation_documents')
    op.drop_table('regulation_documents')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS risklevel')
    op.execute('DROP TYPE IF EXISTS compliancestatus')
    op.execute('DROP TYPE IF EXISTS regulationtype')
