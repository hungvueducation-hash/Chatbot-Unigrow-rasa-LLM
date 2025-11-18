import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class MediaHandler:
    """Quản lý hình ảnh, PDF, video"""
    
    def __init__(self, media_dir: str = "data/knowledge_base"):
        self.media_dir = Path(media_dir)
        self.images_dir = self.media_dir / "images"
        self.documents_dir = self.media_dir / "documents"
        self.videos_dir = self.media_dir / "videos"
    
    def get_product_image(self, product_name: str = "unigrow") -> Optional[str]:
        """Lấy ảnh sản phẩm"""
        image_path = self.images_dir / f"{product_name}.png"
        if image_path.exists():
            logger.info(f"Found image: {image_path}")
            return str(image_path)
        logger.warning(f"Image not found: {image_path}")
        return None
    
    def get_document_path(self, doc_name: str) -> Optional[str]:
        """Lấy đường dẫn PDF/document"""
        doc_path = self.documents_dir / doc_name
        if doc_path.exists():
            logger.info(f"Found document: {doc_path}")
            return str(doc_path)
        logger.warning(f"Document not found: {doc_path}")
        return None
    
    def list_available_documents(self) -> List[str]:
        """Liệt kê các tài liệu có sẵn"""
        if self.documents_dir.exists():
            docs = [f.name for f in self.documents_dir.glob("*")]
            logger.info(f"Found {len(docs)} documents")
            return docs
        return []
    
    def list_available_images(self) -> List[str]:
        """Liệt kê các ảnh có sẵn"""
        if self.images_dir.exists():
            images = [f.name for f in self.images_dir.glob("*")]
            logger.info(f"Found {len(images)} images")
            return images
        return []
    
    def get_media_metadata(self) -> Dict[str, Any]:
        """Lấy metadata của tất cả media"""
        metadata = {
            "images": [],
            "documents": [],
            "videos": []
        }
        
        # Images
        for img in self.list_available_images():
            img_path = self.images_dir / img
            metadata["images"].append({
                "name": img,
                "size": img_path.stat().st_size,
                "modified": img_path.stat().st_mtime
            })
        
        # Documents
        for doc in self.list_available_documents():
            doc_path = self.documents_dir / doc
            metadata["documents"].append({
                "name": doc,
                "size": doc_path.stat().st_size,
                "modified": doc_path.stat().st_mtime
            })
        
        return metadata

# Global media handler instance
media_handler = MediaHandler()
