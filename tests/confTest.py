"""Pytest setup — provide env vars before agent.tools is imported."""
import os
import tempfile

# These run before pytest collects test modules, so by the time
# tests/test_render.py does `from agent.tools import ...`, the env
# vars exist. We point at a throwaway temp dir, not the real state repo.
os.environ.setdefault("STATE_REPO_PATH", tempfile.mkdtemp(prefix="pp-test-state-"))
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-used")