package com.andforce.andclaw.blindpilot.core

/**
 * Local emergency stop that does not depend on VPS or Agent.
 * M1: gate mutating actions. M3 will bind spoken stop phrases.
 */
class LocalActionGate {
    @Volatile
    var generation: Long = 0
        private set

    @Volatile
    var stopped: Boolean = false
        private set

    fun stop(reason: String = "local_emergency_stop") {
        stopped = true
        generation += 1
        lastReason = reason
    }

    fun resume() {
        stopped = false
        generation += 1
        lastReason = null
    }

    @Volatile
    var lastReason: String? = null
        private set

    fun accept(expectedGeneration: Long? = null): ErrorCode? {
        if (stopped) return ErrorCode.TASK_CANCELLED
        if (expectedGeneration != null && expectedGeneration != generation) {
            return ErrorCode.STALE_COMMAND
        }
        return null
    }
}
