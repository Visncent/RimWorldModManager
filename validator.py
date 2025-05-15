def check_mod_integration(mods):
    errors = []
    for mod in mods:
        for dep in get_mod_dependencies(mod):
            if dep not in CRITICAL_MODS and not any(m['packageId'] == dep for m in mods):
                errors.append(f"Мод {mod['name']} требует отсутствующий мод {dep}")
    
    # Проверка конфликтов (пример)
    mod_files = {}
    for mod in mods:
        for file in get_mod_files(mod):  # Ваша функция для получения файлов мода
            if file in mod_files:
                errors.append(f"Конфликт: файл {file} изменяется модами {mod_files[file]} и {mod['name']}")
            mod_files[file] = mod['name']
    
    return errors
