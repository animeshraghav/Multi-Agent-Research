from rich.console import Console

console = Console()

def print_header(title: str):
    console.rule(f"[bold cyan]{title}")

def print_success(message: str):
    console.print(f"[green]{message}")

def print_warning(message: str):
    console.print(f"[yellow]{message}")

def print_error(message: str):
    console.print(f"[red]{message}")