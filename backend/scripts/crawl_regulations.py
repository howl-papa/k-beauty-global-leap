"""
Regulation Crawler

Automated crawler for monitoring cosmetic regulation updates
from FDA, EU Commission, and ASEAN regulatory websites.

This is a basic implementation that can be extended with real crawling logic.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import SessionLocal
from app.models.regulation import RegulationDocument, ProhibitedIngredient, RegulationType
from app.models.product_compliance import ComplianceAlert, RiskLevel


class RegulationCrawler:
    """Crawler for cosmetic regulations"""
    
    def __init__(self, db: SessionLocal):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'K-Beauty-RegTech-Crawler/1.0'
        })
    
    def crawl_fda_mocra(self) -> List[Dict[str, Any]]:
        """
        Crawl FDA MoCRA regulations
        
        In production, this would:
        1. Access FDA website APIs or pages
        2. Parse regulation documents
        3. Extract prohibited/restricted ingredients
        4. Detect changes from previous crawl
        """
        print("📡 Crawling FDA MoCRA regulations...")
        
        # Placeholder - would contain actual crawling logic
        # Example URLs:
        # - https://www.fda.gov/cosmetics/cosmetics-laws-regulations
        # - https://www.fda.gov/cosmetics/cosmetics-guidance-regulation/fda-authority-over-cosmetics
        
        documents = []
        
        # Example document structure
        documents.append({
            "regulation_type": RegulationType.FDA_MOCRA,
            "country_code": "US",
            "title": "Modernization of Cosmetics Regulation Act (MoCRA) - 2024 Update",
            "description": "Updated requirements for cosmetic facility registration and product listing",
            "source_url": "https://www.fda.gov/cosmetics/cosmetics-laws-regulations/modernization-cosmetics-regulation-act-2022",
            "version": "2024.1",
            "effective_date": datetime(2024, 1, 1)
        })
        
        print(f"✓ Found {len(documents)} FDA documents")
        return documents
    
    def crawl_eu_cpnp(self) -> List[Dict[str, Any]]:
        """
        Crawl EU CPNP regulations
        
        In production, this would access:
        - EU Commission cosmetics database
        - CosIng (Cosmetic Ingredients) database
        - European regulations portal
        """
        print("📡 Crawling EU CPNP regulations...")
        
        documents = []
        
        # Example URLs:
        # - https://ec.europa.eu/growth/sectors/cosmetics/legislation_en
        # - https://ec.europa.eu/growth/tools-databases/cosing/
        
        documents.append({
            "regulation_type": RegulationType.EU_CPNP,
            "country_code": "EU",
            "title": "EU Cosmetics Regulation (EC) No 1223/2009 - Latest Amendments",
            "description": "Updated list of prohibited and restricted substances",
            "source_url": "https://ec.europa.eu/growth/sectors/cosmetics/legislation_en",
            "version": "2024.Q4",
            "effective_date": datetime(2024, 10, 1)
        })
        
        print(f"✓ Found {len(documents)} EU documents")
        return documents
    
    def crawl_asean_regulations(self) -> List[Dict[str, Any]]:
        """
        Crawl ASEAN cosmetic regulations
        
        In production, this would access:
        - ASEAN Cosmetic Committee (ACC) documents
        - Individual country regulatory portals (Thailand FDA, HSA Singapore, etc.)
        """
        print("📡 Crawling ASEAN regulations...")
        
        documents = []
        
        # Example sources:
        # - ASEAN Cosmetic Directive
        # - Thailand FDA
        # - Singapore HSA
        
        documents.append({
            "regulation_type": RegulationType.ASEAN,
            "country_code": "TH",
            "title": "ASEAN Cosmetic Directive - 2024 Update",
            "description": "Harmonized requirements for cosmetic products in ASEAN member states",
            "source_url": "http://www.aseancosmetics.org/",
            "version": "2024.1",
            "effective_date": datetime(2024, 7, 1)
        })
        
        print(f"✓ Found {len(documents)} ASEAN documents")
        return documents
    
    def detect_changes(
        self,
        new_documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect changes by comparing with existing database
        
        Returns list of changes that require alerts
        """
        print("🔍 Detecting regulation changes...")
        
        changes = []
        
        for doc in new_documents:
            # Check if document exists
            existing = self.db.query(RegulationDocument).filter(
                RegulationDocument.regulation_type == doc["regulation_type"],
                RegulationDocument.country_code == doc["country_code"],
                RegulationDocument.title == doc["title"]
            ).first()
            
            if not existing:
                changes.append({
                    "type": "new_regulation",
                    "document": doc,
                    "severity": RiskLevel.MEDIUM
                })
                print(f"  ✨ New regulation: {doc['title']}")
            elif existing.version != doc.get("version"):
                changes.append({
                    "type": "regulation_updated",
                    "document": doc,
                    "old_version": existing.version,
                    "new_version": doc.get("version"),
                    "severity": RiskLevel.HIGH
                })
                print(f"  🔄 Updated regulation: {doc['title']}")
        
        return changes
    
    def save_documents(self, documents: List[Dict[str, Any]]):
        """Save or update regulation documents in database"""
        print("💾 Saving regulation documents...")
        
        for doc in documents:
            existing = self.db.query(RegulationDocument).filter(
                RegulationDocument.regulation_type == doc["regulation_type"],
                RegulationDocument.country_code == doc["country_code"],
                RegulationDocument.title == doc["title"]
            ).first()
            
            if existing:
                # Update existing document
                for key, value in doc.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.last_updated = datetime.utcnow()
            else:
                # Create new document
                new_doc = RegulationDocument(**doc)
                self.db.add(new_doc)
        
        self.db.commit()
        print(f"✓ Saved {len(documents)} documents")
    
    def create_alerts(self, changes: List[Dict[str, Any]]):
        """Create compliance alerts for significant changes"""
        print("📢 Creating compliance alerts...")
        
        for change in changes:
            doc = change["document"]
            
            if change["type"] == "new_regulation":
                alert = ComplianceAlert(
                    title=f"New Regulation: {doc['title']}",
                    description=f"A new cosmetic regulation has been published for {doc['country_code']}. Please review your products for compliance.",
                    regulation_type=doc["regulation_type"],
                    country_code=doc["country_code"],
                    severity=change["severity"],
                    effective_date=doc.get("effective_date"),
                    source_url=doc.get("source_url")
                )
            elif change["type"] == "regulation_updated":
                alert = ComplianceAlert(
                    title=f"Regulation Updated: {doc['title']}",
                    description=f"Regulation version updated from {change['old_version']} to {change['new_version']}. Review changes for impact on your products.",
                    regulation_type=doc["regulation_type"],
                    country_code=doc["country_code"],
                    severity=change["severity"],
                    effective_date=doc.get("effective_date"),
                    source_url=doc.get("source_url")
                )
            else:
                continue
            
            self.db.add(alert)
        
        self.db.commit()
        print(f"✓ Created {len(changes)} alerts")
    
    def run(self):
        """Run complete crawling process"""
        print("🚀 Starting regulation crawler...\n")
        
        all_documents = []
        
        # Crawl all sources
        all_documents.extend(self.crawl_fda_mocra())
        all_documents.extend(self.crawl_eu_cpnp())
        all_documents.extend(self.crawl_asean_regulations())
        
        # Detect changes
        changes = self.detect_changes(all_documents)
        
        # Save documents
        self.save_documents(all_documents)
        
        # Create alerts for changes
        if changes:
            self.create_alerts(changes)
        
        print(f"\n✅ Crawling complete!")
        print(f"   Total documents: {len(all_documents)}")
        print(f"   Changes detected: {len(changes)}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("RegTech Regulation Crawler")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    try:
        crawler = RegulationCrawler(db)
        crawler.run()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
