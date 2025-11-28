"""In-memory job manager for background tasks."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class Job:
    job_type: str
    payload: dict
    status: str = "queued"
    progress: float = 0.0
    message: str | None = None


class JobManager:
    def __init__(self):
        self.jobs: List[Job] = []
        self.handlers: Dict[str, Callable[[dict], None]] = {}

    def register(self, job_type: str, handler: Callable[[dict], None]) -> None:
        self.handlers[job_type] = handler

    def enqueue(self, job_type: str, payload: dict) -> Job:
        job = Job(job_type=job_type, payload=payload)
        self.jobs.append(job)
        return job

    def run_all(self) -> None:
        for job in self.jobs:
            handler = self.handlers.get(job.job_type)
            if not handler:
                job.status = "error"
                job.message = "No handler registered"
                continue
            job.status = "running"
            handler(job.payload)
            job.status = "done"
            job.progress = 1.0
