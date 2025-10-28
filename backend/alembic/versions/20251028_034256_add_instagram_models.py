"""Add Instagram models: Post, Hashtag, Influencer

Revision ID: 20251028_034256
Revises: initial
Create Date: 2025-10-28 03:42:56.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251028_034256'
down_revision = None  # Will be updated when we have initial migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create instagram_posts table
    op.create_table(
        'instagram_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('media_type', sa.String(), nullable=False),
        sa.Column('media_url', sa.String(), nullable=True),
        sa.Column('thumbnail_url', sa.String(), nullable=True),
        sa.Column('permalink', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('location_id', sa.String(), nullable=True),
        sa.Column('like_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('comment_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('save_count', sa.Integer(), nullable=True),
        sa.Column('share_count', sa.Integer(), nullable=True),
        sa.Column('reach', sa.Integer(), nullable=True),
        sa.Column('impressions', sa.Integer(), nullable=True),
        sa.Column('engagement_rate', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('hashtags', sa.JSON(), nullable=True),
        sa.Column('mentions', sa.JSON(), nullable=True),
        sa.Column('market', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('sentiment_label', sa.String(), nullable=True),
        sa.Column('detected_products', sa.JSON(), nullable=True),
        sa.Column('detected_brands', sa.JSON(), nullable=True),
        sa.Column('is_sponsored', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('is_verified_account', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('analysis_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_instagram_posts_external_id', 'instagram_posts', ['external_id'], unique=True)
    op.create_index('ix_instagram_posts_id', 'instagram_posts', ['id'], unique=False)
    op.create_index('ix_instagram_posts_market', 'instagram_posts', ['market'], unique=False)
    op.create_index('ix_instagram_posts_category', 'instagram_posts', ['category'], unique=False)
    op.create_index('ix_instagram_posts_timestamp', 'instagram_posts', ['timestamp'], unique=False)
    op.create_index('ix_instagram_posts_username', 'instagram_posts', ['username'], unique=False)

    # Create instagram_hashtags table
    op.create_table(
        'instagram_hashtags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=True),
        sa.Column('market', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('post_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('avg_likes', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('avg_comments', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('avg_engagement', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('growth_rate', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('velocity', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('is_trending', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('trend_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('peak_trend_date', sa.DateTime(), nullable=True),
        sa.Column('competition_level', sa.String(), nullable=True),
        sa.Column('difficulty_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('tracked_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.Column('data_source', sa.String(), nullable=True, server_default='mock'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_instagram_hashtags_external_id', 'instagram_hashtags', ['external_id'], unique=True)
    op.create_index('ix_instagram_hashtags_id', 'instagram_hashtags', ['id'], unique=False)
    op.create_index('ix_instagram_hashtags_name', 'instagram_hashtags', ['name'], unique=False)
    op.create_index('ix_instagram_hashtags_market', 'instagram_hashtags', ['market'], unique=False)
    op.create_index('ix_instagram_hashtags_category', 'instagram_hashtags', ['category'], unique=False)
    op.create_index('ix_instagram_hashtags_tracked_at', 'instagram_hashtags', ['tracked_at'], unique=False)
    op.create_index('idx_hashtag_market_trending', 'instagram_hashtags', ['market', 'is_trending'], unique=False)
    op.create_index('idx_hashtag_market_score', 'instagram_hashtags', ['market', 'trend_score'], unique=False)

    # Create instagram_influencers table
    op.create_table(
        'instagram_influencers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('biography', sa.Text(), nullable=True),
        sa.Column('profile_picture_url', sa.String(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('is_business_account', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('is_private', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('followers_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('following_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('media_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('avg_likes', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('avg_comments', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('avg_views', sa.Float(), nullable=True),
        sa.Column('engagement_rate', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('posts_per_week', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('best_posting_times', sa.JSON(), nullable=True),
        sa.Column('content_types', sa.JSON(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('sub_categories', sa.JSON(), nullable=True),
        sa.Column('market', sa.String(), nullable=False),
        sa.Column('languages', sa.JSON(), nullable=True),
        sa.Column('audience_country_top', sa.String(), nullable=True),
        sa.Column('audience_gender_split', sa.JSON(), nullable=True),
        sa.Column('audience_age_range', sa.String(), nullable=True),
        sa.Column('authenticity_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('brand_affinity_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('content_quality_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('collaboration_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('estimated_post_cost', sa.Float(), nullable=True),
        sa.Column('estimated_story_cost', sa.Float(), nullable=True),
        sa.Column('partnership_tier', sa.String(), nullable=True),
        sa.Column('has_branded_content', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('contact_notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='discovered'),
        sa.Column('last_scraped_at', sa.DateTime(), nullable=True),
        sa.Column('data_source', sa.String(), nullable=True, server_default='mock'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_instagram_influencers_external_id', 'instagram_influencers', ['external_id'], unique=True)
    op.create_index('ix_instagram_influencers_id', 'instagram_influencers', ['id'], unique=False)
    op.create_index('ix_instagram_influencers_username', 'instagram_influencers', ['username'], unique=True)
    op.create_index('ix_instagram_influencers_followers_count', 'instagram_influencers', ['followers_count'], unique=False)
    op.create_index('ix_instagram_influencers_engagement_rate', 'instagram_influencers', ['engagement_rate'], unique=False)
    op.create_index('ix_instagram_influencers_authenticity_score', 'instagram_influencers', ['authenticity_score'], unique=False)
    op.create_index('ix_instagram_influencers_category', 'instagram_influencers', ['category'], unique=False)
    op.create_index('ix_instagram_influencers_market', 'instagram_influencers', ['market'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_instagram_influencers_market', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_category', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_authenticity_score', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_engagement_rate', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_followers_count', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_username', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_id', table_name='instagram_influencers')
    op.drop_index('ix_instagram_influencers_external_id', table_name='instagram_influencers')
    op.drop_table('instagram_influencers')
    
    op.drop_index('idx_hashtag_market_score', table_name='instagram_hashtags')
    op.drop_index('idx_hashtag_market_trending', table_name='instagram_hashtags')
    op.drop_index('ix_instagram_hashtags_tracked_at', table_name='instagram_hashtags')
    op.drop_index('ix_instagram_hashtags_category', table_name='instagram_hashtags')
    op.drop_index('ix_instagram_hashtags_market', table_name='instagram_hashtags')
    op.drop_index('ix_instagram_hashtags_name', table_name='instagram_hashtags')
    op.drop_index('ix_instagram_hashtags_id', table_name='instagram_hashtags')
    op.drop_index('ix_instagram_hashtags_external_id', table_name='instagram_hashtags')
    op.drop_table('instagram_hashtags')
    
    op.drop_index('ix_instagram_posts_username', table_name='instagram_posts')
    op.drop_index('ix_instagram_posts_timestamp', table_name='instagram_posts')
    op.drop_index('ix_instagram_posts_category', table_name='instagram_posts')
    op.drop_index('ix_instagram_posts_market', table_name='instagram_posts')
    op.drop_index('ix_instagram_posts_id', table_name='instagram_posts')
    op.drop_index('ix_instagram_posts_external_id', table_name='instagram_posts')
    op.drop_table('instagram_posts')
