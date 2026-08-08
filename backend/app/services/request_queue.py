import logging
import queue
import threading
from concurrent.futures import Future

from app.services.execution_service import execute_code


logger = logging.getLogger(__name__)

MAX_QUEUE_SIZE = 10

_execution_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def _worker():
    """Process execution requests from the queue."""

    while True:
        code, future = _execution_queue.get()

        try:
            logger.info("Processing queued execution request")
            result = execute_code(code)
            future.set_result(result)

        except Exception as exc:
            logger.exception("Unexpected error in execution queue worker")
            future.set_exception(exc)

        finally:
            _execution_queue.task_done()


_worker_thread = threading.Thread(
    target=_worker,
    name="execution-worker",
    daemon=True
)

_worker_thread.start()


def submit_execution(code: str) -> Future:
    """
    Add a code execution request to the queue.

    Raises queue.Full when the queue has reached its maximum size.
    """

    future = Future()

    _execution_queue.put_nowait((code, future))

    logger.info(
        "Execution request added to queue. Queue size: %d",
        _execution_queue.qsize()
    )

    return future