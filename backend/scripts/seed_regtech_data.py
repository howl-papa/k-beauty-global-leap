"""
Seed RegTech Database with Sample Data

This script populates the database with sample prohibited/restricted ingredients
for testing the RegTech compliance analysis functionality.
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal
from app.models.regulation import ProhibitedIngredient, RegulationType


def seed_prohibited_ingredients(db: SessionLocal):
    """Seed database with sample prohibited and restricted ingredients"""
    
    # Sample prohibited/restricted ingredients based on actual regulations
    sample_ingredients = [
        # US FDA MoCRA - Prohibited
        {
            "ingredient_name": "Mercury compounds",
            "cas_number": "7439-97-6",
            "inci_name": "Mercury",
            "regulation_type": RegulationType.FDA_MOCRA,
            "country_code": "US",
            "status": "PROHIBITED",
            "restriction_notes": "Banned in all cosmetic products except as preservative in eye area cosmetics at trace amounts",
            "hazard_category": "Heavy metal toxicity",
            "alternative_ingredients": ["Zinc oxide", "Titanium dioxide"]
        },
        {
            "ingredient_name": "Chloroform",
            "cas_number": "67-66-3",
            "inci_name": "Chloroform",
            "regulation_type": RegulationType.FDA_MOCRA,
            "country_code": "US",
            "status": "PROHIBITED",
            "restriction_notes": "Prohibited in cosmetic products",
            "hazard_category": "Carcinogen",
            "alternative_ingredients": ["Ethanol", "Isopropyl alcohol"]
        },
        {
            "ingredient_name": "Methylene chloride",
            "cas_number": "75-09-2",
            "inci_name": "Methylene chloride",
            "regulation_type": RegulationType.FDA_MOCRA,
            "country_code": "US",
            "status": "PROHIBITED",
            "restriction_notes": "Banned in cosmetics due to carcinogenic properties",
            "hazard_category": "Carcinogen",
            "alternative_ingredients": ["Ethyl acetate"]
        },
        
        # US FDA MoCRA - Restricted
        {
            "ingredient_name": "Hydroquinone",
            "cas_number": "123-31-9",
            "inci_name": "Hydroquinone",
            "regulation_type": RegulationType.FDA_MOCRA,
            "country_code": "US",
            "status": "RESTRICTED",
            "max_concentration": "2%",
            "restriction_notes": "Allowed only in OTC skin lightening products at 2% concentration",
            "hazard_category": "Skin irritant, potential carcinogen",
            "alternative_ingredients": ["Niacinamide", "Vitamin C", "Alpha arbutin"]
        },
        {
            "ingredient_name": "Formaldehyde",
            "cas_number": "50-00-0",
            "inci_name": "Formaldehyde",
            "regulation_type": RegulationType.FDA_MOCRA,
            "country_code": "US",
            "status": "RESTRICTED",
            "max_concentration": "0.2%",
            "restriction_notes": "Allowed as preservative up to 0.2%, must be labeled",
            "hazard_category": "Carcinogen, allergen",
            "alternative_ingredients": ["Phenoxyethanol", "Benzyl alcohol"]
        },
        
        # EU CPNP - Prohibited
        {
            "ingredient_name": "Parabens (certain types)",
            "cas_number": "94-26-8",
            "inci_name": "Butylparaben",
            "regulation_type": RegulationType.EU_CPNP,
            "country_code": "EU",
            "status": "PROHIBITED",
            "restriction_notes": "Isopropylparaben, isobutylparaben, phenylparaben, benzylparaben, and pentylparaben are prohibited",
            "hazard_category": "Endocrine disruptor",
            "alternative_ingredients": ["Ethylhexylglycerin", "Sodium benzoate"]
        },
        {
            "ingredient_name": "Triclosan",
            "cas_number": "3380-34-5",
            "inci_name": "Triclosan",
            "regulation_type": RegulationType.EU_CPNP,
            "country_code": "EU",
            "status": "PROHIBITED",
            "restriction_notes": "Banned in all cosmetic products in EU since 2018",
            "hazard_category": "Endocrine disruptor, antibiotic resistance",
            "alternative_ingredients": ["Tea tree oil", "Salicylic acid"]
        },
        {
            "ingredient_name": "Lead acetate",
            "cas_number": "301-04-2",
            "inci_name": "Lead acetate",
            "regulation_type": RegulationType.EU_CPNP,
            "country_code": "EU",
            "status": "PROHIBITED",
            "restriction_notes": "Prohibited in all cosmetic products",
            "hazard_category": "Heavy metal toxicity, neurotoxin",
            "alternative_ingredients": ["Natural hair dyes", "Henna"]
        },
        
        # EU CPNP - Restricted
        {
            "ingredient_name": "Resorcinol",
            "cas_number": "108-46-3",
            "inci_name": "Resorcinol",
            "regulation_type": RegulationType.EU_CPNP,
            "country_code": "EU",
            "status": "RESTRICTED",
            "max_concentration": "0.5%",
            "restriction_notes": "Max 0.5% in hair products, prohibited in other cosmetics",
            "hazard_category": "Thyroid disruptor",
            "alternative_ingredients": ["Kojic acid", "Licorice extract"]
        },
        {
            "ingredient_name": "Salicylic acid",
            "cas_number": "69-72-7",
            "inci_name": "Salicylic acid",
            "regulation_type": RegulationType.EU_CPNP,
            "country_code": "EU",
            "status": "RESTRICTED",
            "max_concentration": "2%",
            "restriction_notes": "Max 2% in leave-on products, 3% in rinse-off products",
            "hazard_category": "Skin irritant at high concentrations",
            "alternative_ingredients": ["Lactic acid", "Glycolic acid"]
        },
        
        # ASEAN - Prohibited
        {
            "ingredient_name": "Hydroquinone",
            "cas_number": "123-31-9",
            "inci_name": "Hydroquinone",
            "regulation_type": RegulationType.ASEAN,
            "country_code": "TH",
            "status": "PROHIBITED",
            "restriction_notes": "Completely banned in Thailand and most ASEAN countries",
            "hazard_category": "Skin irritant, potential carcinogen",
            "alternative_ingredients": ["Niacinamide", "Tranexamic acid"]
        },
        {
            "ingredient_name": "Mercury compounds",
            "cas_number": "7439-97-6",
            "inci_name": "Mercury",
            "regulation_type": RegulationType.ASEAN,
            "country_code": "TH",
            "status": "PROHIBITED",
            "restriction_notes": "Banned in all ASEAN member states",
            "hazard_category": "Heavy metal toxicity",
            "alternative_ingredients": ["Zinc oxide", "Titanium dioxide"]
        },
        
        # ASEAN - Restricted
        {
            "ingredient_name": "Kojic acid",
            "cas_number": "501-30-4",
            "inci_name": "Kojic acid",
            "regulation_type": RegulationType.ASEAN,
            "country_code": "TH",
            "status": "RESTRICTED",
            "max_concentration": "1%",
            "restriction_notes": "Maximum 1% in skin lightening products",
            "hazard_category": "Skin irritant at high concentrations",
            "alternative_ingredients": ["Alpha arbutin", "Vitamin C"]
        },
    ]
    
    # Check if data already exists
    existing_count = db.query(ProhibitedIngredient).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} ingredients. Skipping seed.")
        return
    
    # Insert sample data
    for ingredient_data in sample_ingredients:
        ingredient = ProhibitedIngredient(**ingredient_data)
        db.add(ingredient)
    
    db.commit()
    print(f"✅ Successfully seeded {len(sample_ingredients)} prohibited/restricted ingredients")


def main():
    """Main function to seed RegTech data"""
    print("🌱 Seeding RegTech database with sample data...")
    
    db = SessionLocal()
    try:
        seed_prohibited_ingredients(db)
        print("✅ RegTech database seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
