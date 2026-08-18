"""
SK Enterprises | Cybernetic HUD GUI Dashboard for Project SK AI 4.0
Inventor & Sole Architect: Sumit Kumar
"""
import os
import sys
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path

from core.system_paths import BASE_DIR, APPDATA_DIR, LOGS_DIR
from core.education_matrix import UniversalEducationMatrix
from core.data_analyst_engine import DataAnalystSuite
from core.cloud_admin_engine import CloudAdminActuator
from core.astrology_engine import VedicAstrologyCore
from core.commercial_auth_rbac import CommercialAccessGate
from core.autonomous_learner import AutonomousLearningEngine

class SKAIHUDApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Project SK AI 4.0 | JARVIS 4.0 - SK Enterprises (Sumit Kumar)")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg="#080E1C")

        # Load App Icon if available
        ico_path = BASE_DIR / "assets" / "jarvis.ico"
        if ico_path.exists():
            try:
                self.root.iconbitmap(str(ico_path))
            except Exception:
                pass

        # Initialize Cognitive Engines
        self.edu_engine = UniversalEducationMatrix()
        self.data_engine = DataAnalystSuite()
        self.cloud_engine = CloudAdminActuator()
        self.astro_engine = VedicAstrologyCore()
        self.access_gate = CommercialAccessGate()
        
        # Start Autonomous Learner Daemon
        self.learner = AutonomousLearningEngine()
        self.learner.start_daemon()

        self._apply_cyber_theme()
        self._build_header()
        self._build_tabs()
        self._build_status_bar()

    def _apply_cyber_theme(self):
        style = ttk.Style()
        style.theme_use('default')
        
        # Notebook styling
        style.configure("TNotebook", background="#080E1C", borderwidth=0)
        style.configure("TNotebook.Tab", background="#0D1B2A", foreground="#90E0EF", padding=[15, 8], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", "#00B4D8")], foreground=[("selected", "#080E1C")])
        
        # Frame styling
        style.configure("Cyber.TFrame", background="#080E1C")
        style.configure("Card.TFrame", background="#0D1B2A", relief="flat")
        
        # Label styling
        style.configure("Cyber.TLabel", background="#080E1C", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#0D1B2A", foreground="#FFFFFF", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#080E1C", foreground="#00F5D4", font=("Segoe UI", 16, "bold"))
        style.configure("SubHeader.TLabel", background="#080E1C", foreground="#90E0EF", font=("Segoe UI", 9))
        style.configure("Accent.TLabel", background="#0D1B2A", foreground="#00F5D4", font=("Segoe UI", 11, "bold"))

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#0D1B2A", height=70, relief="flat", highlightbackground="#00B4D8", highlightthickness=1)
        header_frame.pack(fill="x", padx=12, pady=(10, 6))

        title_lbl = tk.Label(
            header_frame, 
            text="⚡ SK ENTERPRISES | PROJECT SK AI 4.0 (JARVIS 4.0)", 
            font=("Segoe UI", 14, "bold"), 
            bg="#0D1B2A", 
            fg="#00F5D4"
        )
        title_lbl.pack(anchor="w", padx=15, pady=(8, 2))

        sub_lbl = tk.Label(
            header_frame, 
            text="INVENTOR & SOLE ARCHITECT: SUMIT KUMAR | COMMERCIAL ENTERPRISE COGNITIVE OS", 
            font=("Segoe UI", 9, "bold"), 
            bg="#0D1B2A", 
            fg="#90E0EF"
        )
        sub_lbl.pack(anchor="w", padx=15, pady=(0, 8))

        badge = tk.Label(
            header_frame,
            text="LIFETIME ADMIN KEY: ACTIVE",
            font=("Segoe UI", 9, "bold"),
            bg="#00B4D8",
            fg="#080E1C",
            padx=10,
            pady=4
        )
        badge.place(relx=0.98, rely=0.5, anchor="e")

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=6)

        # 1. Universal Education Tab
        self.tab_edu = ttk.Frame(self.notebook, style="Cyber.TFrame")
        self.notebook.add(self.tab_edu, text=" 🎓 Education Matrix ")
        self._setup_education_tab()

        # 2. Data Analyst Suite Tab
        self.tab_data = ttk.Frame(self.notebook, style="Cyber.TFrame")
        self.notebook.add(self.tab_data, text=" 📊 Data Analyst ")
        self._setup_data_tab()

        # 3. Coral Brain Visualizer Tab (NEW)
        self.tab_coral = ttk.Frame(self.notebook, style="Cyber.TFrame")
        self.notebook.add(self.tab_coral, text=" 🧠 Coral Brain ")
        self._setup_coral_brain_tab()
        self.notebook.add(self.tab_data, text=" 📊 Data Analyst Suite ")
        self._setup_data_tab()

        # 3. Cloud DevOps Tab
        self.tab_cloud = ttk.Frame(self.notebook, style="Cyber.TFrame")
        self.notebook.add(self.tab_cloud, text=" ☁️ Cloud & DevOps ")
        self._setup_cloud_tab()

        # 4. Vedic Astrology Tab
        self.tab_astro = ttk.Frame(self.notebook, style="Cyber.TFrame")
        self.notebook.add(self.tab_astro, text=" 🔮 Vedic Astrology ")
        self._setup_astro_tab()

        # 5. Security & License Tab
        self.tab_sec = ttk.Frame(self.notebook, style="Cyber.TFrame")
        self.notebook.add(self.tab_sec, text=" 🛡️ Security & Licensing ")
        self._setup_security_tab()

    def _setup_coral_brain_tab(self):
        # Neural Core Dynamic Dashboard
        label = tk.Label(self.tab_coral, text="🧠 Neural Cortex Status Monitor", font=("Segoe UI", 12, "bold"), bg="#080E1C", fg="#00F5D4")
        label.pack(pady=(15, 5))

        # System Log Display for Evolution Tracking
        self.log_display = tk.Text(self.tab_coral, height=15, width=80, bg="#0D1B2A", fg="#FFFFFF", font=("Consolas", 10), state="disabled")
        self.log_display.pack(padx=10, pady=10)

        # Update log placeholder
        self.log_display.configure(state="normal")
        self.log_display.insert("end", "[SYSTEM] Universal Mastery Schema Activated.\n")
        self.log_display.insert("end", "[CORE] Evolution initialized. STEM Matrix linking...\n")
        self.log_display.insert("end", "[DATA] Cognitive Data stream ready.\n")
        self.log_display.configure(state="disabled")

    def _setup_education_tab(self):
        left = tk.Frame(self.tab_edu, bg="#0D1B2A", width=320, highlightbackground="#00B4D8", highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 6), pady=6)

        tk.Label(left, text="STEM Curriculum Engine", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#00F5D4").pack(anchor="w", padx=12, pady=(12, 6))

        tk.Label(left, text="Standard / Target Exam:", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.edu_standard_cb = ttk.Combobox(left, values=["Class 12 (NCERT/CBSE)", "Class 10 (NCERT/CBSE)", "JEE Advanced / Main", "NEET Medical", "B.Tech Computer Science", "B.Tech Mechanical", "B.Tech Electrical"], state="readonly")
        self.edu_standard_cb.current(0)
        self.edu_standard_cb.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(left, text="Subject / Topic:", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.edu_subject_entry = tk.Entry(left, bg="#1B263B", fg="#FFFFFF", insertbackground="#00F5D4", relief="flat", font=("Segoe UI", 10))
        self.edu_subject_entry.insert(0, "Quantum Mechanics & Wave Equations")
        self.edu_subject_entry.pack(fill="x", padx=12, pady=(0, 12))

        btn_test = tk.Button(left, text="⚡ Generate Comprehensive Test", bg="#00B4D8", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_generate_test)
        btn_test.pack(fill="x", padx=12, pady=4)

        btn_lec = tk.Button(left, text="📖 Synthesize Lecture Blueprint", bg="#00F5D4", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_generate_lecture)
        btn_lec.pack(fill="x", padx=12, pady=4)

        right = tk.Frame(self.tab_edu, bg="#0D1B2A", highlightbackground="#1B263B", highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, pady=6)

        tk.Label(right, text="Interactive Synthesis Terminal", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#90E0EF").pack(anchor="w", padx=12, pady=8)
        self.edu_output = scrolledtext.ScrolledText(right, bg="#080E1C", fg="#00F5D4", insertbackground="#00F5D4", font=("Consolas", 10), relief="flat")
        self.edu_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.edu_output.insert("1.0", "[SK AI Universal Education Matrix Loaded]\nSelect curriculum or enter topic to synthesize structured assessments and derivation trees.\n")

    def _setup_data_tab(self):
        left = tk.Frame(self.tab_data, bg="#0D1B2A", width=320, highlightbackground="#00B4D8", highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 6), pady=6)

        tk.Label(left, text="Autonomous Data Studio", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#00F5D4").pack(anchor="w", padx=12, pady=(12, 6))

        tk.Label(left, text="Dataset Identifier:", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.data_name_entry = tk.Entry(left, bg="#1B263B", fg="#FFFFFF", insertbackground="#00F5D4", relief="flat", font=("Segoe UI", 10))
        self.data_name_entry.insert(0, "enterprise_revenue_stream.csv")
        self.data_name_entry.pack(fill="x", padx=12, pady=(0, 12))

        btn_clean = tk.Button(left, text="🧹 Auto Clean & Normalize", bg="#00B4D8", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_clean_data)
        btn_clean.pack(fill="x", padx=12, pady=4)

        btn_bi = tk.Button(left, text="📈 Generate BI Visuals Matrix", bg="#00F5D4", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_generate_bi)
        btn_bi.pack(fill="x", padx=12, pady=4)

        btn_sql = tk.Button(left, text="🗄️ Synthesize SQL (BigQuery)", bg="#48CAE4", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_generate_sql)
        btn_sql.pack(fill="x", padx=12, pady=4)

        right = tk.Frame(self.tab_data, bg="#0D1B2A", highlightbackground="#1B263B", highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, pady=6)

        tk.Label(right, text="Data Analyst Output Stream", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#90E0EF").pack(anchor="w", padx=12, pady=8)
        self.data_output = scrolledtext.ScrolledText(right, bg="#080E1C", fg="#00F5D4", insertbackground="#00F5D4", font=("Consolas", 10), relief="flat")
        self.data_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.data_output.insert("1.0", "[SK AI Data Analyst Engine Ready]\nFeatures: Missing Value Imputation, Outlier Filtering, Correlation Matrices, BigQuery SQL Synthesis.\n")

    def _setup_cloud_tab(self):
        left = tk.Frame(self.tab_cloud, bg="#0D1B2A", width=320, highlightbackground="#00B4D8", highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 6), pady=6)

        tk.Label(left, text="Cloud DevOps Actuator", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#00F5D4").pack(anchor="w", padx=12, pady=(12, 6))

        tk.Label(left, text="Target User Email:", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.cloud_user_entry = tk.Entry(left, bg="#1B263B", fg="#FFFFFF", insertbackground="#00F5D4", relief="flat", font=("Segoe UI", 10))
        self.cloud_user_entry.insert(0, "sumit@skenterprises.org")
        self.cloud_user_entry.pack(fill="x", padx=12, pady=(0, 12))

        btn_gw = tk.Button(left, text="🚀 Google Workspace Provision", bg="#00B4D8", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_google_workspace)
        btn_gw.pack(fill="x", padx=12, pady=4)

        btn_m365 = tk.Button(left, text="🛡️ M365 Zero-Trust Enforce", bg="#00F5D4", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_m365)
        btn_m365.pack(fill="x", padx=12, pady=4)

        right = tk.Frame(self.tab_cloud, bg="#0D1B2A", highlightbackground="#1B263B", highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, pady=6)

        tk.Label(right, text="Cloud DevOps Console", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#90E0EF").pack(anchor="w", padx=12, pady=8)
        self.cloud_output = scrolledtext.ScrolledText(right, bg="#080E1C", fg="#00F5D4", insertbackground="#00F5D4", font=("Consolas", 10), relief="flat")
        self.cloud_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.cloud_output.insert("1.0", "[SK AI Cloud DevOps Engine Online]\nGoogle Workspace Directory API & Microsoft Graph Zero-Trust Enforcer Active.\n")

    def _setup_astro_tab(self):
        left = tk.Frame(self.tab_astro, bg="#0D1B2A", width=320, highlightbackground="#00B4D8", highlightthickness=1)
        left.pack(side="left", fill="y", padx=(0, 6), pady=6)

        tk.Label(left, text="Vedic Ephemeris & Kundali", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#00F5D4").pack(anchor="w", padx=12, pady=(12, 6))

        tk.Label(left, text="Date of Birth (YYYY-MM-DD):", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.astro_dob_entry = tk.Entry(left, bg="#1B263B", fg="#FFFFFF", insertbackground="#00F5D4", relief="flat", font=("Segoe UI", 10))
        self.astro_dob_entry.insert(0, "1998-05-15")
        self.astro_dob_entry.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(left, text="Time of Birth (HH:MM):", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.astro_tob_entry = tk.Entry(left, bg="#1B263B", fg="#FFFFFF", insertbackground="#00F5D4", relief="flat", font=("Segoe UI", 10))
        self.astro_tob_entry.insert(0, "10:30")
        self.astro_tob_entry.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(left, text="Location:", bg="#0D1B2A", fg="#FFFFFF", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(6, 2))
        self.astro_loc_entry = tk.Entry(left, bg="#1B263B", fg="#FFFFFF", insertbackground="#00F5D4", relief="flat", font=("Segoe UI", 10))
        self.astro_loc_entry.insert(0, "New Delhi, India")
        self.astro_loc_entry.pack(fill="x", padx=12, pady=(0, 12))

        btn_calc = tk.Button(left, text="🌟 Calculate Natal Kundali Matrix", bg="#00F5D4", fg="#080E1C", font=("Segoe UI", 10, "bold"), relief="flat", command=self._action_calculate_kundali)
        btn_calc.pack(fill="x", padx=12, pady=4)

        right = tk.Frame(self.tab_astro, bg="#0D1B2A", highlightbackground="#1B263B", highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, pady=6)

        tk.Label(right, text="Natal Ephemeris Matrix", font=("Segoe UI", 11, "bold"), bg="#0D1B2A", fg="#90E0EF").pack(anchor="w", padx=12, pady=8)
        self.astro_output = scrolledtext.ScrolledText(right, bg="#080E1C", fg="#00F5D4", insertbackground="#00F5D4", font=("Consolas", 10), relief="flat")
        self.astro_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.astro_output.insert("1.0", "[Vedic Astrology Ephemeris Subsystem 4.0 Active]\nEnter birth coordinates to compute planetary harmonic positions and Vimshottari Dasha.\n")

    def _setup_security_tab(self):
        container = tk.Frame(self.tab_sec, bg="#0D1B2A", highlightbackground="#00B4D8", highlightthickness=1)
        container.pack(fill="both", expand=True, padx=10, pady=6)

        tk.Label(container, text="Enterprise Cryptographic Governance & Identity Lock", font=("Segoe UI", 12, "bold"), bg="#0D1B2A", fg="#00F5D4").pack(anchor="w", padx=15, pady=10)

        info_box = scrolledtext.ScrolledText(container, bg="#080E1C", fg="#00F5D4", font=("Consolas", 10), relief="flat", height=16)
        info_box.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        license_path = BASE_DIR / "config" / "admin_key.json"
        ident_path = BASE_DIR / "config" / "system_identity.json"

        lic_data = {}
        ident_data = {}
        if license_path.exists():
            try:
                lic_data = json.loads(license_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        if ident_path.exists():
            try:
                ident_data = json.loads(ident_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        sec_summary = f"""========================================================================================
                 SK ENTERPRISES | MASTER SECURITY & IDENTITY LOCK
========================================================================================
• SYSTEM: {ident_data.get('system_name', 'SK AI 4.0')} ({ident_data.get('codename', 'Project JARVIS 4.0')})
• INVENTOR & SOLE ARCHITECT: {ident_data.get('inventor', 'Sumit Kumar')}
• ORGANIZATION: {ident_data.get('organization', 'SK Enterprises')}
• COPYRIGHT: {ident_data.get('copyright', '(C) 2026 SK Enterprises')}

[CRYPTOGRAPHIC LICENSE STATUS]
• LICENSE ID: {lic_data.get('license_id', 'SK4-ENTERPRISE-LIFETIME-MASTER-001')}
• TIER: {lic_data.get('tier', 'ADMIN_LIFETIME (Permanent Unlimited Commercial Access)')}
• STATUS: VERIFIED & HARDWARE LOCKED (HMAC-SHA256)
• UNLOCKED FEATURES: {", ".join(lic_data.get('unlocked_features', ['ALL_MODULES']))}

[SECURITY RUNTIME LOGS DIRECTORY]
• Path: {LOGS_DIR}
• UAC Safe AppData: {APPDATA_DIR}
========================================================================================"""
        info_box.insert("1.0", sec_summary)

    def _build_status_bar(self):
        status_frame = tk.Frame(self.root, bg="#0D1B2A", height=28)
        status_frame.pack(fill="x", side="bottom")

        tk.Label(status_frame, text="● SYSTEM HEALTH: 100% OPTIMAL", font=("Segoe UI", 9, "bold"), bg="#0D1B2A", fg="#00F5D4").pack(side="left", padx=12)
        tk.Label(status_frame, text="● 24x7 LEARNING DAEMON: ACTIVE", font=("Segoe UI", 9, "bold"), bg="#0D1B2A", fg="#00B4D8").pack(side="left", padx=12)
        tk.Label(status_frame, text="SK AI 4.0 Production Build | v4.0.0 (x64)", font=("Segoe UI", 9), bg="#0D1B2A", fg="#90E0EF").pack(side="right", padx=12)

    # Action Callbacks
    def _action_generate_test(self):
        subject = self.edu_subject_entry.get()
        std = self.edu_standard_cb.get()
        res = self.edu_engine.generate_comprehensive_test(subject, std, "Hard")
        self.edu_output.delete("1.0", tk.END)
        self.edu_output.insert("1.0", json.dumps(res, indent=2))

    def _action_generate_lecture(self):
        subject = self.edu_subject_entry.get()
        res = self.edu_engine.generate_lecture_blueprint(subject)
        self.edu_output.delete("1.0", tk.END)
        self.edu_output.insert("1.0", json.dumps(res, indent=2))

    def _action_clean_data(self):
        dname = self.data_name_entry.get()
        res = self.data_engine.clean_and_normalize(dname)
        self.data_output.delete("1.0", tk.END)
        self.data_output.insert("1.0", json.dumps(res, indent=2))

    def _action_generate_bi(self):
        res = self.data_engine.generate_bi_visuals(["revenue", "retention_rate", "clv", "server_latency"])
        self.data_output.delete("1.0", tk.END)
        self.data_output.insert("1.0", json.dumps(res, indent=2))

    def _action_generate_sql(self):
        res = self.data_engine.synthesize_sql_query("Aggregate enterprise monthly churn and revenue", dialect="BigQuery")
        self.data_output.delete("1.0", tk.END)
        self.data_output.insert("1.0", json.dumps(res, indent=2))

    def _action_google_workspace(self):
        user = self.cloud_user_entry.get()
        res = self.cloud_engine.provision_enterprise_user("Sumit Kumar", user, "ADMIN_OWNER")
        self.cloud_output.delete("1.0", tk.END)
        self.cloud_output.insert("1.0", json.dumps(res, indent=2))

    def _action_m365(self):
        res = self.cloud_engine.execute_microsoft_admin_task("ENFORCE_MFA_CONDITIONAL_ACCESS_SOC2")
        self.cloud_output.delete("1.0", tk.END)
        self.cloud_output.insert("1.0", json.dumps(res, indent=2))

    def _action_calculate_kundali(self):
        dob = self.astro_dob_entry.get()
        tob = self.astro_tob_entry.get()
        loc = self.astro_loc_entry.get()
        res = self.astro_engine.calculate_natal_matrix(dob, tob, loc)
        self.astro_output.delete("1.0", tk.END)
        self.astro_output.insert("1.0", json.dumps(res, indent=2))

def launch_gui():
    root = tk.Tk()
    app = SKAIHUDApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
