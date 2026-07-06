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

def is_in_sync(src: Path, dest: Path) -> bool:
    """
    Compare src/dest without relying on the full os.stat_result tuple
    (which includes inode/device/atime and will basically never match
    across two separate files, even identical copies).

    A symlink pointing at src always counts as in sync. Otherwise fall
    back to size + mtime, which is what copy2() preserves.
    """
    try:
        if dest.is_symlink() and dest.resolve() == src.resolve():
            return True

        src_stat = src.stat()
        dest_stat = dest.stat()

        if src.is_dir() and dest.is_dir():
            # Cheap directory check: same immediate entry count + names.
            # (Not a deep recursive diff, but avoids false negatives from stat().)
            return sorted(p.name for p in src.iterdir()) == sorted(p.name for p in dest.iterdir())

        return (
            src_stat.st_size == dest_stat.st_size
            and int(src_stat.st_mtime) <= int(dest_stat.st_mtime)
        )
    except Exception:
        return False

def check_status(full_src_path, target_dest):
    """Evaluates the state of the home file relative to the dotfiles repo."""
    if not full_src_path.exists():
        return "Not Installed"

    if not target_dest.exists():
        return "🟢 Missing from Repo (New)"

    if is_in_sync(full_src_path, target_dest):
        if full_src_path.is_symlink():
            return "🔗 Managed (Symlinked via Stow)"
        return "✅ Matched (Identical Content)"

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

def run_sync(packages=None):
    """
    Seed configs into DOTFILES.

    packages: optional list of package names (cfg stem) to restrict the
    sync to. If None or empty, all discovered packages are synced.
    """
    if packages:
        print(f"🚀 Seeding configurations into {DOTFILES} for: {', '.join(packages)}...")
    else:
        print(f"🚀 Seeding configurations into {DOTFILES}...")
    DOTFILES.mkdir(exist_ok=True)

    wanted = set(packages) if packages else None
    matched_any = set()

    for cfg_file in MACKUP_APPS_DIR.glob("*.cfg"):
        pkg_name = cfg_file.stem

        if wanted is not None and pkg_name not in wanted:
            continue
        if wanted is not None:
            matched_any.add(pkg_name)

        mappings = get_stow_paths(cfg_file)

        for rel_path, full_src_path in mappings:
            if full_src_path.exists():
                target_dest = DOTFILES / pkg_name / rel_path

                if target_dest.exists() and is_in_sync(full_src_path, target_dest):
                    continue

                print(f"✨ Migrating [{pkg_name}]: {rel_path}")
                target_dest.parent.mkdir(parents=True, exist_ok=True)

                if full_src_path.is_dir():
                    if target_dest.exists():
                        shutil.rmtree(target_dest)
                    shutil.copytree(full_src_path, target_dest)
                else:
                    shutil.copy2(full_src_path, target_dest)

    if wanted is not None:
        unknown = wanted - matched_any
        if unknown:
            print(f"\n⚠️  No .cfg found for: {', '.join(sorted(unknown))} (check package name / list command)")

    print("\n🎉 Seeding phase finished!")

def main():
    if not MACKUP_APPS_DIR.exists():
        print(f"❌ Mackup database directory not found. Please verify paths.")
        return

    parser = argparse.ArgumentParser(description="Stow-Seed: A discovery tool bridging Mackup data to GNU Stow structures.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommands
    subparsers.add_parser("list", help="Scan and compare active system profiles against the local repo.")

    sync_parser = subparsers.add_parser("sync", help="Copy unmanaged application configurations into your stow structured repo.")
    sync_parser.add_argument(
        "packages",
        nargs="*",
        help="Optional: one or more package names (matching a mackup .cfg stem, e.g. 'git' 'vim') to sync. Omit to sync everything.",
    )

    args = parser.parse_args()

    if args.command == "list":
        run_list()
    elif args.command == "sync":
        run_sync(args.packages)

if __name__ == "__main__":
    main()
