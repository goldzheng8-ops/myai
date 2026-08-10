更好的架构是未来增加一个：

EventFailurePolicy

例如：

IGNORE
LOG
RAISE

但现在我们已经明确 Event 是 Notification Infrastructure，我建议第一版直接固定为 best-effort + logging，不要再引入复杂策略。