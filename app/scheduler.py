"""Very small in-memory scheduler.

A production-ready system would use a real job queue and persistent
storage. This module provides a minimal abstraction so that the rest
of the application can enqueue publishing jobs.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class Job:
    run_at: float
    func: Callable[[], None]
    id: int = field(default_factory=int)


class Scheduler:
    def __init__(self) -> None:
        self.jobs: List[Job] = []
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._running = False

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._thread.start()

    def shutdown(self) -> None:
        self._running = False
        self._thread.join(timeout=1)

    def enqueue(self, delay_seconds: float, func: Callable[[], None]) -> int:
        job = Job(run_at=time.time() + delay_seconds, func=func, id=len(self.jobs) + 1)
        with self._lock:
            self.jobs.append(job)
        return job.id

    def _run(self) -> None:
        while self._running:
            now = time.time()
            to_run: List[Job] = []
            with self._lock:
                remaining: List[Job] = []
                for job in self.jobs:
                    if job.run_at <= now:
                        to_run.append(job)
                    else:
                        remaining.append(job)
                self.jobs = remaining
            for job in to_run:
                try:
                    job.func()
                except Exception:
                    pass
            time.sleep(0.5)


scheduler = Scheduler()
