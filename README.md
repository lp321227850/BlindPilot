# BlindPilot

面向盲人用户的语音优先 Android 手机助手。无 Root，无 Shizuku，无运行时 ADB。

[网站](https://freus.cn) · [安全说明](SECURITY.md) · [贡献](CONTRIBUTING.md) · [上游 Andclaw](https://github.com/andforce/Andclaw)

BlindPilot 不是“AI 能点按钮”。成功标准是盲人用户可以：

- 用语音发起任务
- 听到简洁、明确的进度
- 随时本地停止
- 网络或 Agent 故障时安全失败
- 对发消息、打电话明确确认
- 绝不把密码 / 验证码等 SECRET 交给云端

## 现在做到哪一步

| 里程碑 | 状态 |
|---|---|
| M0 上游审计 + 未改行为的 debug 构建 | 完成 |
| M1 无障碍核心（无 AI 手工动作） | 完成。站点 https://freus.cn ，调试包可下载 |
| M2 ScreenState / StableNodeId | 未开始 |
| M3 语音 + TalkBack | 未开始 |
| M4 设备配对与 WSS | 服务端骨架已有，Android 未接 |
| M5 Antigravity `phone_observe` | 未开始（无第二模型回退） |
| M6–M12 自治循环、安全、Route Replay、发布 | 未开始 |

当前 APK 仍使用上游 applicationId `com.andforce.andclaw`，避免无谓改包名。请从主界面打开 **BlindPilot 无障碍核心**，不要用 Telegram/Kimi 作为盲人主路径。

调试包：https://freus.cn/downloads/Andclaw.apk

完整 git 历史（含 Andclaw 上游）：

```bash
git clone https://freus.cn/downloads/blindpilot.bundle BlindPilot
```

## 架构

```text
盲人用户 --语音--> Android BlindPilot
                      AccessibilityService / ScreenState / 本地停止
                      DeviceWebSocket (WSS)
                           |
                           v
                     VPS (Caddy + FastAPI)
                      DeviceHub / SafetyEngine / AgentRunner
                           |
                           v
                     Antigravity Agent（唯一运行时云端 AI）
                           |
                     类型化 phone_* 工具
                           |
                           v
                     手机执行，不给 Agent 开 shell
```

## 本机构建 Android

需要 JDK 17+、Android SDK 36。上游没有 `gradlew.bat`，Windows 用 Git Bash：

```bash
export ANDROID_HOME=/e/SDK
export JAVA_HOME="/c/Program Files/Microsoft/jdk-21.0.11.10-hotspot"
./gradlew :app:testDebugUnitTest :app:assembleDebug
```

详细命令见 `docs/BUILD.md`。

手工验收 M1（不需要 AI）：

1. 启用无障碍服务（设置里能听到服务说明）。
2. 打开「BlindPilot 无障碍核心」。
3. 依次：朗读屏幕、点击节点、长按、输入文字、滚动、上滑、返回、桌面、打开设置、打开时钟、截屏（仅内存）。
4. 点「本地停止」后再点点击，应被拒绝。

## 后端

```bash
cd server
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"   # Linux: .venv/bin/pip
.venv/Scripts/pytest
.venv/Scripts/uvicorn app.main:app --host 127.0.0.1 --port 8080
```

生产目录约定 `/opt/blindpilot/`。Caddy 终止 TLS，反代 `/v1/` 与 `/health/`。Docker Compose 在 `deploy/docker-compose.yml`；1 核小机器也可以用 systemd + venv。

## 硬约束

- 运行时云端 AI **只有** Antigravity Agent。
- 禁止 Gemini `generateContent` 回退，禁止 OpenAI / Grok / Anthropic 运行时。
- v1 工具是 Custom Functions，不是 Remote MCP。
- Grok 只用于写代码，不进入生产决策环。

## 许可证

MIT。Android 底座来自 [andforce/Andclaw](https://github.com/andforce/Andclaw)（MIT）。
