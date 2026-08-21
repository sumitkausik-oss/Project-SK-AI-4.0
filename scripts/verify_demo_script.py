"""
SK Enterprises | SKAI Demo Script End-to-End Verifier
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI — Powered by SK Enterprises

Runs all commands listed under the 'Try SKAI in 2 minutes' section in README.md.
"""
import os
import sys
import io
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminal
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src_backend.app.database.base import get_db, init_db
from src_backend.app.services.assistant_service import AssistantService
from src_backend.app.services.permission_service import PermissionService
from src_backend.app.services.os_control_service import OSControlService

def test_demo_script():
    print("=" * 80)
    print("SKAI 'Try SKAI in 2 minutes' Demo Script Verification")
    print("=" * 80)
    
    init_db()
    db = next(get_db())
    
    # 1. Open Notepad
    print("\n[Step 1] Command: 'open notepad'")
    res1 = AssistantService.process_command(db, "open notepad")
    print(f" -> Status: {res1['status']} | Action: {res1.get('action')}")
    assert res1['status'] == "COMPLETED", f"Expected COMPLETED, got {res1['status']}"
    assert "notepad" in res1['response'].lower(), "Expected notepad in response"
    print(" [PASS]: Notepad opened successfully.")
    
    # Close notepad to be tidy
    OSControlService.close_app("notepad")
    
    # 2. Take a Screenshot
    print("\n[Step 2] Command: 'take a screenshot'")
    res2 = AssistantService.process_command(db, "take a screenshot")
    print(f" -> Status: {res2['status']} | Action: {res2.get('action')}")
    assert res2['status'] == "COMPLETED"
    assert res2.get("result", {}).get("path"), "Expected screenshot path in result"
    print(f" [PASS]: Screenshot captured at {res2['result']['path']}.")
    
    # 3. Create a File on Desktop
    print("\n[Step 3] Command: 'create a file called test.txt on the desktop'")
    res3 = AssistantService.process_command(db, "create a file called test.txt on the desktop")
    print(f" -> Status: {res3['status']} | Action: {res3.get('action')}")
    assert res3['status'] == "COMPLETED"
    created_path = res3.get("result", {}).get("path")
    assert created_path and Path(created_path).exists(), f"File {created_path} was not created"
    print(f" [PASS]: File created at {created_path}.")
    
    # 4. Remember dark mode preference
    print("\n[Step 4] Command: 'remember that I prefer dark mode'")
    res4 = AssistantService.process_command(db, "remember that I prefer dark mode")
    print(f" -> Status: {res4['status']} | Action: {res4.get('action')}")
    assert res4['status'] == "COMPLETED"
    assert "remembered" in res4['response'].lower() or "stored" in res4['response'].lower()
    print(" [PASS]: Durable fact saved to SQLite memory.")
    
    # 5. Recall memory preferences
    print("\n[Step 5] Command: 'what do you remember about my preferences?'")
    res5 = AssistantService.process_command(db, "what do you remember about my preferences?")
    print(f" -> Status: {res5['status']} | Action: {res5.get('action')}")
    assert res5['status'] == "COMPLETED"
    assert "dark mode" in res5['response'].lower(), "Expected dark mode in recalled facts"
    print(" [PASS]: Durable fact successfully recalled.")
    
    # 6. Local search for files
    print("\n[Step 6] Command: 'search my documents for python'")
    res6 = AssistantService.process_command(db, "search my documents for python")
    print(f" -> Status: {res6['status']} | Action: {res6.get('action')}")
    assert res6['status'] == "COMPLETED"
    assert "results" in res6.get("result", {})
    print(f" [PASS]: Local search returned {len(res6['result']['results'])} ranked matches.")
    
    # 7. Run terminal command
    print("\n[Step 7] Command: 'run command echo \"SKAI Online\"'")
    # Temporarily set terminal confirmation to False to test execution pipeline directly
    PermissionService.set_policy(require_confirmation_for_terminal=False)
    res7 = AssistantService.process_command(db, 'run command echo "SKAI Online"')
    print(f" -> Status: {res7['status']} | Action: {res7.get('action')}")
    assert res7['status'] == "COMPLETED"
    assert "SKAI Online" in str(res7.get("result", {}).get("stdout")), "Expected 'SKAI Online' in terminal stdout"
    print(f" [PASS]: Terminal stdout: {res7['result']['stdout'].strip()}")
    
    # 8. Delete file (Safety Confirmation Gate)
    print("\n[Step 8] Command: 'delete file test.txt' (Testing Safety Gate)")
    PermissionService.set_policy(require_confirmation_for_destructive=True)
    res8 = AssistantService.process_command(db, f"delete file {created_path}")
    print(f" -> Status: {res8['status']} | Action: {res8.get('action')} | Action ID: {res8.get('action_id')}")
    assert res8['status'] == "REQUIRES_CONFIRMATION", f"Expected REQUIRES_CONFIRMATION, got {res8['status']}"
    action_id = res8['action_id']
    
    # Now simulate User Approval via Confirmation Endpoint / Service
    print(f" -> Simulating User Approval for Action ID: {action_id}...")
    res8_confirmed = AssistantService.execute_confirmed_action(db, action_id, approved=True)
    assert res8_confirmed['status'] == "COMPLETED"
    assert not Path(created_path).exists(), f"File {created_path} was not deleted after confirmation"
    print(f" [PASS]: Destructive action safely gated, approved, and executed.")
    
    print("\n" + "=" * 80)
    print("SUCCESS: ALL 8 DEMO SCRIPT COMMANDS VERIFIED AND WORKING 100% CORRECTLY!")
    print("=" * 80)

if __name__ == "__main__":
    test_demo_script()
