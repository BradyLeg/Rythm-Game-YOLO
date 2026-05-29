# input

This service performs active input actions (keyboard presses or emulator gamepad events) on behalf of the app.

Purpose
- Execute user-intended actions derived from STT (mapped commands) by sending native keyboard events or emulating a gamepad.

Responsibilities
- Expose a small API (e.g. `perform_action(action_name, params)`) used by the `stt` and orchestrator layers.
- Support two backends: native keyboard/mouse and virtual gamepad (emulator).
- Provide safe toggles and fail-safes to prevent unwanted repeated input.

Recommended libraries (Windows)
- Native keyboard/mouse: `pyautogui`, `keyboard` (note: `keyboard` requires admin on Windows).
- Virtual gamepad / emulation:
  - `vgamepad` (wrapper around ViGEm) — preferred for modern virtual Xbox controllers.
  - `pyvjoy` for vJoy-based setups (older, requires vJoy driver).

Implementation notes
- Keep a backend-agnostic action enum (e.g. `PRESS_A`, `PRESS_UP`, `HOLD_LEFT`) and translate to library-specific calls.
- Expose a simple configuration to choose the active backend at runtime (e.g. `backend: keyboard|vgamepad`).
- When using virtual gamepad drivers, document driver installation steps and required user permissions.

Testing
- Add a `dry_run` mode that logs actions instead of sending them — useful for development and CI.

Security and safety
- Add an emergency stop (keyboard shortcut) and a maximum repeat limit to avoid runaway input.

Example usage
- `perform_action("press_up")` -> sends keyboard arrow up or corresponding gamepad D-pad event.
