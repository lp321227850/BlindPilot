package com.andforce.andclaw.blindpilot.core

/**
 * SECRET values never leave the device in serialized ScreenState / observe dumps.
 */
object PrivacyRedactor {
    const val PROTECTED = "[PROTECTED]"

    fun isSecretNode(
        isPassword: Boolean,
        className: String?,
        resourceId: String?,
        inputTypeHint: String? = null,
    ): Boolean {
        if (isPassword) return true
        val cls = className.orEmpty()
        val rid = resourceId.orEmpty().lowercase()
        val hint = inputTypeHint.orEmpty().lowercase()
        if (cls.contains("Password", ignoreCase = true)) return true
        if (rid.contains("password") || rid.contains("otp") || rid.contains("pin") ||
            rid.contains("cvv") || rid.contains("pay_pwd")
        ) {
            return true
        }
        if (hint.contains("password") || hint.contains("otp")) return true
        return false
    }

    fun redactText(text: CharSequence?, secret: Boolean): String? {
        if (!secret) return text?.toString()
        if (text.isNullOrEmpty()) return PROTECTED
        return PROTECTED
    }

    fun roleFor(
        className: String?,
        clickable: Boolean,
        editable: Boolean,
        password: Boolean,
        checkable: Boolean = false,
    ): String {
        if (password) return "password_field"
        val cls = className.orEmpty()
        return when {
            editable || cls.contains("EditText", ignoreCase = true) -> "edit"
            checkable && cls.contains("Switch", ignoreCase = true) -> "switch"
            checkable -> "checkbox"
            cls.contains("Button", ignoreCase = true) -> "button"
            cls.contains("ImageView", ignoreCase = true) && clickable -> "button"
            clickable -> "button"
            cls.contains("WebView", ignoreCase = true) -> "webview"
            else -> "text"
        }
    }
}
