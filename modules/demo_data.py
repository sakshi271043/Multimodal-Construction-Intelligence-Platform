"""
High-fidelity demonstration data for Multimodal Construction Intelligence Platform.
Enables instant evaluation and standalone showcase with zero API key dependencies.
"""

from typing import Any, Dict

DEMO_PPE_SITES: Dict[str, Dict[str, Any]] = {
    "Active High-Rise Slab Rebar & Concreting": {
        "title": "Active High-Rise Slab Rebar & Concreting (Floor 14)",
        "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb18626c2?auto=format&fit=crop&w=1200&q=80",
        "zone": "Tower B, Level 14 Deck",
        "safety_score": 72,
        "overall_status": "Needs Attention (Minor Violations)",
        "workers_detected": 6,
        "ppe_detection": [
            {
                "item": "Safety Helmets (Hard Hats)",
                "status": "Partial",
                "compliance_rate": "83% (5/6 Workers)",
                "code_reference": "OSHA 1926.100 & IS 2925:1984",
                "notes": "5 workers equipped with Type II Class E helmets; 1 worker re-tying rebar perimeter zone bareheaded."
            },
            {
                "item": "High-Visibility Safety Vests",
                "status": "Detected",
                "compliance_rate": "100% (6/6 Workers)",
                "code_reference": "OSHA 1926.200 & IS 15809:2017",
                "notes": "All 6 workers wearing fluorescent Class 2 reflective vests with retroreflective bands."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "status": "Detected",
                "compliance_rate": "100% (6/6 Workers)",
                "code_reference": "OSHA 1926.96 & IS 15298:2011",
                "notes": "Puncture-resistant, steel-shank construction boots observed across rebar mat."
            },
            {
                "item": "Safety Harness & Fall Arrest",
                "status": "Partial",
                "compliance_rate": "50% (1/2 at Edge)",
                "code_reference": "OSHA 1926.502 & IS 3521:1999",
                "notes": "2 workers active within 1.5m of unprotected slab edge; 1 worker not tethered to static lifeline."
            },
            {
                "item": "Eye & Face Protection (Goggles)",
                "status": "Partial",
                "compliance_rate": "50% (3/6 Workers)",
                "code_reference": "OSHA 1926.102 & IS 5983:1980",
                "notes": "Concrete boom pump vibrator operators lacking anti-splash impact goggles."
            },
            {
                "item": "Heavy-Duty Work Gloves",
                "status": "Detected",
                "compliance_rate": "100% (6/6 Workers)",
                "code_reference": "OSHA 1926.95 & IS 6994:1973",
                "notes": "EN 388 Level 4 cut-resistant nitrile dipped gloves in active rebar handling."
            }
        ],
        "site_hazards": [
            {
                "hazard_id": "HAZ-001",
                "hazard_type": "Unprotected Slab Edge Fall Hazard",
                "severity": "Critical",
                "location": "Level 14 South-East Perimeter Edge",
                "regulatory_code": "OSHA 1926.501(b)(1) & IS 3696 Part 1",
                "corrective_remedy": "Immediately halt work near edge. Install 42-inch high dual-tier guardrail with intermediate mid-rail and toe-board. Mandate 100% tie-off to certified horizontal lifeline before resumption."
            },
            {
                "hazard_id": "HAZ-002",
                "hazard_type": "Personnel Without Hard Hat in Crane Swivel Arc",
                "severity": "High",
                "location": "Bay C Central Rebar Mat",
                "regulatory_code": "OSHA 1926.100 & IS 2925",
                "corrective_remedy": "Issue immediate stop-work alert to non-compliant worker. Supply approved Type II Class E helmet with chin strap. Re-induct worker into mandatory site PPE protocol."
            },
            {
                "hazard_id": "HAZ-003",
                "hazard_type": "Concrete Pump Hose Whip & Slurry Backsplash",
                "severity": "Medium",
                "location": "Boom Placer Terminal Discharge",
                "regulatory_code": "OSHA 1926.702 & IS 456 Clause 13.3",
                "corrective_remedy": "Secure boom hose joint with safety whip-check cable. Require full face shield and impact goggles for pump line operators."
            }
        ],
        "executive_summary": "Active floor 14 slab decking demonstrates solid compliance in reflective vests and steel footwear. However, critical perimeter edge exposure without dual-lanyard tie-off and 1 bareheaded rebar worker constitute immediate non-compliance items under OSHA 1926 Subpart M and IS 456. Work at perimeter edge must be suspended until guardrails are certified."
    },
    "Deep Excavation & Diaphragm Wall Zone": {
        "title": "Deep Basement Excavation & Diaphragm Wall (Substructure)",
        "image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80",
        "zone": "Basement Level 3 Shoring Pit",
        "safety_score": 89,
        "overall_status": "Compliant (OSHA / IS 456 Approved)",
        "workers_detected": 4,
        "ppe_detection": [
            {
                "item": "Safety Helmets (Hard Hats)",
                "status": "Detected",
                "compliance_rate": "100% (4/4 Workers)",
                "code_reference": "OSHA 1926.100 & IS 2925",
                "notes": "All workers wearing industrial safety helmets with fastened chin straps."
            },
            {
                "item": "High-Visibility Safety Vests",
                "status": "Detected",
                "compliance_rate": "100% (4/4 Workers)",
                "code_reference": "OSHA 1926.200 & IS 15809",
                "notes": "High-luminescence Class 3 vests with reflective strips visible in deep pit."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "status": "Detected",
                "compliance_rate": "100% (4/4 Workers)",
                "code_reference": "OSHA 1926.96 & IS 15298",
                "notes": "Waterproof rubberized safety gumboots with steel toe and puncture plate."
            },
            {
                "item": "Safety Harness & Fall Arrest",
                "status": "N/A",
                "compliance_rate": "Ground Pit Excavation",
                "code_reference": "OSHA 1926.502",
                "notes": "Personnel operating on graded pit floor; excavation access ladder secured."
            },
            {
                "item": "Eye & Face Protection",
                "status": "Detected",
                "compliance_rate": "100% (4/4 Workers)",
                "code_reference": "OSHA 1926.102",
                "notes": "Anti-fog dust goggles worn during hydraulic breaker chipping."
            },
            {
                "item": "Heavy-Duty Work Gloves",
                "status": "Detected",
                "compliance_rate": "100% (4/4 Workers)",
                "code_reference": "OSHA 1926.95",
                "notes": "Vibration-dampening heavy work gloves in use."
            }
        ],
        "site_hazards": [
            {
                "hazard_id": "HAZ-004",
                "hazard_type": "Dewatering Discharge Hose Slip / Trip Hazard",
                "severity": "Low",
                "location": "Sump Well Drainage Trench",
                "regulatory_code": "OSHA 1926.25(a) Housekeeping",
                "corrective_remedy": "Route flexible 4-inch discharge hose along trench perimeter berm and stake down to eliminate walkway tripping hazards."
            }
        ],
        "executive_summary": "Basement excavation pit demonstrates stellar site safety discipline. Diaphragm wall strutting monitored, trench egress ladders properly tied off, and full PPE compliance achieved. Continuous dewatering operational."
    },
    "Suspended Facade Scaffolding & Cradle": {
        "title": "Suspended Facade Scaffolding & Glazing Cradle",
        "image_url": "https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1200&q=80",
        "zone": "North Facade Elevation",
        "safety_score": 54,
        "overall_status": "Non-Compliant (Stop-Work Risk)",
        "workers_detected": 3,
        "ppe_detection": [
            {
                "item": "Safety Helmets (Hard Hats)",
                "status": "Partial",
                "compliance_rate": "67% (2/3 Workers)",
                "code_reference": "OSHA 1926.100 & IS 2925",
                "notes": "1 technician operating without chinstrap in high wind zone."
            },
            {
                "item": "High-Visibility Safety Vests",
                "status": "Detected",
                "compliance_rate": "100% (3/3 Workers)",
                "code_reference": "OSHA 1926.200",
                "notes": "Standard orange vests in use."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "status": "Detected",
                "compliance_rate": "100% (3/3 Workers)",
                "code_reference": "OSHA 1926.96",
                "notes": "Slip-resistant safety boots verified."
            },
            {
                "item": "Safety Harness & Fall Arrest",
                "status": "Non-Compliant",
                "compliance_rate": "33% (1/3 Workers)",
                "code_reference": "OSHA 1926.451 & IS 3696 Part 2",
                "notes": "CRITICAL: Suspended cradle workers anchored to scaffold rail instead of independent vertical lifeline."
            },
            {
                "item": "Eye & Face Protection",
                "status": "Partial",
                "compliance_rate": "33%",
                "code_reference": "OSHA 1926.102",
                "notes": "Lacking wind-protective eye wear at 40m elevation."
            },
            {
                "item": "Heavy-Duty Work Gloves",
                "status": "Detected",
                "compliance_rate": "100%",
                "code_reference": "OSHA 1926.95",
                "notes": "High-grip suction-handling gloves."
            }
        ],
        "site_hazards": [
            {
                "hazard_id": "HAZ-005",
                "hazard_type": "Improper Fall Arrest Anchorage on Suspended Cradle",
                "severity": "Critical",
                "location": "North Facade Cradle #2 (Elevation +38m)",
                "regulatory_code": "OSHA 1926.451(g)(3) & IS 3696 Part 2",
                "corrective_remedy": "IMMEDIATE STOP WORK: Cradle occupants must never anchor to cradle guardrail. Deploy dedicated 16mm polyamide vertical lifelines from roof parapet with certified rope grabs."
            },
            {
                "hazard_id": "HAZ-006",
                "hazard_type": "Missing Kick-Plate / Toe-Board on Scaffolding Platform",
                "severity": "High",
                "location": "Intermediate Staging Tier",
                "regulatory_code": "OSHA 1926.451(h)(2) & IS 3696",
                "corrective_remedy": "Install 150mm steel toe-boards along outer scaffold perimeter to prevent hand tools and glazing bolts from dropping onto ground walkways."
            }
        ],
        "executive_summary": "SEVERE COMPLIANCE BREACH: Suspended platform operations violate OSHA 1926.451 fall protection protocols. Anchorage to the cradle frame rather than independent vertical lifelines poses catastrophic failure risk. Operations suspended pending EHS inspection."
    }
}

DEMO_CRACKS: Dict[str, Dict[str, Any]] = {
    "Structural Shear Crack at Beam-Column Joint": {
        "title": "Structural Shear Crack at Beam-Column Joint",
        "image_url": "https://images.unsplash.com/photo-1590486803833-1c5dc8ddd4c8?auto=format&fit=crop&w=1200&q=80",
        "element": "RCC Beam-Column Connection (Column C-4 / Beam B-12)",
        "defect_type": "Structural Shear Crack",
        "estimated_width_mm": 1.85,
        "is456_exposure_limit_mm": 0.20,
        "urgency": "Urgent (High Structural Risk)",
        "root_causes": "Principal tensile stress exceedance near support face under cyclic lateral or gravity loading; inadequate shear stirrup spacing (per IS 13920 ductile detailing) and high diagonal tension.",
        "engineering_repairs": [
            "Install immediate temporary hydraulic propping beneath beam B-12 span within 1.5m of column face to relieve live loads.",
            "Conduct Ultrasonic Pulse Velocity (UPV) Non-Destructive Testing (IS 13311 Part 1) to determine internal crack propagation depth.",
            "Install surface-mounted injection nipples at 150mm staggered intervals and seal crack line with thixotropic epoxy paste.",
            "Pressure-inject low-viscosity structural epoxy resin (viscosity < 200 cps, tensile strength > 30 MPa) at 0.2 to 0.4 MPa pressure.",
            "Apply bi-directional Carbon Fiber Reinforced Polymer (CFRP) fabric wrap (2 layers of 300 g/m²) saturated with structural epoxy for external shear retrofit per ACI 440.2R."
        ],
        "standards_reference": "IS 456:2000 Clause 35.3.2, IS 13920:2016 Clause 6, ACI 224.1R-07",
        "remediation_urgency_days": "Immediate (Within 48 Hours)"
    },
    "Diagonal Foundation Settlement Crack on Masonry": {
        "title": "Diagonal Foundation Settlement Crack on Masonry Wall",
        "image_url": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=1200&q=80",
        "element": "Ground Floor External Load-Bearing Masonry Infill",
        "defect_type": "Settlement Crack",
        "estimated_width_mm": 0.85,
        "is456_exposure_limit_mm": 0.30,
        "urgency": "Moderate (Monitor & Remediate)",
        "root_causes": "Differential foundation settlement caused by seasonal moisture fluctuation in expansive black cotton soil subgrade; lack of continuous plinth tie-beam.",
        "engineering_repairs": [
            "Affix calibrated acrylic tell-tale crack monitoring gauges across crack face and log displacement weekly for 30 days.",
            "Verify subsoil compaction and install localized micro-piles or chemical polyurethane soil stabilization if settlement remains active.",
            "Rake out masonry mortar joints along crack trajectory to 25mm depth.",
            "Pressure-grout cracks with non-shrink polymer-modified cementitious micro-fine grout conforming to IS 4998.",
            "Stitch masonry using 6mm austenitic stainless steel helical rebar rods embedded in structural thixotropic resin at 450mm vertical centers."
        ],
        "standards_reference": "IS 1905:1987 (Masonry Practice), IS 1080 (Shallow Foundations), BRE Digest 251",
        "remediation_urgency_days": "14 to 30 Days (After Settlement Stabilization)"
    },
    "Concrete Spalling with Corroded Rebar Exposure": {
        "title": "Concrete Spalling with Corroded Rebar Delamination",
        "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb18626c2?auto=format&fit=crop&w=1200&q=80",
        "element": "External Balcony Cantilever Beam Soffit",
        "defect_type": "Spalling & Carbonation Corrosion",
        "estimated_width_mm": 3.40,
        "is456_exposure_limit_mm": 0.20,
        "urgency": "Urgent (High Structural Risk)",
        "root_causes": "Inadequate clear concrete cover (< 20mm), carbonation front reaching rebar steel causing depassivation of protective alkaline film; rust expansion exerting 2.5x volumetric hoop stress, fracturing cover concrete.",
        "engineering_repairs": [
            "Chisel away all hollow, delaminated concrete to at least 20mm beyond all exposed reinforcing steel perimeter.",
            "Abrasive wire-brush or sand-blast corroded rebar to Swedish Standard SA 2.5 cleanliness.",
            "Apply two coats of active zinc-rich epoxy anti-corrosion rebar primer conforming to ASTM A775.",
            "Apply structural bonding agent (epoxy/acrylic co-polymer) to concrete substrate.",
            "Re-build profile using fiber-reinforced polymer-modified mortar (PMM) with 28-day compressive strength > 45 N/mm²."
        ],
        "standards_reference": "IS 456:2000 Clause 26.4 (Cover Requirements), EN 1504 Concrete Repair, ICRI 310.1R",
        "remediation_urgency_days": "Within 7 Days"
    },
    "Plastic Shrinkage Hairline Surface Crazing": {
        "title": "Plastic Shrinkage Hairline Surface Crazing",
        "image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80",
        "element": "Roof Terrace Exposed Slab Deck",
        "defect_type": "Hairline Crack",
        "estimated_width_mm": 0.12,
        "is456_exposure_limit_mm": 0.20,
        "urgency": "Low (Aesthetic / Non-Critical)",
        "root_causes": "Rapid early surface evaporation rate (> 1.0 kg/m²/hr) exceeding bleeding rate during concrete placement under direct hot sun and wind; delayed commencement of wet hessian curing.",
        "engineering_repairs": [
            "Thoroughly pressure-wash surface to eliminate dust and laitance.",
            "Apply two coats of deep-penetrating silane-siloxane hydrophobic breathable penetrant sealer.",
            "For continuous wet terrace protection, overlay with elastomeric polyurethane waterproof membrane with UV-stable topcoat.",
            "Structural epoxy injection is NOT required as crack width (0.12mm) is well within IS 456 permissible limits (0.20mm)."
        ],
        "standards_reference": "IS 456:2000 Clause 13.5 (Curing), ACI 305R-10 Hot Weather Concreting, ACI 224R",
        "remediation_urgency_days": "Routine Preventive Maintenance"
    }
}

DEMO_WEATHER_PROTOCOLS: Dict[str, Dict[str, Any]] = {
    "High Wind / Gale (> 38 km/h)": {
        "icon": "💨",
        "condition": "High Wind / Gale (> 38 km/h)",
        "severity": "High",
        "style_class": "wind",
        "headline": "CRANE SUSPENSION ALERT & HIGH-ELEVATION LOCKDOWN",
        "protocols": [
            "Tower Cranes & Mobile Hoists: Mandatory halt to all lifting operations when sustained wind exceeds 38 km/h (10.5 m/s) per IS 875 Part 3 and OSHA 1926.1431. Release slew brakes to enable free wind-vaning.",
            "Suspended Access Cradles & Scaffolding: Lower all suspended gondolas and cradles to ground level. Tie down loose scaffold boards, netting, and corrugated metal sheets.",
            "Facade & Glazing: Immediately suspend installation of architectural glass curtain walls and large formwork shutters due to sail effect.",
            "Site Perimeter: Secure temporary barricades, hoarding sheets, and loose debris across upper open decks."
        ]
    },
    "Heavy Rain / Monsoon Inundation": {
        "icon": "🌧️",
        "condition": "Heavy Rain / Monsoon Inundation",
        "severity": "High",
        "style_class": "rain",
        "headline": "ELECTRICAL HAZARD & CONCRETE WASHOUT MITIGATION",
        "protocols": [
            "Concreting Protocol: Cease unshielded slab concreting immediately. Rainwater increases water-cement (w/c) ratio, drastically lowering compressive strength. Cover green concrete with polythene sheeting.",
            "Electrical Safety: De-energize low-lying distribution boards. Ensure all temporary power lines pass through 30mA residual current circuit breakers (RCCB/ELCB). Ground submersible dewatering pumps.",
            "Excavation & Slopes: Inspect trench shoring and soil nail retaining walls for slope saturation, hydrostatic pore pressure buildup, and mudslip warning signs under IS 3764.",
            "Water Stagnation: Deploy continuous centrifugal dewatering pumps in basement pits and lift shafts to prevent buoyancy uplift."
        ]
    },
    "Extreme Heat (> 40°C / High UV)": {
        "icon": "☀️",
        "condition": "Extreme Heat (> 40°C / High UV)",
        "severity": "Medium",
        "style_class": "heat",
        "headline": "CONCRETE HYDRATION CONTROL & WORKER HEAT DEFENSE",
        "protocols": [
            "Concreting Timing: Shift major structural pours to early morning (04:00 - 09:00) or night shifts. Maximum fresh concrete temperature must not exceed 32°C at placement (IS 456 Clause 14).",
            "Hydration Crack Prevention: Use chilled mixing water and replace 20-30% cement with pulverized fly ash (IS 3812) to dampen heat of hydration. Commence continuous wet ponding/hessian curing immediately after initial set.",
            "Worker Welfare & OSHA Heat Index: Institute 45-minute work / 15-minute shaded rest rotations. Provide electrolyte rehydration stations and sun-shade awnings across open decks.",
            "Formwork Striking: Do not strip timber or steel formwork prematurely; premature thermal shock causes severe micro-cracking."
        ]
    },
    "Dense Fog / Poor Visibility (< 100m)": {
        "icon": "🌫️",
        "condition": "Dense Fog / Poor Visibility (< 100m)",
        "severity": "Medium",
        "style_class": "wind",
        "headline": "BLIND LIFT PROTOCOLS & SITE TRAFFIC RESTRICTION",
        "protocols": [
            "Lifting Operations: Suspend blind tandem crane lifts where spotter visibility is obscured. Require dual two-way radio channels and radar proximity sensors.",
            "Vehicular Movement: Restrict transit mixer and dumper speed to 10 km/h within site boundaries. Mandate amber flashing beacons and high-beam fog lights.",
            "Work at Height: Equip scaffolding perimeters with high-visibility hazard strobe lighting."
        ]
    },
    "Normal / Clear Weather": {
        "icon": "🌤️",
        "condition": "Normal / Clear Weather",
        "severity": "Low",
        "style_class": "normal",
        "headline": "OPTIMUM PRODUCTION WINDOW & STANDARD CIVIL PROTOCOLS",
        "protocols": [
            "Superstructure Cycle: Ideal conditions for tower crane cycling, formwork shuttering, and slab rebar inspection.",
            "Quality Assurance: Verify cube casting (minimum 3 cubes per 50 m³ pour as per IS 456 Table 2) and record slump cone measurements.",
            "EHS Maintenance: Conduct routine weekly safety toolbox talks, fire extinguisher inspections, and first aid replenishment."
        ]
    }
}

DEMO_CHAT_KNOWLEDGE: Dict[str, str] = {
    "is456": (
        "**IS 456:2000 — Code of Practice for Plain and Reinforced Concrete**\n\n"
        "1. **Permissible Crack Widths (Clause 35.3.2):**\n"
        "   - **Mild Exposure** (Internal surfaces, protected): Maximum **0.30 mm**\n"
        "   - **Moderate Exposure** (Sheltered from severe rain/freezing): Maximum **0.20 mm**\n"
        "   - **Severe / Extreme Exposure** (Coastal, marine spray, aggressive chemicals): Maximum **0.10 mm**\n\n"
        "2. **Minimum Concrete Grades:**\n"
        "   - Plain Concrete (PCC): Minimum **M15**\n"
        "   - Reinforced Concrete (RCC): Minimum **M20** (Severe/Coastal: M30)\n\n"
        "3. **Nominal Clear Cover (Clause 26.4):**\n"
        "   - Footings: 50 mm\n"
        "   - Columns: 40 mm (or bar diameter)\n"
        "   - Beams: 25 mm\n"
        "   - Slabs: 20 mm\n"
        "   - Coastal / Severe exposure: +15 to 20 mm additional sacrificial cover."
    ),
    "osha_wind": (
        "**Tower Crane Wind Speed Safety Limits (OSHA 1926.1431 & IS 875 Part 3):**\n\n"
        "• **Maximum Safe Operating Wind Speed:** Typically **38 km/h (10.5 m/s or 24 mph)** for standard tower crane hook operations.\n"
        "• **Climbing & Jib Jacking Operations:** Must cease when wind exceeds **25 km/h (7 m/s)**.\n"
        "• **Out-of-Service Protocol (Gale / Cyclone > 50 km/h):**\n"
        "  1. Remove all suspended loads immediately.\n"
        "  2. Park trolley at minimum radius near mast.\n"
        "  3. Hoist hook block to highest limit switch.\n"
        "  4. **CRITICAL:** Disengage the slew brake (enable *weathervaning / free-slewing*) so the crane jib naturally turns with wind direction to minimize overturning drag."
    ),
    "crack_repair": (
        "**Engineering Crack Repair Protocol: Epoxy Injection vs Polyurethane Grouting**\n\n"
        "1. **Structural Epoxy Pressure Injection:**\n"
        "   - **Use Case:** Dry, structural cracks (> 0.15 mm) in beams, columns, and slabs where structural tensile continuity must be restored.\n"
        "   - **Properties:** High compressive (> 70 MPa) and tensile bond strength (> 30 MPa) exceeding original concrete strength.\n"
        "   - **Procedure:** Surface clean -> Seal exterior face with thixotropic epoxy putty -> Mount injection ports at 150-200mm centers -> Inject from lowest port upward until resin emerges from adjacent port.\n\n"
        "2. **Hydrophilic Polyurethane (PU) Injection:**\n"
        "   - **Use Case:** Active water-bearing cracks, basement diaphragm walls, retaining walls, swimming pools.\n"
        "   - **Mechanism:** Reacts instantaneously with water to expand 10x-20x into a closed-cell flexible rubberized foam seal.\n"
        "   - **Note:** PU stops water ingress but does not provide structural shear/tensile capacity."
    ),
    "mix_design": (
        "**Cement & Concrete Estimation Thumb Rules (CPWD & IS 10262):**\n\n"
        "• **M20 Grade (1 : 1.5 : 3 nominal):** ~6.8 bags cement / m³ concrete\n"
        "• **M25 Grade (1 : 1 : 2 design):** ~7.8 to 8.2 bags cement / m³ concrete\n"
        "• **M30 / M35 High Performance:** ~8.5 to 9.2 bags cement / m³ concrete (with superplasticizer, w/c ratio 0.38 - 0.42)\n\n"
        "**Structural Steel Reinforcement Benchmarks:**\n"
        "• Residential RCC Frame: 3.5 to 4.2 kg / sqft of built-up area\n"
        "• Commercial High-Rise / Tech Park: 4.8 to 5.8 kg / sqft of built-up area\n"
        "• Heavy Industrial / PEB Foundations: 5.5 to 7.0 kg / sqft"
    )
}
