"""ProvisionPilot CLI."""
import os
import subprocess
import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

from agent.loop import run_session

app = typer.Typer(help="ProvisionPilot — conversational VM provisioning.")
console = Console()


@app.command()
def chat(intent: str = typer.Argument(..., help="What you want, in plain English.")):
    """Start a provisioning session."""
    console.print(f"[bold]Intent:[/] {intent}\n")
    run_session(intent)


@app.command()
def status():
    """Show currently running VMs."""
    state_repo = os.environ["STATE_REPO_PATH"]
    result = subprocess.run(
        ["vagrant", "status"],
        cwd=f"{state_repo}/current",
        capture_output=True, text=True,
    )
    console.print(result.stdout)


@app.command()
def history(n: int = 10):
    """Show the last N provisioning commits from the GitOps repo."""
    state_repo = os.environ["STATE_REPO_PATH"]
    result = subprocess.run(
        ["git", "-C", state_repo, "log", f"-{n}", "--oneline"],
        capture_output=True, text=True,
    )
    table = Table("Commit", "Message")
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        sha, _, msg = line.partition(" ")
        table.add_row(sha, msg)
    console.print(table)


if __name__ == "__main__":
    app()