#!/usr/bin/env python3
import os
import shutil
import configparser
from pathlib import Path

HOME = Path.home()
DOTFILES = HOME / "dotfiles"

# Locate Mackup's application configs (works if installed via pip/pacman/etc.)
# If you cloned the repo, point this directly to the 'mackup/applications' folder.
MACKUP_APPS_DIR = Path("mackup/src/mackup/applications")
# Fallback helper if installed via alternative python paths:
if not MACKUP_APPS_DIR.exists():
    import mackup
    MACKUP_APPS_DIR = Path(mackup.__file__).parent / "applications"

def get_stow_paths(cfg_path):
    """Parses a Mackup .cfg file to find matching source configuration items."""
    config = configparser.ConfigParser(allow_no_value=True)
    try:
        config.read(cfg_path)
    except Exception:
        return []

    paths = []
    
    # 1. Look for standard home files
    if config.has_section('configuration_files'):
        for option in config.options('configuration_files'):
            paths.append((option, HOME / option))
            
    # 2. Look for XDG standard files (~/.config)
    if config.has_section('xdg_configuration_files'):
        for option in config.options('xdg_configuration_files'):
            paths.append((f".config/{option}", HOME / ".config" / option))
            
    return paths

def main():
    print("🚀 Ingesting Mackup database for individual Stow structures...")
    DOTFILES.mkdir(exist_ok=True)

    if not MACKUP_APPS_DIR.exists():
        print(f"❌ Could not automatically find Mackup database at {MACKUP_APPS_DIR}")
        print("Please modify MACKUP_APPS_DIR to point to your mackup/applications folder.")
        return

    for cfg_file in MACKUP_APPS_DIR.glob("*.cfg"):
        pkg_name = cfg_file.stem  # e.g., 'nvim', 'kitty', 'git'
        mappings = get_stow_paths(cfg_file)
        
        for rel_path, full_src_path in mappings:
            # Only migrate if the user actually has this file/directory configured
            if full_src_path.exists():
                print(f"✨ Found config for [{pkg_name}]: {rel_path}")
                
                # Formulate the target stow structure: ~/dotfiles/pkg_name/relative_path
                target_dest = DOTFILES / pkg_name / rel_path
                target_dest.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy things cleanly over safely
                if full_src_path.is_dir():
                    if target_dest.exists():
                        shutil.rmtree(target_dest)
                    shutil.copytree(full_src_path, target_dest)
                else:
                    shutil.copy2(full_src_path, target_dest)
                    
    print(f"\n🎉 Complete! Your dotfiles are separated and ready for Stow at {DOTFILES}")

if __name__ == "__main__":
    main()
