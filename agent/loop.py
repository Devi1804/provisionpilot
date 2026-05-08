"""Main agent loop. Uses the Anthropic SDK with tool use."""
import json
import os
from anthropic import Anthropic
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax

from agent.tools import TOOL_SCHEMAS, TOOL_DISPATCH, MUTATING_TOOLS

console = Console()
client = Anthropic()

SYSTEM_PROMPT = """You are ProvisionPilot, an agent that provisions VMs from natural-language intents.

Your workflow for any provisioning request:
1. Call search_release_notes FIRST with relevant terms. Surface any warnings.
2. Call read_current_inventory to see what's already running.
3. Build a spec (list of VMs with names and roles).
4. Call render_vagrantfile and render_inventory to preview the configs.
5. Show the user the spec and rendered diff. STOP and ask the user to confirm in chat.
6. Once the user confirms (e.g. "yes", "approve", "go"): call write_to_state_repo,
   run_vagrant_up, run_ansible_apply, git_commit_and_push in order. The system will
   prompt the user to approve each mutating tool individually.

VM naming:
- web role: web1, web2, ...
- db role: db1, db2, ...
- app role: app1, app2, ...
- Networking is handled by Vagrant's SSH port forwarding and a dummy-interface bond on each VM.

Never call mutating tools without an explicit user confirmation in chat first.
Be concise."""


def run_session(initial_prompt: str):
    """Interactive agent session. Loops on end_turn so the user can keep talking."""
    messages = [{"role": "user", "content": initial_prompt}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        # Print any text the assistant produced
        for block in response.content:
            if block.type == "text":
                console.print(f"\n[bold cyan]Agent:[/] {block.text}")

        if response.stop_reason == "end_turn":
            # Agent finished its turn — wait for user's next message
            messages.append({"role": "assistant", "content": response.content})
            try:
                user_input = console.input("\n[bold green]You:[/] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Session ended.[/]")
                break
            if not user_input or user_input.lower() in {"exit", "quit", "bye"}:
                console.print("[dim]Session ended.[/]")
                break
            messages.append({"role": "user", "content": user_input})
            continue

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                console.print(f"\n[yellow]→ Tool call:[/] {block.name}")
                console.print(Syntax(json.dumps(block.input, indent=2), "json"))

                if block.name in MUTATING_TOOLS:
                    if not Confirm.ask(f"[red]Approve {block.name}?[/]", default=False):
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": "User declined this action. Stop and ask the user what to do next.",
                            "is_error": True,
                        })
                        continue

                try:
                    result = TOOL_DISPATCH[block.name](**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Error: {e}",
                        "is_error": True,
                    })

            messages.append({"role": "user", "content": tool_results})
            continue

        console.print(f"[red]Unexpected stop_reason: {response.stop_reason}[/]")
        break