from processor import process_excel

INPUT_FILE = "MINA.xlsx"

print("Обработка...")

files, categories = process_excel(INPUT_FILE)

print("\nСозданы файлы:")

for file in files:
    print(f"✓ {file}")

print("\nСтатистика:")

for category, items in categories.items():
    print(f"{category}: {len(items)}")

print("\nГотово!")