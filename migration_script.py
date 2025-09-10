import json

DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080
LAYOUTS_FILE = 'backend/scene_layouts.json'

def migrate_layouts():
    try:
        with open(LAYOUTS_FILE, 'r', encoding='utf-8') as f:
            layouts = json.load(f)
    except FileNotFoundError:
        print(f"Error: {LAYOUTS_FILE} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {LAYOUTS_FILE}.")
        return

    print("Starting migration...")
    updated = False
    for scene_name, layout in layouts.items():
        for sp in layout.get('spawn_points', []):
            # Check if migration is needed by looking for large coordinate values
            if isinstance(sp.get('x'), int) and sp.get('x') > 1:
                print(f"Migrating spawn point {sp.get('id', '')} in scene '{scene_name}'...")
                sp['x'] = sp['x'] / DESIGN_WIDTH
                sp['y'] = sp['y'] / DESIGN_HEIGHT
                sp['width'] = sp['width'] / DESIGN_WIDTH
                sp['height'] = sp['height'] / DESIGN_HEIGHT
                updated = True

            for sc in sp.get('subjects_config', []):
                if isinstance(sc.get('width'), int) and sc.get('width') > 1:
                    print(f"  Migrating subject '{sc.get('name')}' config...")
                    sc['width'] = sc['width'] / DESIGN_WIDTH
                    sc['height'] = sc['height'] / DESIGN_HEIGHT
                    updated = True
    
    if updated:
        try:
            with open(LAYOUTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(layouts, f, indent=2, ensure_ascii=False)
            print("Migration successful! Layouts file has been updated with relative values.")
        except Exception as e:
            print(f"Error writing updated layouts file: {e}")
    else:
        print("No migration needed. Values appear to be relative already.")

if __name__ == "__main__":
    migrate_layouts()
