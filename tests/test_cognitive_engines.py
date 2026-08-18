import unittest
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src_backend.astrology_matrix import VedicKundaliMatrix
from src_backend.license_generator import SKLicenseKeyEngine
from src_backend.marvel_personas import MarvelCognitiveMatrix

class TestSovereignSKAI4(unittest.TestCase):
    def test_identity_and_sole_architect(self):
        ident_file = BASE_DIR / "config" / "system_identity.json"
        self.assertTrue(ident_file.exists())
        data = json.loads(ident_file.read_text(encoding="utf-8"))
        self.assertEqual(data["sole_architect"], "Sumeet Kumar")
        self.assertEqual(data["inventor"], "Sumeet Kumar")
        self.assertEqual(data["organization"], "SK Enterprises")

    def test_license_key_cycle(self):
        gen = SKLicenseKeyEngine.generate_client_key("Test User", "test@user.com")
        self.assertIn("license_key", gen)
        val = SKLicenseKeyEngine.validate_key(gen["license_key"])
        self.assertTrue(val["valid"])
        self.assertEqual(val["payload"]["client_name"], "Test User")

    def test_astrology_matrix_execution(self):
        k = VedicKundaliMatrix.generate_full_lifelong_kundali("Sumeet Kumar", "1993-09-09", "12:00", "Patna")
        self.assertEqual(k["native_name"], "Sumeet Kumar")
        self.assertTrue(len(k["lifelong_predictions"]) >= 4)
        self.assertTrue(len(k["vedic_remedies"]) >= 3)

    def test_marvel_matrix_personas(self):
        self.assertIn("JARVIS", MarvelCognitiveMatrix.PERSONAS)
        self.assertIn("ULTRON_PRIME", MarvelCognitiveMatrix.PERSONAS)
        self.assertIn("DOCTOR_STRANGE", MarvelCognitiveMatrix.PERSONAS)

if __name__ == "__main__":
    unittest.main()
