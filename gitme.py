import subprocess
import sys
import time
import os
from datetime import datetime

# Colors
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"  # Added for warnings/non-critical info
CYAN = "\033[96m"
END = "\033[0m"
WHITE = "\033[97m"

def run_git(description, cmd):
    print(f"{CYAN}→ {description}...{END}", end=" ", flush=True)
    
    # Using capture_output=True to handle both stdout and stderr
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        output = (result.stdout + result.stderr).lower()
        
        # 1. Check for "Nothing to commit" (Common non-error)
        if "nothing to commit" in output or "working tree clean" in output or "no changes added to commit" in output:
            print(f"{BLUE}Skip (Nothing to change){END}")
            return

        # 2. Check for "Up to date" (Common during push)
        if "everything up-to-date" in output:
            print(f"{BLUE}Skip (Already synced){END}")
            return

        # 3. Actual Error Handling
        print(f"\n{RED}❌ ERROR DURING: {description.upper()}{END}")
        print(f"{YELLOW}Command executed: {WHITE}{cmd}{END}")
        
        print(f"\n{RED}--- System Error Message ---{END}")
        # Display stderr if it exists, otherwise fallback to stdout
        error_msg = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
        print(f"{WHITE}{error_msg}{END}")
        print(f"{RED}----------------------------{END}\n")
        
        sys.exit(1)
    
    time.sleep(0.4)
    print(f"{GREEN}Done! ✅{END}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    comment = sys.argv[1] if len(sys.argv) > 1 else ""
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_msg = f"🚀 {dt} {comment}".rstrip()
    header_line = "=" * 35

    print(f"{WHITE}{header_line}")
    print(f"🚀 GITME: {GREEN}{dt}")
    if comment:
        print(f"{YELLOW}📝 {comment}")
    print(f"{WHITE}{header_line}{END}\n")

    # Step 1: Stage
    run_git("Staging changes", "git add .")

    # Step 2: Commit
    run_git("Committing", f'git commit -m "{commit_msg}"')
    
    # Step 3: Push
    # Using the current branch dynamically
    current_branch_cmd = "git rev-parse --abbrev-ref HEAD"
    branch_result = subprocess.run(current_branch_cmd, shell=True, capture_output=True, text=True)
    branch = branch_result.stdout.strip()
    
    run_git(f"Pushing to origin/{branch}", f"git push origin {branch}")

    print(f"\n{GREEN}🎉 All changes are live!{END}\n")

if __name__ == "__main__":
    main()