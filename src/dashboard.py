import time
import random
import sys
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

console = Console()

def boot_sequence():
    """Cyberpunk Boot Sequence Animation"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="[bold white]INITIALIZING MAVI VATAN KERNEL...[/]", total=100)
        time.sleep(1)
        progress.add_task(description="[bold cyan]LOADING NEURAL VISION (YOLO v11)...[/]", total=100)
        time.sleep(0.8)
        progress.add_task(description="[bold blue]ESTABLISHING ACOUSTIC LINK...[/]", total=100)
        time.sleep(0.7)
        progress.add_task(description="[bold red]FAILSAFE: WATCHDOG ARMED.[/]", total=100)
        time.sleep(0.5)
    
    console.print(Align.center("[bold green]>>> SYSTEM READY: ELITE STATUS ACTIVE <<<[/bold green]"))
    time.sleep(1)

def make_layout() -> Layout:
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1),
    )
    layout["left"].split_column(
        Layout(name="telemetry", ratio=1),
        Layout(name="failsafe", ratio=1),
    )
    layout["right"].split_column(
        Layout(name="checklist", ratio=1),
        Layout(name="mission", ratio=1),
    )
    return layout

class Header:
    def __rich__(self) -> Panel:
        return Panel(
            Align.center("[bold cyan]🔱 MAVİ VATAN: STRATEJİK KOMUTA MERKEZİ 🔱[/bold cyan]"),
            style="bold cyan"
        )

def generate_telemetry():
    table = Table(title="[bold green]📊 SİSTEM TELEMETRİSİ[/bold green]", expand=True, border_style="green")
    table.add_column("Parametre", style="cyan")
    table.add_column("Değer", style="white")
    table.add_row("Derinlik (m)", f"{random.uniform(2.0, 5.0):.2f}", "[bold green]STABİL[/bold green]")
    table.add_row("Vakum Seviyesi", "0.85 bar", "[bold green]GÜVENLİ[/bold green]")
    table.add_row("Sıcaklık (CPU)", f"{random.randint(45, 55)}°C", "[bold yellow]NOMİNAL[/bold yellow]")
    table.add_row("Drift (m/s)", f"{random.uniform(0.01, 0.05):.3f}", "[bold blue]CORRECTED[/bold blue]")
    return Panel(table, border_style="green")

def generate_checklist():
    table = Table(title="[bold blue]📋 PRE-FLIGHT CHECKLIST[/bold blue]", expand=True, border_style="blue")
    table.add_column("Kontrol Noktası", style="white")
    table.add_column("Durum", style="bold green")
    table.add_row("O-Ring Sızdırmazlık", "✅ TAM")
    table.add_row("Drop Weight Pimleri", "✅ SERBEST")
    table.add_row("Anodize Gövde Bütünlüğü", "✅ ONAYLI")
    table.add_row("Kill-Switch Testi", "✅ BAŞARILI")
    return Panel(table, border_style="blue")

def generate_failsafe():
    return Panel(
        Align.center("[bold white]DİJİTAL BEKÇİ (WATCHDOG):[/bold white] [bold green]AKTİF[/bold green]\n"
                     "[bold white]SIZINTI SENSÖRÜ:[/bold white] [bold green]NEGATİF[/bold green]\n"
                     "[bold white]KOMÜNİKASYON:[/bold white] [bold yellow]AKUSTİK MOD KİTLİ[/bold yellow]"),
        title="[bold red]🛡️ FAILSAFE MONITOR[/bold red]",
        border_style="red"
    )

def generate_mission():
    states = ["STANDBY", "DIVING", "WAYPOINT_NAV", "OBJECT_DETECTION", "SURFACE"]
    current_state = states[int(time.time() / 2) % len(states)]
    return Panel(
        Align.center(f"[bold magenta]DURUM: {current_state}[/bold magenta]\n"
                     f"[italic white]'{current_state}' Görev Safhası İcra Ediliyor...[/italic white]"),
        title="[bold magenta]🚀 GÖREV YÖNETİCİSİ[/bold magenta]",
        border_style="magenta"
    )

def main():
    boot_sequence()
    layout = make_layout()
    layout["header"].update(Header())
    layout["footer"].update(Panel(Align.center("[italic white]Derinliklerin Sessizliğinde Mühendislik Mirası İnşa Ediliyor...[/italic white]")))
    
    with Live(layout, refresh_per_second=4, screen=True):
        try:
            while True:
                layout["telemetry"].update(generate_telemetry())
                layout["checklist"].update(generate_checklist())
                layout["failsafe"].update(generate_failsafe())
                layout["mission"].update(generate_mission())
                time.sleep(0.2)
        except KeyboardInterrupt:
            console.print("\n[bold red]TERMINATING COMMAND CENTER...[/bold red]")
            sys.exit()

if __name__ == "__main__":
    main()
