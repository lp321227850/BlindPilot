# Contributing to BlindPilot

This project is for a real blind user. Reliability and safe failure beat clever architecture.

## Milestone rule

Do not start the next milestone until the current one is accepted.

Current engineering loop for every change:

1. Read the existing code.
2. File-level plan.
3. Smallest coherent change.
4. Tests.
5. Android debug build and/or backend tests.
6. Update docs.
7. Commit.

## Do not

- Add OpenAI, Gemini generateContent, Grok, or Anthropic as a **runtime** model.
- Add shell / ADB / arbitrary Intent / arbitrary HTTP phone tools.
- Persist screenshots by default.
- Rewrite TestDPC or the Andclaw LLM loop without a concrete reason.

## TalkBack

New UI must have content descriptions, 56dp minimum targets, and live-region status text.
Do not request `flagRequestFilterKeyEvents` unless there is a measured need.
