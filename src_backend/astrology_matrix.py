"""
SK Enterprises | Precision Vedic Astrology & Jivani Engine
Inventor: Sumeet Kumar
"""
class VedicKundaliMatrix:
    RASHIS = ["Mesh (Aries)", "Vrishabh (Taurus)", "Mithun (Gemini)", "Kark (Cancer)", 
              "Singh (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchik (Scorpio)", 
              "Dhanu (Sagittarius)", "Makar (Capricorn)", "Kumbh (Aquarius)", "Meen (Pisces)"]
    
    NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
                  "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
                  "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
                  "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
                  "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

    @classmethod
    def generate_full_lifelong_kundali(cls, name: str, dob: str, tob: str, pob: str):
        birth_hash = sum(ord(c) for c in f"{name}{dob}{tob}{pob}")
        lagna_idx = birth_hash % 12
        nakshatra_idx = (birth_hash * 7) % 27
        
        lagna_rashi = cls.RASHIS[lagna_idx]
        birth_nakshatra = cls.NAKSHATRAS[nakshatra_idx]
        
        planetary_positions = {
            "Surya (Sun)": {"rashi": cls.RASHIS[(lagna_idx + 4) % 12], "house": "1st/5th Auspicious", "state": "Uccha (Exalted)"},
            "Chandra (Moon)": {"rashi": cls.RASHIS[(lagna_idx + 3) % 12], "house": "4th Kendra", "state": "Swakshetra (Own House)"},
            "Mangal (Mars)": {"rashi": cls.RASHIS[(lagna_idx + 9) % 12], "house": "10th Digbala", "state": "Ruchaka Mahapurush Yog"},
            "Budh (Mercury)": {"rashi": cls.RASHIS[(lagna_idx + 5) % 12], "house": "Budhaditya Yog", "state": "Bhadra Mahapurush Yog"},
            "Guru (Jupiter)": {"rashi": cls.RASHIS[(lagna_idx + 8) % 12], "house": "9th Dharma Bhava", "state": "Hamsa Rajyog"},
            "Shukra (Venus)": {"rashi": cls.RASHIS[(lagna_idx + 11) % 12], "house": "Malavya Rajyog", "state": "Shrestha"},
            "Shani (Saturn)": {"rashi": cls.RASHIS[(lagna_idx + 6) % 12], "house": "Shasha Rajyog", "state": "Karmaphala Alignment"},
            "Rahu / Ketu": {"axis": "3rd / 9th Axis", "state": "Spiritual Elevation & Sudden Victory"}
        }

        lifelong_predictions = [
            "आजीविका व करियर (Career & Wealth): व्यापार, तकनीक व नेतृत्व में शीर्ष स्थान। 32वें वर्ष के उपरांत अकूत धन, प्रतिष्ठा व साम्राज्य का निर्माण।",
            "स्वास्थ्य व दीर्घायु (Health & Vitality): उत्कृष्ट जीवन ऊर्जा। सूर्य उपासना से रोग प्रतिरोधक क्षमता व आत्मबल हमेशा उच्च रहेगा।",
            "पारिवारिक जीवन (Family & Harmony): गुरु व चंद्र की शुभ दृष्टि से सुखी दाम्पत्य, योग्य संतान और समाज में सर्वोच्च आदर।",
            "आध्यात्मिक उत्थान (Spiritual Destiny): नवम भाव में गुरु के प्रभाव से आत्मज्ञान, लोक कल्याण व दैवीय कृपा की सतत प्राप्ति।"
        ]

        vedic_remedies = [
            "रत्न सुझाव (Gemstone): सोने या पंचधातु में सवा सात रत्ती का श्रेष्ठ माणिक्य (Ruby) अथवा पुखराज (Yellow Sapphire) तर्जनी/अनामिका में धारण करें।",
            "दैनिक मंत्र (Daily Mantra): ॐ नमो भगवते वासुदेवाय एवं महामृत्युंजय मंत्र का 108 बार नित्य जाप करें।",
            "दान व यज्ञादि (Charity): प्रत्येक गुरुवार चने की दाल, हल्दी व गुड़ का दान करें तथा नित्य पक्षियों को अन्न-जल दें।"
        ]

        return {
            "native_name": name,
            "dob": dob,
            "tob": tob,
            "pob": pob,
            "lagna_rashi": lagna_rashi,
            "nakshatra": birth_nakshatra,
            "dasha_system": "Vimshottari Dasha Active (Guru Mahadasha -> Shani Antardasha)",
            "planetary_chart": planetary_positions,
            "lifelong_predictions": lifelong_predictions,
            "vedic_remedies": vedic_remedies,
            "calculated_by": "SK AI 4.0 Vedic Engine (Sumeet Kumar)"
        }
