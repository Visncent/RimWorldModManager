from collections import deque

def topological_sort(mods):
    # Строим граф зависимостей и счетчик входящих связей
    graph = {mod['packageId']: set() for mod in mods}
    in_degree = {mod['packageId']: 0 for mod in mods}
    
    for mod in mods:
        dependencies = get_mod_dependencies(mod)  # Ваша функция для получения зависимостей
        for dep in dependencies:
            if dep in graph:
                graph[dep].add(mod['packageId'])
                in_degree[mod['packageId']] += 1
    
    # Очередь модов без зависимостей
    queue = deque([mod for mod in in_degree if in_degree[mod] == 0])
    sorted_mods = []
    
    while queue:
        current = queue.popleft()
        sorted_mods.append(current)
        
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(sorted_mods) != len(mods):
        raise ValueError("Обнаружены циклические зависимости!")
    
    return sorted_mods
