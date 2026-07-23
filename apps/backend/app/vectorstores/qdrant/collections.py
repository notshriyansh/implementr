from qdrant_client.http.models import Distance, VectorParams

from app.core.config import get_settings
from app.vectorstores.qdrant.client import get_qdrant_client

import logging

logger = logging.getLogger(__name__)


async def ensure_collections() -> None:
    client = get_qdrant_client()
    settings = get_settings()

    collections = [
        settings.qdrant_documents_collection,
        settings.qdrant_code_collection,
        settings.qdrant_symbols_collection,
    ]

    response = await client.get_collections()

    existing = {
        c.name
        for c in response.collections
    }

    for collection in collections:
        if collection in existing:
            continue

        if collection in existing:
            logger.info(
                "Collection '%s' already exists.",
                collection,
            )
            continue

        logger.info(
            "Creating collection '%s'...",
            collection,
        )


        await client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )