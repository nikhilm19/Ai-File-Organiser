import os
import sys
import shutil
import json
import re
from pathlib import Path
import google.generativeai as genai

# --- CONFIGURATION ---
genai.configure(api_key=os.environ.get("GEMINI"))
print("🕵️ Searching for available models...\n")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
TARGET_DIR = Path("../")  # Change this to your target directory
HISTORY_FILE = TARGET_DIR / ".organizer_history.json"

def get_safe_path(dest_folder, filename):
    """Ensures we NEVER overwrite a file."""
    base_name, ext = os.path.splitext(filename)
    counter = 1
    safe_path = dest_folder / filename
    
    while safe_path.exists():
        safe_path = dest_folder / f"{base_name}_{counter}{ext}"
        counter += 1
    return safe_path

def suggest_folder_structure(file_names):
    """Asks Gemini to analyze the files and propose semantic folders."""
    print("🧠 Analyzing file semantics and determining the most practical structure...")
    
    prompt = f"""
    You are a highly intelligent, practical file organizer.
    I have a messy folder containing these exact files:
    {', '.join(file_names)}
    
    Group these files into clear, straightforward, and highly practical folder names based on their context. 
    Match my personal folder naming style exactly. My style is literal, project-based, and uses a mix of spaces, hyphens, or underscores without any fancy adjectives or jokes.
    
    Examples of my actual folder names: 'AdventureWorks+Raw+Data', 'ai-agents-for-beginners', 'Deck_templates', 'Equity Research', 'indian-language-app', 'MBA', 'MF Tracker', 'priyanka wedding', "Marketing", "PM", "Trade Finance".
    
    Every single file provided must be assigned to exactly one folder.
    
    Respond ONLY with a valid JSON object where keys are folder names and values are lists of the exact filenames.
    """
    
    # Remember to use the exact model string that worked for you in the previous step
    model = genai.GenerativeModel('gemini-2.5-flash') 
    response = model.generate_content(prompt)
    
    raw_text = response.text
    json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            print("❌ AI returned malformed JSON. Try again.")
            return None
    return None
def generate_dynamic_roast(folder_name, file_names):
    """Generates a snarky README for the newly created semantic folder."""
    prompt = f"""
    You are an exhausted digital file organizer. I just created a folder named '{folder_name}' and put these files inside: {', '.join(file_names)}.
    Write a 3-sentence, passive-aggressive note to leave in a README.txt file. Roast the files and the folder theme. Sign off as 'Your Exhausted Python Script'.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    return model.generate_content(prompt).text

def undo_organization():
    """Reads the history ledger and reverts all moves."""
    if not HISTORY_FILE.exists():
        print("🛑 No history file found. Cannot undo.")
        return

    print("⏪ Initiating undo sequence...")
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    restored_count = 0
    for move in history:
        current_path = Path(move["current_path"])
        original_path = Path(move["original_path"])

        if current_path.exists():
            shutil.move(str(current_path), str(original_path))
            restored_count += 1
            
            # Clean up empty folders and the READMEs we generated
            parent_dir = current_path.parent
            readme_path = parent_dir / "README_PLEASE.txt"
            if readme_path.exists():
                os.remove(readme_path)
            
            try:
                # Will only remove the directory if it is completely empty
                parent_dir.rmdir() 
            except OSError:
                pass 

    # Delete the history file after a successful undo
    os.remove(HISTORY_FILE)
    print(f"✅ Undo complete! Restored {restored_count} files to their original chaotic state.")

def organize_files():
    if not TARGET_DIR.exists() or not any(TARGET_DIR.iterdir()):
        TARGET_DIR.mkdir(exist_ok=True)
        print(f"📁 '{TARGET_DIR}' is empty. Drop some files in it!")
        return

    # 1. READ FILES (Ignoring the script and the history log)
    all_files = [f.name for f in TARGET_DIR.iterdir() if f.is_file() and f.name not in ["organizer.py", ".organizer_history.json"]]
    
    if not all_files:
        print("Folder is empty. Nothing to do.")
        return

    # 2. GET AI PROPOSAL
    proposed_structure = suggest_folder_structure(all_files)
    if not proposed_structure:
        return

    # 3. SHOW PROPOSAL & GET APPROVAL
    print("\n" + "="*40)
    print("📝 PROPOSED FOLDER STRUCTURE:")
    for folder, files in proposed_structure.items():
        print(f"\n📁 {folder}/")
        for file in files:
            print(f"   📄 {file}")
    print("="*40 + "\n")

    approval = input("Do you approve this structure? (y/n): ").strip().lower()
    
    if approval != 'y':
        print("🛑 Operation aborted.")
        return

    # 4. EXECUTE MOVE, ROAST, AND LOG HISTORY
    print("\n🚀 Executing file relocation...")
    move_history = []
    
    for folder_name, files_to_move in proposed_structure.items():
        dest_folder = TARGET_DIR / folder_name
        dest_folder.mkdir(exist_ok=True)
        
        actual_moved_files = []
        
        for file_name in files_to_move:
            source_file = TARGET_DIR / file_name
            if source_file.exists():
                safe_dest = get_safe_path(dest_folder, file_name)
                shutil.move(str(source_file), str(safe_dest))
                actual_moved_files.append(file_name)
                
                # Log the move for the undo feature
                move_history.append({
                    "original_path": str(source_file),
                    "current_path": str(safe_dest)
                })
        
        if actual_moved_files:
            print(f"✍️  Drafting roast for {folder_name}...")
            # roast_text = generate_dynamic_roast(folder_name, actual_moved_files)
            
            with open(dest_folder / "README_PLEASE.txt", "w") as f:
                f.write(f"--- FOLDER AUDIT REPORT: {folder_name} ---\n\n")
                # f.write(roast_text)

    # Save the history ledger
    if move_history:
        # Load existing history if we are doing multiple runs, or start fresh
        existing_history = []
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r") as f:
                existing_history = json.load(f)
        
        existing_history.extend(move_history)
        
        with open(HISTORY_FILE, "w") as f:
            json.dump(existing_history, f, indent=4)

    print("\n✅ Cleanup complete. Check your newly organized folders!")

if __name__ == "__main__":
    # Check if the user passed the --undo flag in the terminal
    if len(sys.argv) > 1 and sys.argv[1] == "--undo":
        undo_organization()
    else:
        organize_files()