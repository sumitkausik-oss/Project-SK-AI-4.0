"""
SK Enterprises | SKAI Master Assistant & Intent Dispatch Engine
Founder & Sole Architect: Sumeet Kumar
Platform: SKAI Cognitive Operating System

Orchestrates voice and text commands into OS execution, memory recall,
permission enforcement, and structured feedback.
"""
import re
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from src_backend.app.core.config import settings
from src_backend.app.services.os_control_service import OSControlService
from src_backend.app.services.permission_service import PermissionService, ActionCategory
from src_backend.app.repositories.memory_repo import ChatRepository, MemoryRepository, AuditRepository
from src_backend.anti_extraction_security import AntiExtractionShield

class AssistantService:
    """Master reasoning, intent parsing, and execution pipeline for SKAI."""

    @classmethod
    def execute_confirmed_action(cls, db: Session, action_id: str, approved: bool) -> Dict[str, Any]:
        """Executes or rejects a previously queued high-impact action upon user review."""
        action = PermissionService.pop_pending_action(action_id)
        if not action:
            return {
                "success": False,
                "error": f"Pending action ID '{action_id}' not found or already processed."
            }

        action_type = action["action_type"]
        params = action["params"]

        if not approved:
            AuditRepository.log_event(
                db=db,
                event_type=f"REJECTED_{action_type}",
                description=f"User explicitly rejected high-impact action '{action_type}' with params {params}",
                severity="WARNING",
                actor="USER"
            )
            return {
                "success": True,
                "status": "REJECTED",
                "action": action_type,
                "message": f"Action '{action_type}' was successfully cancelled by the user."
            }

        # Execute approved action
        result = cls._dispatch_os_tool(action_type, params)
        AuditRepository.log_event(
            db=db,
            event_type=f"CONFIRMED_{action_type}",
            description=f"User approved and executed '{action_type}'. Outcome: {result.get('success')}",
            severity="INFO" if result.get("success") else "ERROR",
            actor="USER_APPROVED"
        )
        return {
            "success": result.get("success", False),
            "status": "COMPLETED",
            "action": action_type,
            "result": result
        }

    @classmethod
    def _dispatch_os_tool(cls, action_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Directly invokes the underlying OS Control tool."""
        if action_type == "OPEN_APP":
            return OSControlService.open_app(params.get("app", ""))
        elif action_type == "CLOSE_APP":
            return OSControlService.close_app(params.get("target", ""))
        elif action_type == "LIST_RUNNING_APPS":
            return OSControlService.list_running_apps()
        elif action_type == "CREATE_FILE":
            return OSControlService.create_file(params.get("file_path", ""), params.get("content", ""))
        elif action_type == "CREATE_FOLDER":
            return OSControlService.create_folder(params.get("folder_path", ""))
        elif action_type == "READ_FILE":
            return OSControlService.read_file(params.get("file_path", ""))
        elif action_type == "WRITE_FILE":
            return OSControlService.write_file(params.get("file_path", ""), params.get("content", ""), params.get("append", False))
        elif action_type == "DELETE_FILE":
            return OSControlService.delete_file(params.get("target_path", ""))
        elif action_type == "LIST_FOLDER":
            return OSControlService.list_folder(params.get("folder_path", "Desktop"))
        elif action_type == "TERMINAL_COMMAND":
            return OSControlService.run_terminal_command(params.get("command", ""), params.get("cwd"))
        elif action_type == "SEARCH_LOCAL_FILES":
            return OSControlService.search_local_files(params.get("query", ""), params.get("base_dir"))
        elif action_type == "TAKE_SCREENSHOT":
            return OSControlService.take_screenshot(params.get("filename"))
        elif action_type == "CODE_ASSIST_PROJECT_MAP":
            return OSControlService.code_assist_read_project(params.get("project_path", ""))
        elif action_type == "CODE_ASSIST_EDIT":
            return OSControlService.code_assist_edit_file(params.get("file_path", ""), params.get("target_content", ""), params.get("replacement_content", ""))
        else:
            return {"success": False, "error": f"Unknown action type '{action_type}'"}

    @classmethod
    def process_command(
        cls,
        db: Session,
        query: str,
        persona: str = "SKAI",
        language: str = "en-US",
        user_email: str = "sumeet.admin@skenterprises.ai"
    ) -> Dict[str, Any]:
        """
        Main natural language processing pipeline.
        Parses intent, verifies permissions, executes actions, records memory & audit trails.
        """
        # 1. Anti-Extraction Prompt Sanitization
        sanitized = AntiExtractionShield.sanitize_ai_prompt_query(query)
        if "[SECURITY LOCK ACTIVATED]" in sanitized:
            return {
                "status": "SECURITY_LOCKED",
                "thought_process": "1. Anti-Extraction Shield trapped malicious probe.\n2. Enforcing zero-extraction protocol.",
                "response": sanitized,
                "voice_text": "Security lock activated. Sovereign core protected.",
                "action": "SECURITY_LOCK",
                "inventor": settings.INVENTOR,
                "organization": settings.ORGANIZATION
            }

        q = query.strip()
        q_lower = q.lower()

        # 2. Contextual Memory Recall
        memories = MemoryRepository.recall_associative(db, q, limit=3)
        memory_context = [f"[{m.key}]: {m.content}" for m in memories] if memories else []

        action_type = None
        params = {}
        description = ""

        # ---------------------------------------------------------------------
        # 3. INTENT PARSING RULES (English & Hindi)
        # ---------------------------------------------------------------------

        # A. Screenshot
        if any(k in q_lower for k in ["take screenshot", "take a screenshot", "capture screen", "screenshot lo", "screenshot le lo", "screen capture"]):
            action_type = "TAKE_SCREENSHOT"
            params = {}
            description = "Capture display screenshot"

        # B. Application Open
        elif q_lower.startswith(("open ", "launch ", "start ")) and not any(k in q_lower for k in ["file", "folder", "terminal", "command"]):
            app_name = re.sub(r'^(open|launch|start)\s+', '', q, flags=re.IGNORECASE).strip()
            action_type = "OPEN_APP"
            params = {"app": app_name}
            description = f"Launch application '{app_name}'"
        elif "kholo" in q_lower or "open karo" in q_lower:
            app_name = re.sub(r'\s+(kholo|open karo|chalao).*$', '', q, flags=re.IGNORECASE).strip()
            action_type = "OPEN_APP"
            params = {"app": app_name}
            description = f"Launch application '{app_name}'"

        # C. Application Close
        elif q_lower.startswith(("close ", "kill ", "quit ", "terminate ")) and not any(k in q_lower for k in ["file", "folder"]):
            app_name = re.sub(r'^(close|kill|quit|terminate)\s+', '', q, flags=re.IGNORECASE).strip()
            action_type = "CLOSE_APP"
            params = {"target": app_name}
            description = f"Terminate application '{app_name}'"
        elif "band karo" in q_lower or "close karo" in q_lower:
            app_name = re.sub(r'\s+(band karo|close karo|rok do).*$', '', q, flags=re.IGNORECASE).strip()
            action_type = "CLOSE_APP"
            params = {"target": app_name}
            description = f"Terminate application '{app_name}'"

        # D. List Running Apps
        elif any(k in q_lower for k in ["list apps", "running apps", "what apps are open", "list processes", "open applications"]):
            action_type = "LIST_RUNNING_APPS"
            params = {}
            description = "List active running applications"

        # E. File Creation
        elif any(k in q_lower for k in ["create file", "create a file", "make file", "file banao", "new file"]):
            # Extract filename (e.g. "create a file called test.txt on the desktop with content hello")
            match = re.search(r'(?:called|named)\s+([a-zA-Z0-9_\-\.]+(?:\.[a-zA-Z0-9]+)?)', q, re.IGNORECASE)
            if not match:
                match = re.search(r'(?:file)\s+([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)', q, re.IGNORECASE)
            if not match:
                match = re.search(r'(?:create file|make file|create a file)\s+([a-zA-Z0-9_\-\.]+)', q, re.IGNORECASE)
            fname = match.group(1) if match else "test.txt"
            
            # Destination directory
            dest = "Desktop"
            if "documents" in q_lower:
                dest = "Documents"
            elif "downloads" in q_lower:
                dest = "Downloads"
            
            # Content
            content = ""
            content_match = re.search(r'(?:with content|saying|containing)\s+["\']?([^"\']+)["\']?', q, re.IGNORECASE)
            if content_match:
                content = content_match.group(1)

            file_path = f"{dest}/{fname}"
            action_type = "CREATE_FILE"
            params = {"file_path": file_path, "content": content}
            description = f"Create file '{file_path}'"

        # F. Folder Creation
        elif any(k in q_lower for k in ["create folder", "create a folder", "make folder", "folder banao", "directory banao"]):
            match = re.search(r'(?:called|named)\s+([a-zA-Z0-9_\-\.]+)', q, re.IGNORECASE)
            if not match:
                match = re.search(r'(?:folder|directory)\s+([a-zA-Z0-9_\-\.]+)', q, re.IGNORECASE)
            folder_name = match.group(1) if match else "New_Folder"
            dest = "Desktop"
            if "documents" in q_lower:
                dest = "Documents"
            folder_path = f"{dest}/{folder_name}"
            action_type = "CREATE_FOLDER"
            params = {"folder_path": folder_path}
            description = f"Create folder '{folder_path}'"

        # G. Read File
        elif any(k in q_lower for k in ["read file", "view file", "show file", "cat ", "file padho", "content of"]):
            match = re.search(r'(?:read file|view file|show file|cat|content of)\s+["\']?([^"\']+)["\']?', q, re.IGNORECASE)
            file_path = match.group(1).strip() if match else "test.txt"
            action_type = "READ_FILE"
            params = {"file_path": file_path}
            description = f"Read contents of file '{file_path}'"

        # H. Delete File / Folder
        elif any(k in q_lower for k in ["delete file", "remove file", "delete folder", "file delete karo", "erase file"]):
            match = re.search(r'(?:delete file|remove file|delete folder|erase file)\s+["\']?([^"\']+)["\']?', q, re.IGNORECASE)
            target = match.group(1).strip() if match else "test.txt"
            action_type = "DELETE_FILE"
            params = {"target_path": target}
            description = f"Permanently delete '{target}'"

        # I. Terminal Execution
        elif any(k in q_lower for k in ["run command", "run terminal", "execute command", "shell command", "powershell ", "terminal me run karo"]):
            cmd = re.sub(r'^(run command|run terminal|execute command|shell command|terminal me run karo)\s+', '', q, flags=re.IGNORECASE).strip()
            action_type = "TERMINAL_COMMAND"
            params = {"command": cmd}
            description = f"Execute terminal command: `{cmd}`"

        # J. Local Search
        elif any(k in q_lower for k in ["search my documents", "search documents", "search my computer", "search files for", "find file", "search for", "search "]):
            term = re.sub(r'^(search my documents for|search documents for|search my computer for|search files for|search my documents|search documents|find file|search for|search)\s+', '', q, flags=re.IGNORECASE).strip()
            action_type = "SEARCH_LOCAL_FILES"
            params = {"query": term}
            description = f"Intelligent local file search for: '{term}'"

        # K. Remember Context / Memory
        elif any(k in q_lower for k in ["remember that", "remember my", "yaad rakho ki", "store fact"]):
            fact = re.sub(r'^(remember that|remember my|yaad rakho ki|store fact)\s+', '', q, flags=re.IGNORECASE).strip()
            # Generate key from fact summary
            key = " ".join(fact.split()[:4]).capitalize()
            MemoryRepository.store_memory(db=db, key=key, content=fact, tags=["preference", "user_context"], category="PREFERENCE")
            
            thought = f"1. Identified durable user fact: '{fact}'\n2. Stored to persistent SQLite memory under key: '{key}'."
            response = f"✅ **Memory Stored:** I have securely recorded this to local memory:\n\n> *\"{fact}\"*"
            voice_text = "I have remembered that for future sessions."
            
            AuditRepository.log_event(db, "STORE_MEMORY", f"Stored memory: {key}", "INFO", "SKAI")
            return {
                "status": "COMPLETED",
                "action": "STORE_MEMORY",
                "thought_process": thought,
                "response": response,
                "voice_text": voice_text,
                "result": {"key": key, "content": fact},
                "inventor": settings.INVENTOR,
                "organization": settings.ORGANIZATION
            }

        # L. What do you remember / Memory query
        elif any(k in q_lower for k in ["what do you remember", "show memories", "kya yaad hai", "my preferences", "recall memory"]):
            all_mems = MemoryRepository.list_all(db, limit=20)
            if all_mems:
                mem_list = "\n".join([f"• **{m.key}**: {m.content}" for m in all_mems])
                response = f"🧠 **SKAI Durable Local Memory ({len(all_mems)} entries):**\n\n{mem_list}"
                voice_text = f"I currently remember {len(all_mems)} durable facts in your local memory store."
            else:
                response = "🧠 **SKAI Local Memory:** No durable facts stored yet. You can say *'remember that [fact]'* anytime!"
                voice_text = "I do not have any saved memories yet."

            return {
                "status": "COMPLETED",
                "action": "GET_MEMORY",
                "thought_process": "1. Retrieved all durable facts from SQLite memory repository.",
                "response": response,
                "voice_text": voice_text,
                "result": {"count": len(all_mems)},
                "inventor": settings.INVENTOR,
                "organization": settings.ORGANIZATION
            }

        # ---------------------------------------------------------------------
        # 4. EXECUTION & PERMISSION GATEWAY
        # ---------------------------------------------------------------------
        if action_type:
            # Evaluate against safety policies
            evaluation = PermissionService.evaluate_request(action_type, params, description)
            
            # If explicit confirmation required:
            if evaluation.get("requires_confirmation"):
                action_id = evaluation["action_id"]
                AuditRepository.log_event(
                    db=db,
                    event_type=f"CONFIRMATION_REQUESTED_{action_type}",
                    description=f"Action '{action_type}' triggered safety gate (Action ID: {action_id})",
                    severity="WARNING",
                    actor="SKAI_SAFETY_GATE"
                )
                
                thought = (
                    f"1. Parsed high-impact action: {action_type}\n"
                    f"2. Target: {params}\n"
                    f"3. Triggered Safety Confirmation Gate (Action ID: {action_id}).\n"
                    f"4. Awaiting user approval."
                )
                response = (
                    f"🛡️ **Safety Confirmation Required**\n\n"
                    f"SKAI requires your explicit authorization to execute this high-impact action:\n"
                    f"• **Action:** `{action_type}`\n"
                    f"• **Details:** {description}\n"
                    f"• **Action ID:** `{action_id}`\n\n"
                    f"*Please click **Approve** or **Reject** in the prompt to continue.*"
                )
                voice_text = "Confirmation required for this high impact action."

                return {
                    "status": "REQUIRES_CONFIRMATION",
                    "action": action_type,
                    "action_id": action_id,
                    "category": evaluation.get("category"),
                    "params": params,
                    "description": description,
                    "thought_process": thought,
                    "response": response,
                    "voice_text": voice_text,
                    "requires_confirmation": True,
                    "inventor": settings.INVENTOR,
                    "organization": settings.ORGANIZATION
                }

            # If auto-approved or read-only:
            result = cls._dispatch_os_tool(action_type, params)
            success = result.get("success", False)

            AuditRepository.log_event(
                db=db,
                event_type=f"EXEC_{action_type}",
                description=f"Executed '{action_type}'. Success: {success}",
                severity="INFO" if success else "ERROR",
                actor="SKAI_AUTO"
            )

            # Format human-friendly response based on tool outcome
            thought = (
                f"1. Parsed intent: {action_type} ({description})\n"
                f"2. Trust Category: {evaluation.get('category')} (Auto-Approved)\n"
                f"3. Executed via OSControlService -> Result: {'Success' if success else 'Failed'}"
            )

            if success:
                if action_type == "OPEN_APP":
                    response = f"🚀 **Application Launched:** Successfully opened **{params.get('app')}** on your system."
                    voice_text = f"Opened {params.get('app')}."
                elif action_type == "CLOSE_APP":
                    response = f"⏹️ **Application Closed:** {result.get('message')}"
                    voice_text = f"Closed {params.get('target')}."
                elif action_type == "TAKE_SCREENSHOT":
                    response = (
                        f"📸 **Screenshot Captured:**\n\n"
                        f"• **File:** `{result.get('filename')}`\n"
                        f"• **Saved to:** `{result.get('path')}`\n"
                        f"• **Resolution:** {result.get('width')}x{result.get('height')}"
                    )
                    voice_text = "Screenshot captured successfully."
                elif action_type == "CREATE_FILE":
                    response = f"📄 **File Created:** Successfully created `{result.get('filename')}` at `{result.get('path')}`."
                    voice_text = f"Created file {result.get('filename')}."
                elif action_type == "READ_FILE":
                    snippet = result.get("content", "")
                    response = f"📖 **File Contents (`{result.get('filename')}`):**\n\n```text\n{snippet}\n```"
                    voice_text = f"Read {result.get('filename')}."
                elif action_type == "DELETE_FILE":
                    response = f"🗑️ **Deleted:** {result.get('message')}"
                    voice_text = "Target deleted successfully."
                elif action_type == "TERMINAL_COMMAND":
                    stdout = result.get('stdout', '') or '(no output)'
                    stderr = result.get('stderr', '')
                    err_sec = f"\n**Errors:**\n```text\n{stderr}\n```" if stderr else ""
                    response = f"💻 **Terminal Output (Exit Code: {result.get('exit_code')}):**\n\n```text\n{stdout}\n```{err_sec}"
                    voice_text = "Command executed."
                elif action_type == "SEARCH_LOCAL_FILES":
                    count = result.get("count", 0)
                    if count > 0:
                        lines = []
                        for r in result.get("results", [])[:5]:
                            snip = f" — *\"{r['snippet']}\"*" if r.get('snippet') else ""
                            lines.append(f"• **{r['filename']}** ({r['match_type']}) `{r['path']}`{snip}")
                        response = f"🔍 **Found {count} matching file(s) for '{params.get('query')}':**\n\n" + "\n".join(lines)
                        voice_text = f"Found {count} matches on your computer."
                    else:
                        response = f"🔍 **Local Search:** No files found matching '{params.get('query')}'. Try another keyword or folder."
                        voice_text = "No matching files found."
                elif action_type == "LIST_RUNNING_APPS":
                    apps = result.get("apps", [])[:8]
                    app_lines = "\n".join([f"• **{a['name']}** (PID: {a['pid']}, RAM: {a['memory_mb']} MB)" for a in apps])
                    response = f"📊 **Active Applications ({result.get('total_active')} total):**\n\n{app_lines}"
                    voice_text = f"There are {result.get('total_active')} running processes."
                else:
                    response = f"✅ **Executed {action_type}:** {result.get('message', 'Success')}"
                    voice_text = "Action completed."
            else:
                response = f"❌ **Execution Error:** {result.get('error', 'Unknown error occurred.')}"
                voice_text = "An error occurred while executing the command."

            # Save chat log
            try:
                conv = ChatRepository.get_or_create_conversation(db, "default_session", user_email, persona)
                ChatRepository.add_message(db, conv.id, "AI", response, query, thought, voice_text, persona)
            except Exception:
                pass

            return {
                "status": "COMPLETED" if success else "FAILED",
                "action": action_type,
                "result": result,
                "thought_process": thought,
                "response": response,
                "voice_text": voice_text,
                "inventor": settings.INVENTOR,
                "organization": settings.ORGANIZATION
            }

        # ---------------------------------------------------------------------
        # 5. CONVERSATIONAL & GENERAL INTELLIGENCE (Bilingual Butler)
        # ---------------------------------------------------------------------
        if any(k in q_lower for k in ["sumit", "sumeet", "creator", "owner", "architect", "founder", "banaya", "who made you", "kaun hai", "who are you"]):
            thought = (
                f"1. Validated Immutable Creator & Architect: {settings.INVENTOR} ({settings.ORGANIZATION}).\n"
                f"2. Recalled memory context: {memory_context[:2]}\n"
                f"3. Formulating bilingual acknowledgment."
            )
            response = (
                f"प्रणाम सुमीत सर! मैं **SKAI (Powered by {settings.ORGANIZATION})** हूँ — आपका स्थानीय डेस्कटॉप AI सहायक।\n\n"
                f"मेरा निर्माण, वास्तुकला एवं स्वामित्व केवल और केवल **Inventor & Sole Architect: {settings.INVENTOR}** द्वारा **{settings.ORGANIZATION}** के अंतर्गत किया गया है। "
                f"मैं आपके कंप्यूटर के ऐप्स, फ़ाइलें, टर्मिनल, सर्च और मेमोरी को पूरी सुरक्षा के साथ नियंत्रित कर सकता हूँ।"
            )
            voice_text = "Pranam Sumeet Sir. Main SKAI hoon, powered by SK Enterprises. Main aapke computer ko niyantrit karne ke liye taiyaar hoon."
        else:
            thought = (
                f"1. General assistant reasoning for: '{q}'\n"
                f"2. Context memories: {memory_context}\n"
                f"3. All local OS modules active and operational."
            )
            response = (
                f"प्रणाम सुमीत सर! SKAI आपके निर्देश पर कार्य करने के लिए तैयार है: **'{q}'**।\n\n"
                f"आप मुझसे कंप्यूटर पर ऐप्स खोलने, फ़ाइलें बनाने/पढ़ने/हटाने, स्क्रीनशॉट लेने, टर्मिनल कमांड चलाने या लोकल फ़ाइलें सर्च करने के लिए कह सकते हैं।"
            )
            voice_text = "Main aapka aadesh process karne ke liye taiyaar hoon Sir."

        try:
            conv = ChatRepository.get_or_create_conversation(db, "default_session", user_email, persona)
            ChatRepository.add_message(db, conv.id, "AI", response, query, thought, voice_text, persona)
        except Exception:
            pass

        return {
            "status": "COMPLETED",
            "action": "CONVERSATION",
            "thought_process": thought,
            "response": response,
            "voice_text": voice_text,
            "persona": persona,
            "inventor": settings.INVENTOR,
            "organization": settings.ORGANIZATION
        }
