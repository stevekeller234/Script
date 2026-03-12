#!/usr/bin/env python3
"""
Git Commit History Generator
WARNING: This script generates artificial commit history for educational purposes.
Using fake commit history to misrepresent work violates GitHub's Terms of Service.
Use responsibly and ethically.
"""

import os
import subprocess
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
START_DATE = datetime.now() - timedelta(days=4 * 365)  # 4 years ago
END_DATE = datetime.now()
REPO_PATH = Path.cwd()

# Commit patterns
COMMIT_MESSAGES = [
    "fix: resolve bug in authentication",
    "feat: add user profile page",
    "refactor: improve code structure",
    "docs: update README",
    "chore: update dependencies",
    "test: add unit tests",
    "style: format code",
    "perf: optimize database queries",
    "fix: handle edge case",
    "feat: implement search functionality",
    "refactor: extract common logic",
    "docs: add API documentation",
    "chore: clean up unused files",
    "test: fix failing tests",
    "feat: add dark mode support",
    "fix: correct validation logic",
    "perf: reduce bundle size",
    "feat: add pagination",
    "refactor: simplify component",
    "docs: update installation guide",
]

FILE_NAMES = [
    "src/main.py",
    "src/utils.py",
    "src/config.py",
    "src/models.py",
    "src/api.py",
    "tests/test_main.py",
    "tests/test_utils.py",
    "README.md",
    "requirements.txt",
    "config.json",
    "src/components/Button.js",
    "src/components/Header.js",
    "src/services/auth.js",
    "src/services/api.js",
]


def run_git_command(cmd, check=True):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return None


def init_repo():
    """Initialize git repository if not already initialized."""
    if not (REPO_PATH / ".git").exists():
        print("Initializing git repository...")
        run_git_command("git init")
        run_git_command('git config user.name "Dev-Ameen01"')
        run_git_command('git config user.email "email.mameen@gmail.com"')
    else:
        print("Git repository already initialized.")


def create_random_file_content(filename):
    """Generate random file content."""
    ext = Path(filename).suffix
    if ext == ".py":
        return f"""# {filename}
import os
import sys

def main():
    print("Hello from {filename}")
    return True

if __name__ == "__main__":
    main()
"""
    elif ext == ".js":
        return f"""// {filename}
export const {Path(filename).stem} = () => {{
    console.log("Hello from {filename}");
    return true;
}};
"""
    elif ext == ".md":
        return f"""# {filename}

This is a documentation file.

## Features
- Feature 1
- Feature 2
- Feature 3
"""
    elif ext == ".txt":
        return f"Requirements for {filename}\n\nPackage1==1.0.0\nPackage2==2.0.0\n"
    elif ext == ".json":
        return '{\n  "name": "project",\n  "version": "1.0.0"\n}'
    else:
        return f"Content for {filename}\n" + "x" * random.randint(50, 200)


def make_commit(date, message, num_files=1):
    """Create a commit with random file changes."""
    # Randomly select files to modify
    files_to_modify = random.sample(FILE_NAMES, min(num_files, len(FILE_NAMES)))
    
    for filename in files_to_modify:
        filepath = REPO_PATH / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Randomly decide: create, modify, or delete
        action = random.choice(["create", "modify", "modify"])
        
        if action == "delete" and filepath.exists():
            filepath.unlink()
        else:
            # Create or modify file
            if filepath.exists():
                # Modify existing file
                content = filepath.read_text()
                lines = content.split("\n")
                if lines:
                    insert_pos = random.randint(0, len(lines))
                    lines.insert(insert_pos, f"# Modified at {date.strftime('%Y-%m-%d')}")
                    content = "\n".join(lines)
            else:
                # Create new file
                content = create_random_file_content(filename)
            
            filepath.write_text(content)
    
    # Stage all changes
    run_git_command("git add -A")
    
    # Set commit date and create commit
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date.strftime("%Y-%m-%d %H:%M:%S")
    env["GIT_COMMITTER_DATE"] = date.strftime("%Y-%m-%d %H:%M:%S")
    
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=REPO_PATH,
        env=env,
        capture_output=True,
        check=False
    )


def is_weekend(date):
    """Check if date is a weekend."""
    return date.weekday() >= 5  # Saturday = 5, Sunday = 6


def should_skip_day(date):
    """Determine if we should skip this day (weekends, holidays, random days off)."""
    # Skip weekends (70% chance)
    if is_weekend(date) and random.random() < 0.7:
        return True
    
    # Random days off (5% chance on weekdays)
    if not is_weekend(date) and random.random() < 0.05:
        return True
    
    return False


def generate_commits():
    """Generate commits over the time period."""
    current_date = START_DATE
    commit_count = 0
    
    print(f"Generating commits from {START_DATE.date()} to {END_DATE.date()}...")
    print("This may take a while...\n")
    
    while current_date < END_DATE:
        if should_skip_day(current_date):
            current_date += timedelta(days=1)
            continue
        
        # Determine number of commits for this day (0-5)
        num_commits = random.choices(
            [0, 1, 2, 3, 4, 5],
            weights=[20, 30, 25, 15, 7, 3]  # More likely to have 1-2 commits
        )[0]
        
        for _ in range(num_commits):
            # Random time during work hours (9 AM - 6 PM)
            hour = random.randint(9, 18)
            minute = random.randint(0, 59)
            commit_time = current_date.replace(hour=hour, minute=minute)
            
            # Select commit message
            message = random.choice(COMMIT_MESSAGES)
            
            # Determine commit size (1-5 files)
            num_files = random.choices(
                [1, 2, 3, 4, 5],
                weights=[40, 30, 20, 7, 3]  # More likely to have 1-2 files
            )[0]
            
            make_commit(commit_time, message, num_files)
            commit_count += 1
            
            if commit_count % 100 == 0:
                print(f"Generated {commit_count} commits... (Current date: {current_date.date()})")
        
        # Move to next day
        current_date += timedelta(days=1)
        
        # Add occasional gaps (vacation periods)
        if random.random() < 0.01:  # 1% chance
            gap_days = random.randint(3, 14)  # 3-14 day gap
            current_date += timedelta(days=gap_days)
            print(f"Added gap: skipping {gap_days} days (simulating vacation)")
    
    print(f"\nCompleted! Generated {commit_count} commits total.")


def main():
    """Main function."""
    import sys
    
    print("=" * 60)
    print("Git Commit History Generator")
    print("=" * 60)
    print("\n⚠️  WARNING:")
    print("This script generates artificial commit history.")
    print("Using fake commits to misrepresent work violates GitHub ToS.")
    print("Use responsibly and ethically.\n")
    
    # Skip prompt if --yes flag is provided
    if "--yes" not in sys.argv:
        response = input("Do you want to continue? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            return
    
    init_repo()
    generate_commits()
    
    print("\n" + "=" * 60)
    print("Commits generated successfully!")
    print("=" * 60)
    print("\nTo push to GitHub (if you choose to):")
    print("1. Add remote: git remote add origin <your-repo-url>")
    print("2. Push: git push -u origin main --force")
    print("\n⚠️  Remember: Pushing fake history may violate GitHub ToS.")


if __name__ == "__main__":
    main()
