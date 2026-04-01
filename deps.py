import subprocess
import sys
import shutil
import log
from pathlib import Path


def download_dependencies() -> None:
    """
    Downloads Elite.SpanshTools via dotnet publish and places the DLLs in ./lib/.
    """
    # Capture the lib folder location as well as the csproj name for the nuget package so they can be retrieved
    root = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
    csproj = root / "nuget_restore" / "restore.csproj"
    libfolder = root / "lib"

    # The dotnet CLI must be installed to work.  It comes with the .NET SDK.
    if not shutil.which("dotnet"):
        log.writeln("ERROR: 'dotnet' CLI not found. Install .NET 8 SDK from https://dotnet.microsoft.com/download")
        sys.exit(1)

    # Restore the package
    log.writeln("Restoring NuGet packages via dotnet publish...")
    result = subprocess.run(
        [
            "dotnet", "publish",
            str(csproj),
            "--configuration", "Release",
            "--output", str(libfolder),
            "--nologo",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.writeln("dotnet publish failed:\n")
        log.writeln(result.stdout)
        log.writeln(result.stderr)
        sys.exit(result.returncode)

    log.writeln(f"DLLs written to {libfolder}")
    dlls = sorted(libfolder.glob("*.dll"))
    for dll in dlls:
        log.writeln(f"  {dll.name}")