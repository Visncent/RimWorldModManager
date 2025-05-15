from core.mod_manager import ModManagerApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ModManagerApp(root)
    root.mainloop()
OFFICIAL_DLC = {
    "ludeon.rimworld.royalty": "Royalty DLC",
    "ludeon.rimworld.ideology": "Ideology DLC",
    "ludeon.rimworld.biotech": "Biotech DLC"
}
CRITICAL_MODS = {
    "ludeon.rimworld": "Core Game",
    "brrainz.harmony": "Harmony Library",
    "unlimitedhugs.hugslib": "HugsLib",
    "kentington.saveourship2": "Save Our Ship 2",
    **OFFICIAL_DLC  # Объединяем с DLC
}
class ModManagerApp:
    def setup_ui(self):
        critical_frame = ttk.Frame(self.root)
        critical_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(critical_frame, text="Добавить критический мод", 
                  command=self.add_critical_mod_dialog).pack(side=tk.LEFT)
        ttk.Button(critical_frame, text="Удалить критический мод", 
                  command=self.remove_critical_mod_dialog).pack(side=tk.LEFT, padx=5)
    def add_critical_mod_dialog(self):
        mod_id = simpledialog.askstring(
            "Добавить критический мод",
            "Введите PackageId мода (например: author.modname):",
            parent=self.root
        )
        if mod_id:
            mod_name = simpledialog.askstring(
                "Добавить критический мод",
                "Введите название мода:",
                parent=self.root
            )
            if mod_name:
                self.add_critical_mod(mod_id, mod_name)
    def add_critical_mod(self, mod_id, mod_name):
        if mod_id in CRITICAL_MODS:
            messagebox.showwarning("Предупреждение", "Этот мод уже в списке критических!")
            return
        CRITICAL_MODS[mod_id] = mod_name
        for mod in self.steam_mods + self.local_mods:
            if mod['packageId'] == mod_id:
                mod['status'] = "Critical"
        self.update_mod_tables()
        messagebox.showinfo("Успех", f"Мод {mod_name} добавлен в критические!")
    def remove_critical_mod_dialog(self):
        removable_mods = {k:v for k,v in CRITICAL_MODS.items() 
                        if k not in ["ludeon.rimworld"] 
                        and not k.startswith("ludeon.rimworld.")}
        if not removable_mods:
            messagebox.showinfo("Инфо", "Нет пользовательских критических модов для удаления")
            return
        mod_list = "\n".join([f"{i+1}. {v} ({k})" for i,(k,v) in enumerate(removable_mods.items())])
        choice = simpledialog.askinteger(
            "Удалить критический мод",
            f"Выберите мод для удаления:\n{mod_list}\n\nВведите номер:",
            parent=self.root,
            minvalue=1,
            maxvalue=len(removable_mods)
        if choice:
            mod_id = list(removable_mods.keys())[choice-1]
            self.remove_critical_mod(mod_id)
    def remove_critical_mod(self, mod_id):
        if mod_id not in CRITICAL_MODS:
            messagebox.showerror("Ошибка", "Мод не найден в списке!")
            return
        mod_name = CRITICAL_MODS.pop(mod_id)
        for mod in self.steam_mods + self.local_mods:
            if mod['packageId'] == mod_id:
                mod['status'] = "Active" if mod['active'] else "Inactive"
        self.update_mod_tables()
        messagebox.showinfo("Успех", f"Мод {mod_name} удалён из критических!")
    def update_mod_tables(self):
        self.update_mod_table(self.tree_steam, self.steam_mods)
        self.update_mod_table(self.tree_local, self.local_mods)
    def scan_mods_folder(self, path, mod_type):
        mods = []
        if not path.exists():
            return mods
        for mod_dir in path.iterdir():
            if not mod_dir.is_dir():
                continue
            manifest = mod_dir / "About/Manifest.xml"
            if not manifest.exists():
                continue
            try:
                tree = ET.parse(manifest)
                root = tree.getroot()
                mod_data = {
                    "id": mod_dir.name,
                    "name": root.findtext("name", "Unnamed"),
                    "author": root.findtext("author", "Unknown"),
                    "version": root.findtext("version", "1.0"),
                    "packageId": root.findtext("packageId", ""),
                    "path": str(mod_dir),
                    "type": mod_type,
                    "active": False,
                    "status": "Inactive"
                }
                if mod_data["packageId"] in OFFICIAL_DLC:
                    mod_data["status"] = "Official DLC"
                elif mod_data["packageId"] in CRITICAL_MODS:
                    mod_data["status"] = "Critical"
                if mod_data["packageId"] in self.active_mods:
                    mod_data["active"] = True
                    if mod_data["status"] == "Inactive":
                        mod_data["status"] = "Active"
                mods.append(mod_data)
            except ET.ParseError as e:
                print(f"Error parsing {manifest}: {e}")
        return mods
