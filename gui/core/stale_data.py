"""
Generic stale-data watcher.

Widgets compose one of these per data stream they care about (one per
GNSS fix, one per battery reading, etc.) so "no update recently" logic
lives in exactly one place instead of being reimplemented per widget.
Every widget showing live data should use this — nothing should just
freeze on a last-known value with no visible indication it's stale.
"""

from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class StaleDataWatcher(QObject):
    """Watches a single data stream for staleness.

    Connect `.notify` directly to the signal you want to watch — it
    accepts and ignores any signal arguments. If `.notify()` isn't
    called again within `timeout_ms`, `became_stale` fires. The next
    `.notify()` call after that fires `became_fresh`.
    """

    became_stale = pyqtSignal()
    became_fresh = pyqtSignal()

    def __init__(self, timeout_ms: int, parent=None):
        super().__init__(parent)
        self._is_stale = False

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(timeout_ms)
        self._timer.timeout.connect(self._on_timeout)

    def notify(self, *_args):
        """Call on every fresh update; restarts the staleness countdown."""
        if self._is_stale:
            self._is_stale = False
            self.became_fresh.emit()
        self._timer.start()

    def is_stale(self) -> bool:
        return self._is_stale

    def stop(self):
        """Stop watching (widget teardown, or a stream intentionally
        paused). Does not emit became_stale/became_fresh."""
        self._timer.stop()

    def _on_timeout(self):
        self._is_stale = True
        self.became_stale.emit()


if __name__ == '__main__':
    import sys
    from PyQt6.QtCore import QCoreApplication

    app = QCoreApplication(sys.argv)

    watcher = StaleDataWatcher(timeout_ms=300)
    watcher.became_stale.connect(lambda: print('became_stale'))
    watcher.became_fresh.connect(lambda: print('became_fresh'))

    print('notify() at t=0')
    watcher.notify()

    QTimer.singleShot(500, lambda: (
        print(f'is_stale at t=500ms: {watcher.is_stale()}'),
    ))
    QTimer.singleShot(600, watcher.notify)
    QTimer.singleShot(700, lambda: (
        print(f'is_stale at t=700ms: {watcher.is_stale()}'),
        app.quit(),
    ))

    app.exec()
