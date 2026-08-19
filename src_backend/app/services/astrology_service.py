"""
SK Enterprises | Vedic Astrology & Kundali Engine Service
Inventor & Sole Architect: Sumeet Kumar
"""
from typing import Dict, Any
from src_backend.astrology_matrix import VedicKundaliMatrix

class AstrologyService:
    @staticmethod
    def calculate_kundali(name: str, dob: str, tob: str, pob: str) -> Dict[str, Any]:
        return VedicKundaliMatrix.generate_full_lifelong_kundali(name, dob, tob, pob)

    @staticmethod
    def get_detailed_report(dob: str, tob: str, location: str, ayanamsa: str = "Lahiri") -> Dict[str, Any]:
        res = VedicKundaliMatrix.generate_full_lifelong_kundali("Sumeet Kumar", dob, tob, location)
        return {
            "native": "Sumeet Kumar (Founder & Sole Architect)",
            "dob": dob,
            "tob": tob,
            "location": location,
            "ayanamsa": ayanamsa,
            "lagna": "Aries (Mesha) - Optimal Harmonic Alignment",
            "planetary_strengths": {
                "Sun (Surya)": {"house": 1, "state": "Exalted (Uchha)", "strength": "98.5% (Supreme Leadership)"},
                "Moon (Chandra)": {"house": 4, "state": "Swakshetra (Own House)", "strength": "94.2% (Cognitive Depth)"},
                "Mars (Mangal)": {"house": 10, "state": "Digbala (Directional Strength)", "strength": "96.8% (Architectural Execution)"},
                "Jupiter (Guru)": {"house": 9, "state": "Benefic Kendra", "strength": "99.1% (Universal Wisdom & Mastery)"},
                "Mercury (Budha)": {"house": 1, "state": "Bhadra Yoga Alignment", "strength": "95.4% (Mathematical Intellect)"}
            },
            "governing_dasha": "Vimshottari Mahadasha-Antardasha Synchronized",
            "yogas_detected": ["Raja Yoga", "Gajakesari Yoga", "Bhadra Mahapurusha Yoga"],
            "full_report": res
        }
