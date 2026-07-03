#!/usr/bin/env python3
import os
import shutil
import argparse
import configparser
from pathlib import Path

HOME = Path.home()
DOTFILES = HOME / "dotfiles"

# Locate Mackup's database
MACKUP_APPS_DIR = Path("mackup/src/mackup/applications")

# Termux specific global python path backup
TERMUX_MACKUP_DIR = Path("/data/data/com.termux/files/usr/lib/python3.13/site-packages/mackup/applications")

if not MACKUP_APPS_DIR.exists():
    if TERMUX_MACKUP_DIR.exists():
        MACKUP_APPS_DIR = TERMUX_MACKUP_DIR
    else:
        try:
            import mackup
            # Guard against __file__ being None or missing
            if hasattr(mackup, '__file__') and mackup.__file__:
                MACKUP_APPS_DIR = Path(str(mackup.__file__)).parent / "applications"
        except (ImportError, AttributeError, TypeError):
            pass

def get_stow_paths(cfg_path):
    config = configparser.ConfigParser(allow_no_value=True)
    try:
        config.read(cfg_path)
    except Exception:
        return []

    paths = []
    if config.has_section('configuration_files'):
        for option in config.options('configuration_files'):
            paths.append((option, HOME / option))
    if config.has_section('xdg_configuration_files'):
        for option in config.options('xdg_configuration_files'):
            paths.append((f".config/{option}", HOME / ".config" / option))
    return paths

def check_status(full_src_path, target_dest):
    """Evaluates the state of the home file relative to the dotfiles repo."""
    if not full_src_path.exists():
        return "Not Installed"
        
    if not target_dest.exists():
        return "🟢 Missing from Repo (New)"
        
    # Check if they point to the exact same data / are symlinked
    try:
        if full_src_path.stat() == target_dest.stat():
            if full_src_path.is_link():
                return "🔗 Managed (Symlinked via Stow)"
            return "✅ Matched (Identical Content)"
    except Exception:
        pass
        
    return "⚠️ Out of Sync (Modified)"

def run_list():
    print(f"🔍 Auditing system config files against {DOTFILES}...\n")
    print(f"{'Package':<15} {'Relative Path':<40} {'Status'}")
    print("-" * 80)
    
    for cfg_file in MACKUP_APPS_DIR.glob("*.cfg"):
        pkg_name = cfg_file.stem
        mappings = get_stow_paths(cfg_file)
        
        for rel_path, full_src_path in mappings:
            if full_src_path.exists():
                target_dest = DOTFILES / pkg_name / rel_path
                status = check_status(full_src_path, target_dest)
                print(f"{pkg_name:<15} {rel_path:<40} {status}")

def run_sync():
    print(f"🚀 Seeding configurations into {DOTFILES}...")
    DOTFILES.mkdir(exist_ok=True)

    for cfg_file in MACKUP_APPS_DIR.glob("*.cfg"):
        pkg_name = cfg_file.stem
        mappings = get_stow_paths(cfg_file)
        
        for rel_path, full_src_path in mappings:
            if full_src_path.exists():
                target_dest = DOTFILES / pkg_name / rel_path
                
                # Use our exact stat check from earlier to skip exact matches
                if target_dest.exists() and full_src_path.stat() == target_dest.stat():
                    continue
                    
                print(f"✨ Migrating [{pkg_name}]: {rel_path}")
                target_dest.parent.mkdir(parents=True, exist_ok=True)
                
                if full_src_path.is_dir():
                    if target_dest.exists():
                        shutil.rmtree(target_dest)
                    shutil.copytree(full_src_path, target_dest)
                else:
                    shutil.copy2(full_src_path, target_dest)
    print("\n🎉 Seeding phase finished!")

def main():
    if not MACKUP_APPS_DIR.exists():
        print(f"❌ Mackup database directory not found. Please verify paths.")
        return

    parser = argparse.ArgumentParser(description="Stow-Seed: A discovery tool bridging Mackup data to GNU Stow structures.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Subcommands
    subparsers.add_parser("list", help="Scan and compare active system profiles against the local repo.")
    subparsers.add_parser("sync", help="Copy unmanaged application configurations into your stow structured repo.")

    args = parser.parse_args()

    if args.command == "list":
        run_list()
    elif args.command == "sync":
        run_sync()

if __name__ == "__main__":
    main()

