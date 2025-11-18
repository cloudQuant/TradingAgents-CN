"""Utilities for persisting APScheduler job pause states across restarts."""
from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tradingagents.utils.logging_manager import get_logger

logger = get_logger(__name__)
_lock = Lock()
_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "scheduler_jobs_state.json"


def _ensure_config_dir() -> None:
    """Make sure the config directory exists."""
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _read_states() -> Dict[str, bool]:
    """Read persisted job states from the config file."""
    if not _CONFIG_PATH.exists():
        return {}

    try:
        with _CONFIG_PATH.open("r", encoding="utf-8") as fp:
            data = json.load(fp) or {}
            return {str(k): bool(v) for k, v in data.items()}
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read scheduler job states, ignoring persisted data: %s", exc)
        return {}


def _write_states(states: Dict[str, bool]) -> None:
    """Persist job states to disk atomically."""
    _ensure_config_dir()
    tmp_path = _CONFIG_PATH.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as fp:
        json.dump(states, fp, ensure_ascii=False, indent=2)
    tmp_path.replace(_CONFIG_PATH)


def record_job_state(job_id: str, paused: bool) -> None:
    """Persist the desired pause state for a job."""
    job_id = str(job_id)
    with _lock:
        states = _read_states()
        states[job_id] = bool(paused)
        _write_states(states)
        logger.debug("Persisted scheduler job state: %s paused=%s", job_id, paused)


def get_persisted_states() -> Dict[str, bool]:
    """Return a copy of the persisted job states."""
    with _lock:
        return dict(_read_states())


def apply_persisted_states(scheduler: AsyncIOScheduler) -> None:
    """Ensure the scheduler matches the persisted pause states."""
    states = get_persisted_states()
    if not states:
        return

    for job_id, paused in states.items():
        job = scheduler.get_job(job_id)
        if not job:
            logger.warning("Persisted scheduler job state references missing job: %s", job_id)
            continue

        try:
            if paused:
                scheduler.pause_job(job_id)
                logger.info("Applied persisted pause state to job %s", job_id)
            else:
                scheduler.resume_job(job_id)
                logger.info("Applied persisted running state to job %s", job_id)
        except Exception as exc:
            logger.error("Failed to apply persisted state for job %s: %s", job_id, exc)
