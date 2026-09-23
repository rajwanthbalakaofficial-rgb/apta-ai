"""
Universal CLI Entry Point for apta AI - Interactive Terminal Interface.
"""

import sys
import argparse
import platform
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from agent import AptaAgent
from tools import UNIVERSAL_TOOLS

console = Console()

BANNER = """
 [bold cyan]==========================================================[/bold cyan]
   [bold yellow]🤖 apta AI (ఆప్త AI) - Universal Autonomous Agent[/bold yellow]
   [dim]Created for Rajwanth Balaka | Universal AI Engine[/dim]
 [bold cyan]==========================================================[/bold cyan]
"""

def display_help():
    help_text = """
### 🛠️ Interactive Commands:
- `/mode universal` : Switch to Universal Agent Mode (All tools + System engineering).
- `/mode coding`    : Switch to Code Developer Mode.
- `/mode udvega`    : Switch to Udvegadarshini Biofeedback Companion Mode.
- `/tools`          : List all registered Universal Tools.
- `/clear`          : Clear terminal screen.
- `/help`           : Show this help menu.
- `exit` / `quit`   : Exit the agent session.
"""
    console.print(Panel(Markdown(help_text), title="apta AI Help", border_style="yellow"))

def list_tools():
    tool_names = [f"• [bold cyan]{t.__name__}[/bold cyan]: {t.__doc__.strip().splitlines()[0]}" for t in UNIVERSAL_TOOLS]
    tools_text = "\n".join(tool_names)
    console.print(Panel(tools_text, title="Registered Universal Tools", border_style="green"))

def main():
    parser = argparse.ArgumentParser(description="apta AI Universal Autonomous Agent")
    parser.add_argument(
        "--mode",
        choices=["universal", "coding", "udvegadarshini"],
        default="universal",
        help="Operating mode: 'universal' (default), 'coding', or 'udvegadarshini'."
    )
    args = parser.parse_args()

    console.print(BANNER)
    
    current_mode = args.mode
    agent = AptaAgent(mode=current_mode)
    
    os_info = f"{platform.system()} {platform.release()}"
    console.print(f"[bold green]>>> System Environment:[/bold green] [bold white]{os_info}[/bold white]")
    console.print(f"[bold green]>>> Active Mode:[/bold green] [bold yellow]{current_mode.upper()}[/bold yellow]")
    console.print(f"[bold green]>>> Registered Tools:[/bold green] [bold cyan]{len(UNIVERSAL_TOOLS)} Universal Tools[/bold cyan]\n")

    if not agent.is_configured():
        console.print(
            "[yellow]⚠️ Note: GEMINI_API_KEY is not set in environment or .env file.[/yellow]\n"
            "[dim]Add GEMINI_API_KEY=your_key in apta-ai/.env to enable live Gemini AI execution.[/dim]\n"
        )

    console.print("[dim]Type your command/query. Type '/help' for options, 'exit' to quit.[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask(f"[bold magenta]Mama ({current_mode})[/bold magenta]")
            cmd = user_input.strip()
            if not cmd:
                continue
                
            if cmd.lower() in ["exit", "quit", "q"]:
                console.print("\n[bold cyan]Bye mama! Next time kaluddam! 👋[/bold cyan]")
                break
            elif cmd.lower() == "/help":
                display_help()
                continue
            elif cmd.lower() == "/tools":
                list_tools()
                continue
            elif cmd.lower() == "/clear":
                console.clear()
                console.print(BANNER)
                continue
            elif cmd.lower().startswith("/mode"):
                parts = cmd.split()
                if len(parts) > 1 and parts[1] in ["universal", "coding", "udvegadarshini", "udvega"]:
                    new_mode = "udvegadarshini" if parts[1] == "udvega" else parts[1]
                    current_mode = new_mode
                    agent = AptaAgent(mode=current_mode)
                    console.print(f"[bold green]Switched mode to: {current_mode.upper()}[/bold green]\n")
                else:
                    console.print("[yellow]Usage: /mode [universal | coding | udvegadarshini][/yellow]")
                continue

            console.print("\n[dim]apta AI is thinking...[/dim]")
            reply = agent.send_message(user_input)
            
            console.print("\n[bold yellow]apta AI:[/bold yellow]")
            console.print(Panel(Markdown(reply), border_style="cyan"))
            console.print()

        except KeyboardInterrupt:
            console.print("\n[bold cyan]Session terminated. Bye mama! 👋[/bold cyan]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()
