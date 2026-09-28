import tomlkit

def deep_merge(base, overlay):
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base

def merge_files(paths, output_path):
    with open(paths[0]) as f:
        merged = tomlkit.parse(f.read())

    for path in paths[1:]:
        with open(path) as f:
            overlay = tomlkit.parse(f.read())
        deep_merge(merged, overlay)

    with open(output_path, "w") as f:
        f.write(tomlkit.dumps(merged))

merge_files(["palette.toml", "style.toml", "symbol.toml", "extra.toml"], "../starship/.config/starship.toml")
