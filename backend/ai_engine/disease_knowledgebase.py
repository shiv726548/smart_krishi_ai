"""
Smart Krishi AI - Comprehensive Plant Disease & Crop Health Knowledgebase
Supports: Tomato, Potato, Rice, Wheat, Cotton, Corn
Languages: English (en), Hindi (hi), Marathi (mr)
"""

DISEASE_KNOWLEDGEBASE = {
    "Tomato": {
        "Early Blight": {
            "health_status": "Diseased",
            "confidence_default": 0.92,
            "cause": "Fungal infection by Alternaria solani",
            "symptoms": {
                "en": "Concentric rings on lower leaves, yellowing margins, target-board spot patterns.",
                "hi": "निचली पत्तियों पर गोल छल्ले, किनारों का पीला पड़ना और काले धब्बे।",
                "mr": "खालील पानांवर गोल चकतीसारखे काळे डाग आणि पाने पिवळी पडणे."
            },
            "actions": {
                "en": ["Remove and burn infected leaves.", "Avoid overhead irrigation.", "Ensure proper plant spacing for airflow."],
                "hi": ["संक्रमित पत्तियों को काटकर जला दें।", "ऊपर से पानी देने से बचें।", "हवा के प्रवाह के लिए पौधों के बीच दूरी रखें।"],
                "mr": ["बाधित पाने काढून नष्ट करा.", "पानांवर थेट पाणी मारणे टाळा.", "हवा खेळती राहण्यासाठी योग्य अंतर ठेवा."]
            },
            "chemical_treatment": "Fungicide spray: Mancozeb (75% WP) at 2g/liter or Copper Oxychloride at 3g/liter.",
            "organic_treatment": "Neem oil spray (5ml/liter) mixed with cow urine solution or Trichoderma viride."
        },
        "Late Blight": {
            "health_status": "Diseased",
            "confidence_default": 0.94,
            "cause": "Phytophthora infestans fungus-like pathogen",
            "symptoms": {
                "en": "Water-soaked dark lesions on leaf tips, white fuzzy mold on underside during high humidity.",
                "hi": "पत्तियों की नोक पर काले पानी जैसे धब्बे और नीचे सफेद फफूंद।",
                "mr": "पानांच्या टोकावर काळे ओले डाग आणि खालच्या बाजूला पांढरी बुरशी."
            },
            "actions": {
                "en": ["Destroy severely infected plants.", "Apply preventative copper spray before rain.", "Reduce field moisture."],
                "hi": ["गंभीर रूप से प्रभावित पौधों को नष्ट करें।", "बारिश से पहले कॉपर स्प्रे करें।"],
                "mr": ["ज्यास्त बाधित झाडे उपटून नष्ट करा.", "कॉपर फवारणी करा."]
            },
            "chemical_treatment": "Cymoxanil + Mancozeb (Curzate) 2g/L or Metalaxyl 8% + Mancozeb 64% (Ridomil MZ) at 2.5g/L.",
            "organic_treatment": "Bordeaux mixture (1%) or Garlic extract spray."
        },
        "Leaf Curl Virus": {
            "health_status": "Diseased",
            "confidence_default": 0.89,
            "cause": "Begomovirus transmitted by Whiteflies (Bemisia tabaci)",
            "symptoms": {
                "en": "Upward curling and twisting of leaves, stunted plant growth, pale green/yellow puckering.",
                "hi": "पत्तियों का ऊपर की ओर मुड़ना, विकास रुकना और पीलापन।",
                "mr": "पाने वरच्या बाजूला गोळा होणे (चुरडा-मुरडा) आणि वाढ खुंटणे."
            },
            "actions": {
                "en": ["Control whitefly vectors using yellow sticky traps.", "Uproot viral infected plants."],
                "hi": ["पीले चिपचिपे ट्रैप लगाएं।", "संक्रमित पौधों को उखाड़ फेंकें।"],
                "mr": ["पिवळे चिकट सापळे लावा.", "बाधित झाडे मुळासकट उपटा."]
            },
            "chemical_treatment": "Imidacloprid 17.8 SL at 0.5ml/L or Acetamiprid 20 SP at 0.2g/L for vector control.",
            "organic_treatment": "Spray Neem seed kernel extract (NSKE 5%) twice a week."
        },
        "Nitrogen Deficiency": {
            "health_status": "Nutrient Deficient",
            "confidence_default": 0.91,
            "cause": "Low soil Nitrogen availability",
            "symptoms": {
                "en": "Uniform yellowing of older lower leaves, thin weak stems, slow growth.",
                "hi": "पुरानी निचली पत्तियों का पीला पड़ना, तना पतला और कमजोर होना।",
                "mr": "जुनी पाने पिवळी पडणे आणि खोड बारीक होणे."
            },
            "actions": {
                "en": ["Apply nitrogen rich fertilizer.", "Improve soil organic matter with vermicompost."],
                "hi": ["यूरिया या नाइट्रोजन युक्त उर्वरक डालें।", "वर्मीकंपोस्ट का प्रयोग करें।"],
                "mr": ["युरिया किंवा नत्रयुक्त खत द्या.", "गांडूळ खत वापरा."]
            },
            "chemical_treatment": "Foliar spray of 1% Urea solution or NPK 19:19:19 (5g/L).",
            "organic_treatment": "Apply well-rotted farmyard manure (FYM) or Jeevamrut."
        },
        "Healthy": {
            "health_status": "Healthy",
            "confidence_default": 0.98,
            "cause": "Optimal growth conditions",
            "symptoms": {
                "en": "Vibrant green leaves, strong erect stem, no visible spots or pests.",
                "hi": "हरी स्वस्थ पत्तियां, मजबूत तना, कोई बीमारी नहीं।",
                "mr": "ताजी हिरवी पाने, दणकट खोड, कोणतीही कीड नाही."
            },
            "actions": {
                "en": ["Maintain current irrigation and fertilizing schedule.", "Inspect weekly for pests."],
                "hi": ["वर्तमान सिंचाई और खाद प्रबंधन जारी रखें।", "साप्ताहिक निरीक्षण करें।"],
                "mr": ["सध्याचे पाणी आणि खत व्यवस्थापन चालू ठेवा."]
            },
            "chemical_treatment": "None required.",
            "organic_treatment": "Apply organic mulch to retain soil moisture."
        }
    },

    "Potato": {
        "Early Blight": {
            "health_status": "Diseased",
            "confidence_default": 0.93,
            "cause": "Alternaria solani fungal spores",
            "symptoms": {
                "en": "Dark brown dark spots with target rings on potato foliage.",
                "hi": "आलू की पत्तियों पर भूरे छल्लेदार धब्बे।",
                "mr": "बटाट्याच्या पानांवर तांबूस काळे गोल डाग."
            },
            "actions": {
                "en": ["Destroy crop residue post harvest.", "Apply recommended fungicide."],
                "hi": ["फसल अवशेष नष्ट करें।", "फफूंदनाशक का छिड़काव करें।"],
                "mr": ["पीक काढणीनंतर उर्वरित भाग नष्ट करा."]
            },
            "chemical_treatment": "Mancozeb 75 WP at 2.5g/L.",
            "organic_treatment": "Trichoderma harzianum soil application."
        },
        "Late Blight": {
            "health_status": "Diseased",
            "confidence_default": 0.95,
            "cause": "Phytophthora infestans",
            "symptoms": {
                "en": "Rapidly expanding black water-soaked areas, white mildew under leaves.",
                "hi": "पत्तियों पर तेजी से फैलते काले धब्बे और सड़ांध।",
                "mr": "पानांवर वेगाने पसरणारे काळे डाग आणि सड."
            },
            "actions": {
                "en": ["Spray protective fungicides immediately.", "Stop irrigation if high moisture."],
                "hi": ["तुरंत सुरक्षात्मक फफूंदनाशक का छिड़काव करें।"],
                "mr": ["त्वरित बुरशीनाशक फवारा."]
            },
            "chemical_treatment": "Mancozeb + Metalaxyl 2.5g/L.",
            "organic_treatment": "Bordeaux Mixture spray (1%)."
        },
        "Healthy": {
            "health_status": "Healthy",
            "confidence_default": 0.97,
            "cause": "Good health",
            "symptoms": {
                "en": "Lush green potato canopy.",
                "hi": "हरी-भरी स्वस्थ फसल।",
                "mr": "निरोगी हिरवीगार पिके."
            },
            "actions": {
                "en": ["Monitor tuber formation and maintain soil moisture around 50-60%."],
                "hi": ["नमी 50-60% बनाए रखें।"],
                "mr": ["मातीतील ओलावा ५०-६०% ठेवा."]
            },
            "chemical_treatment": "None",
            "organic_treatment": "Decomposed compost."
        }
    },

    "Rice": {
        "Bacterial Leaf Blight": {
            "health_status": "Diseased",
            "confidence_default": 0.91,
            "cause": "Xanthomonas oryzae pv. oryzae",
            "symptoms": {
                "en": "Wavy yellow to white lesions starting from leaf tips and margins.",
                "hi": "धान की पत्तियों के किनारों से पीला और सफेद सुखापन।",
                "mr": "तांदळाच्या पानांच्या कडा पिवळ्या व पांढऱ्या पडणे."
            },
            "actions": {
                "en": ["Drain field water temporarily.", "Avoid excessive nitrogen fertilizers."],
                "hi": ["खेत से अतिरिक्त पानी निकालें।", "अधिक यूरिया न डालें।"],
                "mr": ["शेतातून अतिरिक्त पाणी काढून द्या.", "जास्त नत्र वापरू नका."]
            },
            "chemical_treatment": "Streptocycline 1g + Copper Oxychloride 30g in 10L water.",
            "organic_treatment": "Fresh cow dung extract (20%) spray."
        },
        "Blast Disease": {
            "health_status": "Diseased",
            "confidence_default": 0.93,
            "cause": "Magnaporthe oryzae fungus",
            "symptoms": {
                "en": "Spindle-shaped or eye-shaped spots with reddish-brown margins on leaf.",
                "hi": "नाव के आकार के या आंख जैसे भूरे धब्बे।",
                "mr": "पानांवर टोकदार किंवा डोळ्याच्या आकाराचे काळे-तांबूस डाग (तांबेरा)."
            },
            "actions": {
                "en": ["Maintain flooded conditions if possible.", "Apply systemic fungicide."],
                "hi": ["फफूंदनाशक का उपयोग करें।"],
                "mr": ["योग्य बुरशीनाशक वापरा."]
            },
            "chemical_treatment": "Tricyclazole 75 WP at 0.6g/L or Isoprothiolane at 1.5ml/L.",
            "organic_treatment": "Pseudomonas fluorescens 10g/L spray."
        },
        "Healthy": {
            "health_status": "Healthy",
            "confidence_default": 0.98,
            "cause": "Optimal paddy growth",
            "symptoms": {
                "en": "Healthy green paddy tiller development.",
                "hi": "स्वस्थ धान के कल्ले और हरी पत्तियां।",
                "mr": "छातीइतकी निरोगी भात पिके."
            },
            "actions": {
                "en": ["Ensure 2-5cm water level during tillering."],
                "hi": ["2-5 सेमी पानी का स्तर बनाए रखें।"],
                "mr": ["पाण्याचा योग्य उपसा ठेवा."]
            },
            "chemical_treatment": "None",
            "organic_treatment": "Azospirillum & PSB biofertilizer."
        }
    },

    "Wheat": {
        "Yellow Rust": {
            "health_status": "Diseased",
            "confidence_default": 0.94,
            "cause": "Puccinia striiformis fungal infection",
            "symptoms": {
                "en": "Bright yellow pustules arranged in linear stripes along leaf veins.",
                "hi": "गेहूं की पत्तियों पर पीले रंग की धारियां और हल्दी जैसा पाउडर।",
                "mr": "गव्हाच्या पानांवर पिवळ्या रंगाचे पट्टे (हळद्या/तांबेरा)."
            },
            "actions": {
                "en": ["Spray fungicide immediately upon detection to stop spread."],
                "hi": ["तुरंत फफूंदनाशक का छिड़काव करें।"],
                "mr": ["रोग दिसताच त्वरित फवारणी करा."]
            },
            "chemical_treatment": "Propiconazole 25 EC at 1ml/L water.",
            "organic_treatment": "Fermented buttermilk/sour curd solution spray (5%)."
        },
        "Healthy": {
            "health_status": "Healthy",
            "confidence_default": 0.99,
            "cause": "Healthy grain development",
            "symptoms": {
                "en": "Vibrant green wheat canopy.",
                "hi": "हरी-भरी गेहूं की फसल।",
                "mr": "निरोगी गव्हाचे पीक."
            },
            "actions": {
                "en": ["Provide light irrigation at crown root initiation & flowering."],
                "hi": ["समय पर सिंचाई करें।"],
                "mr": ["वेळेवर पाणी द्या."]
            },
            "chemical_treatment": "None",
            "organic_treatment": "Vermicompost top dressing."
        }
    },

    "Cotton": {
        "Bollworm Damage": {
            "health_status": "Diseased",
            "confidence_default": 0.90,
            "cause": "Helicoverpa armigera / Pink Bollworm caterpillar pest",
            "symptoms": {
                "en": "Bores into cotton bolls, square dropping, chewed leaf edges.",
                "hi": "कपास के घेंघों में छेद, डोडे गिरना और सुंडी की मौजूदगी।",
                "mr": "कपाशीच्या बोंडात छिद्रे आणि गुलाबी बोंडअळीचा प्रादुर्भाव."
            },
            "actions": {
                "en": ["Install Pheromone traps (5/acre).", "Pick damaged bolls."],
                "hi": ["फेरोमोन ट्रैप लगाएं।", "क्षतिग्रस्त डोडे नष्ट करें।"],
                "mr": ["कामगंधी सापळे लावा.", "किडलेली बोंडे गोळा करून नष्ट करा."]
            },
            "chemical_treatment": "Spinetoram 11.7 SC at 1ml/L or Emamectin Benzoate 5 SG at 0.5g/L.",
            "organic_treatment": "Release Trichogramma egg parasitoids or spray Beauveria bassiana."
        },
        "Healthy": {
            "health_status": "Healthy",
            "confidence_default": 0.96,
            "cause": "Optimal cotton growth",
            "symptoms": {
                "en": "Broad green leaves, healthy bolls and squares.",
                "hi": "स्वस्थ चौड़ी हरी पत्तियां।",
                "mr": "छान निरोगी कपाशीची पाने."
            },
            "actions": {
                "en": ["Monitor regularly for sucking pests."],
                "hi": ["नियमित कीट निगरानी करें।"],
                "mr": ["किडींची नियमित पाहणी करा."]
            },
            "chemical_treatment": "None",
            "organic_treatment": "Neem oil foliar spray."
        }
    },

    "Corn": {
        "Fall Armyworm": {
            "health_status": "Diseased",
            "confidence_default": 0.92,
            "cause": "Spodoptera frugiperda larvae",
            "symptoms": {
                "en": "Ragged holes in central whorl, saw-dust like excrement inside whorl.",
                "hi": "मक्के के पोंगली में बड़े छेद और चूरे जैसा मल।",
                "mr": "मक्याच्या पोंग्यात मोठी छिद्रे आणि लहरी अळीचे मल."
            },
            "actions": {
                "en": ["Apply sand + neem cake mixture in whorls.", "Spray targeted insecticide."],
                "hi": ["पोंगली में रेत और नीम की खली डालें।"],
                "mr": ["पोंग्यात वाळू व निंबोळी पेंड टाका."]
            },
            "chemical_treatment": "Chlorantraniliprole 18.5 SC at 0.4ml/L.",
            "organic_treatment": "Metarhizium anisopliae or Bacillus thuringiensis (Bt) spray."
        },
        "Healthy": {
            "health_status": "Healthy",
            "confidence_default": 0.97,
            "cause": "Healthy maize foliage",
            "symptoms": {
                "en": "Dark green leaves with sturdy stem.",
                "hi": "मजबूत तना और हरी पत्तियां।",
                "mr": "मजबूत ताट आणि निरोगी पाने."
            },
            "actions": {
                "en": ["Ensure adequate moisture during knee-high and tasseling stages."],
                "hi": ["घुटने की ऊंचाई पर सिंचाई करें।"],
                "mr": ["योग्य टप्प्यावर पाणी द्या."]
            },
            "chemical_treatment": "None",
            "organic_treatment": "Farmyard manure application."
        }
    }
}
