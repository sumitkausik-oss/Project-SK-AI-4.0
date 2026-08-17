import unittest
import json
import base64
import hashlib
from pathlib import Path

from core.education_matrix import UniversalEducationMatrix
from core.data_analyst_engine import DataAnalystSuite
from core.cloud_admin_engine import CloudAdminActuator
from core.astrology_engine import VedicAstrologyCore
from core.commercial_auth_rbac import CommercialAccessGate

class TestProjectSKAI4Engines(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent

    def test_education_matrix(self):
        edu = UniversalEducationMatrix()
        self.assertIn("K-12 NCERT (Class 1-12)", edu.curriculum)
        
        test_obj = edu.generate_comprehensive_test("Physics", "Class 12", "Hard")
        self.assertEqual(test_obj["difficulty"], "Hard")
        self.assertEqual(test_obj["total_marks"], 120)
        self.assertEqual(len(test_obj["modules"]), 3)

        blueprint = edu.generate_lecture_blueprint("Quantum Mechanics & Schrödinger Wave Equations")
        self.assertIn("derivation_chain", blueprint)
        self.assertEqual(len(blueprint["derivation_chain"]), 4)

    def test_data_analyst_suite(self):
        suite = DataAnalystSuite()
        clean_res = suite.clean_and_normalize("enterprise_q3_financials.csv")
        self.assertEqual(clean_res["status"], "Production-Ready Cleaned DataFrame")
        self.assertGreaterEqual(len(clean_res["operations"]), 4)

        bi_res = suite.generate_bi_visuals(["revenue", "churn_rate", "clv"])
        self.assertEqual(len(bi_res["charts"]), 3)
        self.assertIn("Cyberpunk Glassmorphic", bi_res["bi_format"])

        sql_res = suite.synthesize_sql_query("Summarize monthly active revenue", dialect="BigQuery")
        self.assertIn("SELECT", sql_res["sql"])

    def test_cloud_admin_engine(self):
        actuator = CloudAdminActuator()
        gw_res = actuator.execute_google_workspace_task("SUSPEND_USER", "inactive_contractor@skenterprises.org")
        self.assertEqual(gw_res["execution"], "SUCCESS")

        m365_res = actuator.execute_microsoft_admin_task("ENFORCE_MFA_CONDITIONAL_ACCESS")
        self.assertEqual(m365_res["execution"], "ENFORCED")

        prov_res = actuator.provision_enterprise_user("Sumeet Kumar", "sumeet@skenterprises.org", "OWNER_ADMIN")
        self.assertEqual(prov_res["status"], "PROVISIONED")

    def test_astrology_engine(self):
        astro = VedicAstrologyCore()
        kundali = astro.calculate_natal_matrix("1998-05-15", "10:30", "New Delhi, India")
        self.assertIn("planetary_strengths", kundali)
        self.assertIn("Sun (Surya)", kundali["planetary_strengths"])
        self.assertIn("governing_period", kundali)

    def test_commercial_rbac(self):
        gate = CommercialAccessGate()
        self.assertTrue(gate.check_module_access("ADMIN_LIFETIME", "EDUCATION"))
        self.assertTrue(gate.check_module_access("ADMIN_LIFETIME", "DATA_ANALYST"))
        self.assertTrue(gate.check_module_access("ADMIN_LIFETIME", "ASTROLOGY"))
        self.assertTrue(gate.check_module_access("DATA_ANALYST_EDITION", "DATA_ANALYST"))
        self.assertFalse(gate.check_module_access("DATA_ANALYST_EDITION", "ASTROLOGY"))

        auth_res = gate.verify_google_token("VALID_GOOGLE_OAUTH_TOKEN_TEST_12345")
        self.assertTrue(auth_res["authenticated"])

    def test_cryptographic_license(self):
        lic_file = self.root_dir / "config" / "license.key"
        self.assertTrue(lic_file.exists())
        token = lic_file.read_text(encoding="utf-8")
        data = json.loads(base64.b64decode(token.encode()).decode())
        payload = data["payload"]
        sig = data["signature"]

        raw_str = json.dumps(payload, sort_keys=True)
        expected_sig = hashlib.sha256((raw_str + "SK_ENTERPRISES_SUMEET_KUMAR_2026_MASTER_SECRET").encode()).hexdigest()
        self.assertEqual(sig, expected_sig)
        self.assertEqual(payload["owner"], "Sumeet Kumar")
        self.assertEqual(payload["organization"], "SK Enterprises")

    def test_system_identity(self):
        ident_file = self.root_dir / "config" / "system_identity.json"
        self.assertTrue(ident_file.exists())
        ident = json.loads(ident_file.read_text(encoding="utf-8"))
        self.assertEqual(ident["inventor"], "Sumeet Kumar")
        self.assertEqual(ident["organization"], "SK Enterprises")
        self.assertEqual(ident["sole_architect"], "Sumeet Kumar")

if __name__ == "__main__":
    unittest.main()
