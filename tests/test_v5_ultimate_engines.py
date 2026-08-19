import unittest
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.astrology_matrix import VedicKundaliMatrix
from src_backend.super_admin import SuperAdminHub
from src_backend.central_data_lake import CentralAdminDataLake

class TestSovereignMaster(unittest.TestCase):
    def test_identity_and_sole_architect(self):
        ident_file = BASE_DIR / "config" / "system_identity.json"
        self.assertTrue(ident_file.exists())
        data = json.loads(ident_file.read_text(encoding="utf-8"))
        self.assertEqual(data["sole_architect"], "Sumeet Kumar")
        self.assertEqual(data["inventor"], "Sumeet Kumar")
        self.assertEqual(data["organization"], "SK Enterprises")

    def test_super_admin_key_cycles(self):
        # 1-Year Key
        gen_usr = SuperAdminHub.generate_license("Test Client", "client@sk.ai", "1_YEAR_USER")
        val_usr = SuperAdminHub.validate_license(gen_usr["license_key"])
        self.assertTrue(val_usr["valid"])
        self.assertEqual(val_usr["payload"]["valid_days"], 365)

        # Lifetime Admin Key
        gen_adm = SuperAdminHub.generate_license("Sumeet Kumar", "sumeet.admin@sk.ai", "ADMIN_LIFETIME")
        val_adm = SuperAdminHub.validate_license(gen_adm["license_key"])
        self.assertTrue(val_adm["valid"])
        self.assertEqual(val_adm["payload"]["valid_days"], 36500)

    def test_client_registration_and_killswitch(self):
        reg = SuperAdminHub.register_client("Demo User", 25, "Patna", "demo@user.com", "9153579979")
        self.assertIn("license", reg)
        
        # Killswitch Test
        SuperAdminHub.toggle_client_status("demo@user.com", False)
        val = SuperAdminHub.validate_license(reg["license"]["license_key"])
        self.assertFalse(val["valid"])
        self.assertIn("Suspended", val["reason"])

if __name__ == "__main__":
    unittest.main()
