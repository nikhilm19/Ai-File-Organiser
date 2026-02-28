Semantic File Organizer 🧹
Bring order to your digital workspace with AI-driven context analysis.

🔴 The Problem
Standard file management relies on generic extensions (like .pdf or .jpg), leading to cluttered "Downloads" folders filled with vaguely named documents such as Final_v3.pdf. This lacks project-specific context and wastes valuable time when searching for critical files.

🟢 The Solution
This AI-powered agent analyzes the actual semantics of your filenames to understand their purpose. It intelligently groups related items into practical, project-based folders—modeled after real-world organizational habits—and provides an automated "audit report" for every new cluster.

✨ Key Features
🧠 Semantic Clustering: Goes beyond file types to group items by project context, such as 'MBA', 'MF Tracker', or 'indian-language-app'.

📝 Witty Audit Reports: Generates a README_PLEASE.txt in every new folder, providing a concise, AI-generated summary and critique of the stored files.

🛡️ Zero Data Loss: Prevents overwriting by automatically appending numerical counters to duplicate filenames during relocation.

⏪ Instant Rollback: Includes a built-in undo feature that utilizes a hidden local ledger to restore every file to its original location.

🚀 Getting Started
1. Prerequisites
Python 3.8+

Google Gemini API Key: Obtain a free key from Google AI Studio.

2. Installation
Install the Google Generative AI SDK:

Bash
pip install -U google-generativeai
3. Configuration
Set your API key as an environment variable to keep your credentials secure:

Mac / Linux:

Bash
export GEMINI="your_actual_api_key_here"
Windows (Command Prompt):

DOS
set GEMINI="your_actual_api_key_here"
🛠️ Usage
Place your unorganized files into a folder named messy_folder in the same directory as the script.

Organize Files:

Bash
python organizer.py
The AI will propose a folder structure based on your naming style and wait for your approval (y/n) before moving files.

Undo Organization:

Bash
python organizer.py --undo
Restores all files to their original state and removes generated folders.

⚙️ Architecture
The Architect: Uses Few-Shot Prompting to map files to specific, practical folder names based on user-provided examples.

The Auditor: Analyzes the final clusters to generate automated, witty feedback for the user.

The Ledger: Tracks every file move in a local .organizer_history.json file for 100% reversible operations.