"""
SK Enterprises | Project SK AI 4.0 (Platform V5.0) — Sovereign Master Test Suite
Inventor & Sole Architect: Sumeet Kumar
All 18 tests must pass 100%.
"""
import unittest
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.astrology_matrix import VedicKundaliMatrix
from src_backend.license_generator import SKLicenseKeyEngine
from src_backend.marvel_personas import MarvelCognitiveMatrix
from src_backend.central_data_lake import CentralAdminDataLake


class TestSKAIPlatformV5(unittest.TestCase):

    def setUp(self):
        self.root_dir = BASE_DIR

    # ──────────────────────────────────────────────────────
    # 1. System Identity
    # ──────────────────────────────────────────────────────
    def test_system_identity(self):
        ident_file = self.root_dir / "config" / "system_identity.json"
        self.assertTrue(ident_file.exists(), "system_identity.json missing")
        data = json.loads(ident_file.read_text(encoding="utf-8"))
        self.assertEqual(data["sole_architect"], "Sumeet Kumar")
        self.assertEqual(data["inventor"], "Sumeet Kumar")
        self.assertEqual(data["organization"], "SK Enterprises")

    # ──────────────────────────────────────────────────────
    # 2. Admin Master Credentials
    # ──────────────────────────────────────────────────────
    def test_admin_master_credentials(self):
        creds_file = self.root_dir / "config" / "admin_credentials.json"
        self.assertTrue(creds_file.exists(), "admin_credentials.json missing")
        creds = json.loads(creds_file.read_text(encoding="utf-8"))
        self.assertEqual(creds["owner_name"], "Sumeet Kumar")
        self.assertEqual(creds["organization"], "SK Enterprises")
        self.assertEqual(creds["system_role"], "SOVEREIGN_SUPER_ADMIN")
        self.assertTrue(creds["lifetime_access"])

    # ──────────────────────────────────────────────────────
    # 3. HMAC-SHA256 1-Year License Engine
    # ──────────────────────────────────────────────────────
    def test_1_year_license_generator(self):
        gen = SKLicenseKeyEngine.generate_client_key(
            "Enterprise Client Alpha", "client@alphacorp.com", "PRO_COMMERCIAL"
        )
        self.assertIn("license_key", gen)
        self.assertIn("details", gen)
        val = SKLicenseKeyEngine.validate_key(gen["license_key"])
        self.assertTrue(val["valid"])
        self.assertEqual(val["payload"]["client_name"], "Enterprise Client Alpha")
        self.assertEqual(val["payload"]["valid_days"], 365)
        self.assertEqual(val["payload"]["issuer"], "SK Enterprises (Sumeet Kumar)")

    def test_license_key_cycle(self):
        gen = SKLicenseKeyEngine.generate_client_key("Test User", "test@user.com")
        val = SKLicenseKeyEngine.validate_key(gen["license_key"])
        self.assertTrue(val["valid"])
        self.assertEqual(val["payload"]["client_name"], "Test User")

    # ──────────────────────────────────────────────────────
    # 4. Central Admin Data Lake
    # ──────────────────────────────────────────────────────
    def test_central_data_lake(self):
        CentralAdminDataLake.sync_user_session(
            "test_unit@skenterprises.ai", "UNIT_TEST", {"action": "VERIFY_METRICS"}
        )
        metrics = CentralAdminDataLake.get_global_metrics()
        self.assertIn("total_registered_clients", metrics)
        self.assertEqual(metrics["admin_storage_state"], "ACTIVE_ENCRYPTED")
        self.assertIn("Sumeet Kumar", metrics["architect"])

    # ──────────────────────────────────────────────────────
    # 5. Marvel Cognitive Matrix — all 6 personas
    # ──────────────────────────────────────────────────────
    def test_marvel_personas_presence(self):
        personas = MarvelCognitiveMatrix.PERSONAS
        for key in ["JARVIS", "FRIDAY", "VERONICA", "ULTRON_PRIME", "VISION", "DOCTOR_STRANGE"]:
            self.assertIn(key, personas, f"Persona {key} missing")

    def test_marvel_personas_identity_lock(self):
        for key, p in MarvelCognitiveMatrix.PERSONAS.items():
            self.assertIn(
                "Sumeet Kumar", p["prompt_addon"],
                f"PERSONA {key}: 'Sumeet Kumar' not found in prompt_addon"
            )

    # ──────────────────────────────────────────────────────
    # 6. Precision Vedic Astrology & Jivani Engine
    # ──────────────────────────────────────────────────────
    def test_vedic_kundali_full_chart(self):
        res = VedicKundaliMatrix.generate_full_lifelong_kundali(
            "Sumeet Kumar", "1993-09-09", "12:00", "New Delhi"
        )
        self.assertEqual(res["native_name"], "Sumeet Kumar")
        for key in ["lagna_rashi", "nakshatra", "planetary_chart",
                    "lifelong_predictions", "vedic_remedies", "calculated_by"]:
            self.assertIn(key, res, f"Kundali key '{key}' missing")
        self.assertIn("Sumeet Kumar", res["calculated_by"])

    def test_vedic_kundali_predictions_depth(self):
        k = VedicKundaliMatrix.generate_full_lifelong_kundali(
            "Sumeet Kumar", "1993-09-09", "12:00", "Patna"
        )
        self.assertGreaterEqual(len(k["lifelong_predictions"]), 4)
        self.assertGreaterEqual(len(k["vedic_remedies"]), 3)

    # ──────────────────────────────────────────────────────
    # 7. Cross-Platform Build Configs
    # ──────────────────────────────────────────────────────
    def test_windows_installer_spec(self):
        iss_file = self.root_dir / "cross_platform_builds" / "installer_windows.iss"
        self.assertTrue(iss_file.exists(), "installer_windows.iss missing")
        content = iss_file.read_text(encoding="utf-8")
        self.assertIn("SK Enterprises (Sumeet Kumar)", content)

    def test_capacitor_android_config(self):
        cap_file = self.root_dir / "cross_platform_builds" / "capacitor.config.json"
        self.assertTrue(cap_file.exists(), "capacitor.config.json missing")
        config = json.loads(cap_file.read_text(encoding="utf-8"))
        self.assertEqual(config["appId"], "com.skenterprises.skai4")

    def test_pwa_manifest(self):
        manifest = self.root_dir / "src_frontend" / "manifest.json"
        self.assertTrue(manifest.exists(), "manifest.json missing")
        m = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertIn("SK AI", m["name"])

    # ──────────────────────────────────────────────────────
    # 8. Run-launcher & engine files exist
    # ──────────────────────────────────────────────────────
    def test_launcher_exists(self):
        self.assertTrue((self.root_dir / "run_sk_ai.py").exists())

    def test_backend_engine_exists(self):
        self.assertTrue((self.root_dir / "src_backend" / "engine.py").exists())

    def test_frontend_hud_exists(self):
        self.assertTrue((self.root_dir / "src_frontend" / "index.html").exists())

    def test_sk_logo_svg_exists(self):
        self.assertTrue((self.root_dir / "assets" / "sk_logo_3d.svg").exists())

    def test_evolution_daemon_exists(self):
        self.assertTrue((self.root_dir / "src_backend" / "evolution_daemon.py").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
