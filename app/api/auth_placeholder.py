# /app/api/auth_placeholder.py
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.organization import Organization, User

async def get_current_organization(db: AsyncSession = Depends(get_db)) -> Organization:
    """
    Placeholder Auth. In a real app, this would come from a JWT token.
    For now, just grab the first Organization.
    """
    org = await db.get(Organization, 1) # Get Org with ID 1
    if not org:
        # If no org 1, create one for testing
        org = Organization(name="Test Forwarder")
        db.add(org)
        await db.commit()
        await db.refresh(org)
    return org
