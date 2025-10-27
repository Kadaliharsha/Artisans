# routers/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import your models and schemas
from models.product import Product as ProductModel
from schemas.product import ProductCreate, Product
from database.database import get_db

router = APIRouter(prefix="/api/v1")

@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product
    """
    try:
        db_product = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            category=product.category,
            image_url=product.image_url,
            artisan_id=product.artisan_id,
            is_active=product.is_active
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        return db_product
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )

@router.get("/products", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of products with pagination
    """
    try:
        products = db.query(Product).offset(skip).limit(limit).all()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving products: {str(e)}"
        )