import subprocess
import sys

pages = ["index.html", "sorting.html", "searching.html", "tests/test_algorithms.html"]
has_error = False

for page in pages:
    url = f"file:///c:/Users/aryan/Desktop/Sorting and Searching/{page}"
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-logging=stderr",
        "--dump-dom",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    stderr = res.stderr
    
    # Check for JS errors in stderr
    for error_keyword in ["Uncaught TypeError", "Uncaught ReferenceError", "Uncaught SyntaxError", "Uncaught RangeError"]:
        if error_keyword in stderr or error_keyword in res.stdout:
            print(f"[FAIL] Found {error_keyword} in {page}")
            has_error = True
            
    print(f"[PASS] {page} loaded without JavaScript runtime errors.")

if not has_error:
    print("\nALL PAGES LOADED CLEANLY WITH ZERO JS RUNTIME ERRORS!")
    sys.exit(0)
else:
    sys.exit(1)
