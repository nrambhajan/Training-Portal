"""
Day 3.5 — Archive, Find & Grep Practice
Run once on server: python3 seed_day3_5.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

module = models.Module(
    title="Day 3.5 - Archive, Find & Grep Practice",
    description="Hands-on tasks covering tar/gzip archives, find command, locate, grep, and file searching techniques.",
    sort_order=4,
    unlock_percent=0,
    is_published=False,
    time_limit=60,
)
db.add(module)
db.commit()
db.refresh(module)

questions = [
    {
        "type": "practical",
        "text": "TASK 1 - Create a Gzip-Compressed Tarball\n\nCreate a gzip-compressed tarball of the /home directory and save it as /tmp/home_backup.tar.gz",
        "verify_command": "test -f /tmp/home_backup.tar.gz && file /tmp/home_backup.tar.gz | grep -q 'gzip' && echo 'archive_ok'",
        "verify_expected": "archive_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 1,
        "hint": "Use: tar -czf /tmp/home_backup.tar.gz /home",
    },
    {
        "type": "practical",
        "text": "TASK 2 - List Archive Contents Without Extracting\n\nList the contents of /tmp/home_backup.tar.gz WITHOUT extracting it.\n\nSave the listing output to /home/trainee/archive_contents.txt",
        "verify_command": "test -s /home/trainee/archive_contents.txt && grep -q 'home' /home/trainee/archive_contents.txt && echo 'listed'",
        "verify_expected": "listed",
        "verify_type": "contains",
        "points": 2.0,
        "order": 2,
        "hint": "Use: tar -tzf /tmp/home_backup.tar.gz > /home/trainee/archive_contents.txt",
    },
    {
        "type": "practical",
        "text": "TASK 3 - Extract Archive to a Different Directory\n\nExtract the contents of /tmp/home_backup.tar.gz into the directory /tmp/extracted/\n\nCreate /tmp/extracted/ first if it doesn't exist. After extraction, files from /home should be inside /tmp/extracted/",
        "verify_command": "test -d /tmp/extracted && ls /tmp/extracted/home/ 2>/dev/null && echo 'extracted_ok'",
        "verify_expected": "extracted_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
        "hint": "Use: mkdir -p /tmp/extracted && tar -xzf /tmp/home_backup.tar.gz -C /tmp/extracted/",
    },
    {
        "type": "practical",
        "text": "TASK 4 - Create File with Space in Name & Use locate\n\nDo the following:\n1. Create a folder: /home/trainee/myTasks/\n2. Inside it, create a file called 'hello World.txt' (with a space in the name)\n3. Write some content in the file (anything you want)\n4. Run 'sudo updatedb' to update the file database\n5. Use the 'locate' command to find the file and save the output to /home/trainee/locate_output.txt",
        "verify_command": "test -f '/home/trainee/myTasks/hello World.txt' && test -s '/home/trainee/myTasks/hello World.txt' && test -s /home/trainee/locate_output.txt && grep -q 'hello World.txt' /home/trainee/locate_output.txt && echo 'all_done'",
        "verify_expected": "all_done",
        "verify_type": "contains",
        "points": 3.0,
        "order": 4,
        "hint": "Use quotes for filenames with spaces: touch '/home/trainee/myTasks/hello World.txt'. Install mlocate if needed: sudo apt install mlocate -y",
    },
    {
        "type": "practical",
        "text": "TASK 5 - Find Files Irrespective of Case\n\nUse the find command to search /home/trainee/ for all files with the name 'hello' (irrespective of upper/lower case).\n\nSave the output to /home/trainee/find_iname.txt",
        "verify_command": "test -s /home/trainee/find_iname.txt && grep -qi 'hello' /home/trainee/find_iname.txt && echo 'found'",
        "verify_expected": "found",
        "verify_type": "contains",
        "points": 2.0,
        "order": 5,
        "hint": "Use: find /home/trainee/ -iname '*hello*' > /home/trainee/find_iname.txt (the -iname flag is case-insensitive)",
    },
    {
        "type": "practical",
        "text": "TASK 6 - Find Files by Permission\n\nUse the find command to get all files with permission 644 under /root/\n\nSave the output to /home/trainee/find_perm.txt\n\nNote: Use 2>/dev/null to suppress 'permission denied' errors.",
        "verify_command": "test -f /home/trainee/find_perm.txt && head -1 /home/trainee/find_perm.txt | grep -q '/' && echo 'perm_found'",
        "verify_expected": "perm_found",
        "verify_type": "contains",
        "points": 2.0,
        "order": 6,
        "hint": "Use: find /root/ -type f -perm 644 2>/dev/null > /home/trainee/find_perm.txt",
    },
    {
        "type": "practical",
        "text": "TASK 7 - Create a Multi-Line File\n\nCreate a file at /home/trainee/sample.txt with EXACTLY these contents (3 lines, with an empty line in between):\n\nLine 1: this line is the 1st lower case line in this file.\nLine 2: (empty line)\nLine 3: Two lines above this line is empty.\nLine 4: And this is the last line.",
        "verify_command": "grep -q '1st lower case' /home/trainee/sample.txt && grep -q 'Two lines above' /home/trainee/sample.txt && grep -q 'last line' /home/trainee/sample.txt && echo 'file_correct'",
        "verify_expected": "file_correct",
        "verify_type": "contains",
        "points": 2.0,
        "order": 7,
        "hint": "Use nano or cat with heredoc. Make sure to include the blank line between line 1 and 'Two lines above'.",
    },
    {
        "type": "practical",
        "text": "TASK 8 - Grep with Line Numbers\n\nUsing the file /home/trainee/sample.txt from the previous task:\n\nGrep the word 'is' and show line numbers in the output.\n\nSave the output to /home/trainee/grep_is.txt",
        "verify_command": "test -s /home/trainee/grep_is.txt && grep -q ':' /home/trainee/grep_is.txt && grep -q 'is' /home/trainee/grep_is.txt && echo 'grep_ok'",
        "verify_expected": "grep_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 8,
        "hint": "Use: grep -n 'is' /home/trainee/sample.txt > /home/trainee/grep_is.txt (the -n flag shows line numbers)",
    },
    {
        "type": "practical",
        "text": "TASK 9 - Case-Insensitive Grep\n\nUsing the file /home/trainee/sample.txt:\n\nGrep the word 'this' irrespective of case (should match 'this', 'This', 'THIS' etc.)\n\nSave the output to /home/trainee/grep_this.txt",
        "verify_command": "test -s /home/trainee/grep_this.txt && grep -qi 'this' /home/trainee/grep_this.txt && echo 'grep_case_ok'",
        "verify_expected": "grep_case_ok",
        "verify_type": "contains",
        "points": 2.0,
        "order": 9,
        "hint": "Use: grep -i 'this' /home/trainee/sample.txt > /home/trainee/grep_this.txt (the -i flag is case-insensitive)",
    },
    {
        "type": "mcq",
        "text": "What would the command 'find /dev -type c -perm 660' do?",
        "options": [
            "Find all regular files in /dev with permission 660",
            "Find all character device files in /dev with permission 660",
            "Find all directories in /dev with permission 660",
            "Find all block device files in /dev with permission 660"
        ],
        "correct_answer": "1",
        "points": 2.0,
        "order": 10,
        "hint": "The -type c means character device files. The -perm 660 means exact permission match.",
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print("  - 9 Practical tasks")
print("  - 1 MCQ")
print("Module is DRAFT - publish from admin panel when ready")
db.close()
