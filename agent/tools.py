"""Tools the agent can call. Each is a plain Python function with a JSON-schema description."""
import json
import os
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from rag.search import search as rag_search

REPO_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = REPO_ROOT / "infra-templates"
STATE_REPO = Path(os.environ["STATE_REPO_PATH"])

_jinja = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


# ---------- Tool implementations ----------

def search_release_notes(query: str) -> dict:
    """Search the release notes RAG index. Returns top 5 matches."""
    results = rag_search(query, k=5)
    return {"results": results}


def read_current_inventory() -> dict:
    """Read the current Vagrantfile and inventory from the state repo."""
    vagrantfile = STATE_REPO / "current" / "Vagrantfile"
    inventory = STATE_REPO / "current" / "hosts.ini"
    return {
        "vagrantfile": vagrantfile.read_text() if vagrantfile.exists() else "",
        "inventory": inventory.read_text() if inventory.exists() else "",
    }


def render_vagrantfile(spec: dict) -> dict:
    """Render a Vagrantfile from a spec. spec = {vms: [{name, ip_mgmt, ip_data, role}], memory_mb, cpus}."""
    template = _jinja.get_template("Vagrantfile.j2")
    rendered = template.render(**spec)
    return {"rendered": rendered}


def render_inventory(spec: dict) -> dict:
    """Render an Ansible inventory from a spec."""
    vms_by_role = {}
    for vm in spec["vms"]:
        vms_by_role.setdefault(vm["role"], []).append(vm)
    template = _jinja.get_template("inventory.j2")
    rendered = template.render(vms_by_role=vms_by_role)
    return {"rendered": rendered}


def write_to_state_repo(vagrantfile: str, inventory: str) -> dict:
    """Write rendered files into the state repo's `current/` dir."""
    current = STATE_REPO / "current"
    current.mkdir(parents=True, exist_ok=True)
    (current / "Vagrantfile").write_text(vagrantfile)
    (current / "hosts.ini").write_text(inventory)
    return {"status": "written", "path": str(current)}


def run_vagrant_up() -> dict:
    """Run `vagrant up` against the state repo's Vagrantfile."""
    result = subprocess.run(
        ["vagrant", "up"],
        cwd=STATE_REPO / "current",
        capture_output=True,
        text=True,
        timeout=900,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:],  # last 2K chars
        "stderr": result.stderr[-2000:],
    }


def run_ansible_apply() -> dict:
    """Run the Ansible playbook against the current inventory."""
    playbook = REPO_ROOT / "ansible" / "site.yml"
    inventory = STATE_REPO / "current" / "hosts.ini"
    result = subprocess.run(
        ["ansible-playbook", "-i", str(inventory), str(playbook)],
        capture_output=True,
        text=True,
        timeout=900,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
    }


def git_commit_and_push(message: str) -> dict:
    """Commit current state and push to the state repo's main branch (or open PR)."""
    subprocess.run(["git", "-C", str(STATE_REPO), "add", "."], check=True)
    result = subprocess.run(
        ["git", "-C", str(STATE_REPO), "commit", "-m", message],
        capture_output=True, text=True,
    )
    if result.returncode != 0 and "nothing to commit" in result.stdout:
        return {"status": "no_changes"}
    push = subprocess.run(
        ["git", "-C", str(STATE_REPO), "push"],
        capture_output=True, text=True,
    )
    return {"status": "pushed" if push.returncode == 0 else "failed", "stderr": push.stderr}


def vagrant_destroy() -> dict:
    """Tear down all VMs."""
    result = subprocess.run(
        ["vagrant", "destroy", "-f"],
        cwd=STATE_REPO / "current",
        capture_output=True, text=True, timeout=600,
    )
    return {"returncode": result.returncode, "stdout": result.stdout[-1000:]}


# ---------- Tool schemas (for Claude) ----------

TOOL_SCHEMAS = [
    {
        "name": "search_release_notes",
        "description": "Search release notes for known issues, regressions, or version constraints. ALWAYS call this before provisioning.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "read_current_inventory",
        "description": "Read the current fleet state from the GitOps repo.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "render_vagrantfile",
        "description": "Render a Vagrantfile from a spec. Does NOT run anything yet.",
        "input_schema": {
            "type": "object",
            "properties": {
                "spec": {
                    "type": "object",
                    "properties": {
                        "vms": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "role": {"type": "string", "enum": ["web", "db", "app"]},
                                },
                                "required": ["name", "role"],
                            },
                        },
                        "memory_mb": {"type": "integer", "default": 1024},
                        "cpus": {"type": "integer", "default": 1},
                    },
                    "required": ["vms"],
                },
            },
            "required": ["spec"],
        },
    },
    {
        "name": "render_inventory",
        "description": "Render an Ansible inventory from the same spec.",
        "input_schema": {
            "type": "object",
            "properties": {"spec": {"type": "object"}},
            "required": ["spec"],
        },
    },
    {
        "name": "write_to_state_repo",
        "description": "Write the rendered Vagrantfile and inventory into the GitOps state repo. REQUIRES user approval first.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vagrantfile": {"type": "string"},
                "inventory": {"type": "string"},
            },
            "required": ["vagrantfile", "inventory"],
        },
    },
    {
        "name": "run_vagrant_up",
        "description": "Boot the VMs. REQUIRES user approval. Takes 1-5 minutes.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "run_ansible_apply",
        "description": "Run Ansible playbook against the running VMs. REQUIRES user approval.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "git_commit_and_push",
        "description": "Commit and push to the GitOps state repo. Call after a successful provision.",
        "input_schema": {
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"],
        },
    },
    {
        "name": "vagrant_destroy",
        "description": "Destroy all VMs. REQUIRES user approval.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

TOOL_DISPATCH = {
    "search_release_notes": lambda **kw: search_release_notes(**kw),
    "read_current_inventory": lambda **kw: read_current_inventory(),
    "render_vagrantfile": lambda **kw: render_vagrantfile(**kw),
    "render_inventory": lambda **kw: render_inventory(**kw),
    "write_to_state_repo": lambda **kw: write_to_state_repo(**kw),
    "run_vagrant_up": lambda **kw: run_vagrant_up(),
    "run_ansible_apply": lambda **kw: run_ansible_apply(),
    "git_commit_and_push": lambda **kw: git_commit_and_push(**kw),
    "vagrant_destroy": lambda **kw: vagrant_destroy(),
}

MUTATING_TOOLS = {
    "write_to_state_repo",
    "run_vagrant_up",
    "run_ansible_apply",
    "git_commit_and_push",
    "vagrant_destroy",
}