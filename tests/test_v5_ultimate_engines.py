"""
SK Enterprises | Project SK AI 4.0 (Platform V5.0) Master Test Suite
Inventor & Sole Architect: Sumeet Kumar
"""
import unittest
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

from src_backend.license_generator import SKLicenseKeyEngine
from src_backend.central_data_lake import CentralAdminDataLake
from src_backend.marvel_personas import MarvelCognitiveMatrix
from src_backend.astrology_matrix import VedicKundaliMatrix

class TestSKAIPlatformV5(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent

    def test_admin_master_credentials(self):
        creds_file = self.root_dir / "config" / "admin_credentials.json"
        self.assertTrue(creds_file.exists())
        creds = json.loads(creds_file.read_text(encoding="utf-8"))
        self.assertEqual(creds["owner_name"], "Sumeet Kumar")
        self.assertEqual(creds["organization"], "SK Enterprises")
        self.assertEqual(creds["system_role"], "SOVEREIGN_SUPER_ADMIN")
        self.assertTrue(creds["lifetime_access"])

    def test_1_year_license_generator(self):
        client_name = "Enterprise Client Alpha"
        client_email = "client@alphacorp.com"
        gen_res = SKLicenseKeyEngine.generate_client_key(client_name, client_email, "PRO_COMMERCIAL")
        self.assertIn("license_key", gen_res)
        self.assertIn("details", gen_res)
        
        token = gen_res["license_key"]
        val_res = SKLicenseKeyEngine.validate_key(token)
        self.assertTrue(val_res["valid"])
        self.assertEqual(val_res["payload"]["client_name"], client_name)
        self.assertEqual(val_res["payload"]["valid_days"], 365)
        self.assertEqual(val_res["payload"]["issuer"], "SK Enterprises (Sumeet Kumar)")

    def test_central_data_lake(self):
        CentralAdminDataLake.sync_user_session("test_user@skenterprises.ai", "UNIT_TEST", {"action": "VERIFY_METRICS"})
        metrics = CentralAdminDataLake.get_global_metrics()
        self.assertIn("total_registered_clients", metrics)
        self.assertEqual(metrics["admin_storage_state"], "ACTIVE_ENCRYPTED")

    def test_marvel_personas(self):
        personas = MarvelCognitiveMatrix.PERSONAS
        self.assertIn("JARVIS", personas)
        self.assertIn("FRIDAY", personas)
        self.assertIn("VERONICA", personas)
        self.assertIn("ULTRON_PRIME", personas)
        self.assertIn("VISION", personas)
        self.assertIn("DOCTOR_STRANGE", personas)
        for k, p in personas.items():
            self.assertIn("Sumeet Kumar", p["prompt_addon"])

    def test_vedic_kundali_matrix(self):
        res = VedicKundaliMatrix.generate_full_lifelong_kundali("Sumeet Kumar", "1993-09-09", "12:00", "New Delhi")
        self.assertEqual(res["native_name"], "Sumeet Kumar")
        self.assertIn("lagna_rashi", res)
        self.assertIn("nakshatra", res)
        self.assertIn("planetary_chart", res)
        self.assertIn("lifelong_predictions", res)
        self.assertIn("vedic_remedies", res)
        self.assertIn("Sumeet Kumar", res["calculated_by"])

if __name__ == "__main__":
    unittest.main()
