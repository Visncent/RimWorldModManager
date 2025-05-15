import hashlib

def check_dependencies(mods):
    errors = []
    for mod in mods:
        for dep in get_dependencies(mod):
            if dep not in CRITICAL_MODS and not any(m['packageId'] == dep for m in mods):
                errors.append(f"Мод {mod['name']} требует отсутствующий мод {dep}")
    return errors

def verify_hashes(mod):
    expected_hash = get_expected_hash(mod['packageId'])
    current_hash = hashlib.sha256(get_mod_file(mod, "Assemblies/Mod.dll").read_bytes()).hexdigest()
    return current_hash == expected_hash
