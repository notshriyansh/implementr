
from threading import RLock

from app.architecture.repository_graph import RepositoryGraph


class RepositoryGraphRegistry:

    def __init__(self) -> None:
        self._graphs: dict[str, RepositoryGraph] = {}
        self._lock = RLock()

    def get(
        self,
        repository_id: str,
    ) -> RepositoryGraph | None:
        with self._lock:
            return self._graphs.get(repository_id)

    def replace(
        self,
        repository_id: str,
        graph: RepositoryGraph,
    ) -> None:
        """Atomically publish a completely built repository graph."""
        with self._lock:
            self._graphs[repository_id] = graph

    def remove(
        self,
        repository_id: str,
    ) -> bool:
        with self._lock:
            return self._graphs.pop(repository_id, None) is not None

    def repository_ids(self) -> list[str]:
        with self._lock:
            return list(self._graphs.keys())
