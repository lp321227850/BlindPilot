package com.andforce.andclaw.blindpilot.core

/**
 * Package identity only. Rejects arbitrary Intent URIs (VIEW/DIAL/SEND/HTTP).
 */
object PackageNames {
    private val PACKAGE = Regex("^[A-Za-z][A-Za-z0-9_]*(\\.[A-Za-z][A-Za-z0-9_]*)+$")

    private val ALIASES: Map<String, List<String>> = mapOf(
        "设置" to listOf("com.android.settings"),
        "settings" to listOf("com.android.settings"),
        "时钟" to listOf(
            "com.android.deskclock",
            "com.google.android.deskclock",
            "com.sec.android.app.clockpackage",
        ),
        "clock" to listOf(
            "com.android.deskclock",
            "com.google.android.deskclock",
            "com.sec.android.app.clockpackage",
        ),
        "电话" to listOf(
            "com.android.dialer",
            "com.google.android.dialer",
            "com.samsung.android.dialer",
            "com.android.phone",
        ),
        "phone" to listOf(
            "com.android.dialer",
            "com.google.android.dialer",
            "com.samsung.android.dialer",
        ),
        "联系人" to listOf(
            "com.android.contacts",
            "com.google.android.contacts",
            "com.samsung.android.app.contacts",
        ),
        "短信" to listOf(
            "com.android.mms",
            "com.google.android.apps.messaging",
            "com.samsung.android.messaging",
        ),
        "微信" to listOf("com.tencent.mm"),
        "wechat" to listOf("com.tencent.mm"),
    )

    fun isValid(packageName: String): Boolean {
        val pkg = packageName.trim()
        if (pkg.isEmpty() || pkg.length > 255) return false
        if (pkg.contains(':') || pkg.contains('/') || pkg.contains(' ') || pkg.contains('\\')) {
            return false
        }
        return PACKAGE.matches(pkg)
    }

    fun normalizeAppName(name: String): String = name.trim().lowercase()

    fun candidatesFor(appName: String): List<String> {
        val key = appName.trim()
        if (key.isEmpty()) return emptyList()
        ALIASES[key]?.let { return it }
        ALIASES[normalizeAppName(key)]?.let { return it }
        if (isValid(key)) return listOf(key)
        return emptyList()
    }
}
