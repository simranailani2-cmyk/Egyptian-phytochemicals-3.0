import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Egyptian Ethnopharmacology Docking Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for design styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f385c;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. App Framing & Titles
st.title("𓆎𓅓𓏏𓊖 KemetDock Portal")
st.subheader("Bridging Ancient Egyptian Phytotherapy with Computational Molecular Docking")
st.markdown("---")

# 3. EMBEDDED DATASET (No Excel file needed!)
@st.cache_data
def load_data():
    raw_data = [
        [1, "Allium sativum", "Amaryllidaceae", "Garlic", "Ebers Papyrus, Par. 432: 𓆼𓄿𓆰 (Hamanu)", "Garlic is applied to treat pestilence, bodily swellings, and clear out internal parasites.", "Allicin", "1M17", -7.2, "C=CCSS(=O)CC=C", "SAFE (Common food item; avoid raw excess if on anticoagulants)"],
        [2, "Commiphora myrrha", "Burseraceae", "Myrrh", "Ebers Papyrus, Par. 510: 𓂝𓈖𓏏𓆰 (Antyw)", "Apply myrrh resin to open wounds, pustules, and skin eruptions to draw out inflammation.", "Myrrhanol A", "3LN1", -8.5, "CC1=C[C@@H](O)[C@@H]2[C@H](O)CC[C@]3(C)[C@H](CC[C@@H]23)C(=C)CO1", "SAFE (Excellent topically; check therapeutic doses if internal)"],
        [3, "Punica granatum", "Lythraceae", "Pomegranate", "Ebers Papyrus, Par. 50: 𓈖𓄿𓉔𓏠𓆰 (Nhmd)", "The root of pomegranate is crushed in water and drunk to destroy tapeworms and flatulence.", "Ellagic Acid", "1M17", -8.9, "C1=C2C3=C(C(=C1O)O)OC(=O)C4=CC(=C(C(=C43)OC2=O)O)O", "SAFE (High antioxidant value; well tolerated)"],
        [4, "Ricinus communis", "Euphorbiaceae", "Castor Oil Plant", "Ebers Papyrus, Par. 251: 𓂧𓎛𓈖𓆰 (Dgbm)", "Chew the beans with beer to flush disease from the belly; use roots in water for head pain.", "Ricinoleic acid", "2X79", -6.8, "CCCCCC(O)CC=CCCCCCCCC(=O)O", "HIGH TOXICITY WARNING (Seeds contain deadly Ricin; oil must be highly processed)"],
        [5, "Acacia nilotica", "Fabaceae", "Egyptian Acacia", "Ebers Papyrus, Par. 783: 𓈙𓈖𓍿𓆰 (Sndjt)", "To soothe painful joints and localized fluid swelling, apply a poultice of acacia leaves and honey.", "Catechin", "4UYD", -8.1, "C1C(C(OC2=CC(=CC(=C21)O)O)C3=CC(=C(C=C3)O)O)O", "SAFE (Contains strong plant tannins; high doses may cause mild nausea)"],
        [6, "Coriandrum sativum", "Apiaceae", "Coriander", "Edwin Smith, Par. 41: 𓎛𓄿𓏏𓏤𓆰 (Hawt)", "Coriander is steeped and drunk to cool heat in the tissue and calm an overactive belly.", "Linalool", "3LN1", -6.4, "CC(=CCCC(C)(C=C)O)C", "SAFE (Standard culinary herb)"],
        [7, "Boswellia carterii", "Burseraceae", "Frankincense", "Ebers Papyrus, Par. 640: 𓊹𓋴𓈖𓏏𓆰 (Sneter)", "Fumigate the room or apply the resin topically to banish foul breath and rotting of flesh.", "Boswellic Acid", "2AZ5", -9.1, "CC1CCC2(CCC3(C(=CCC4C3(CCC5C4(CCCC5(C)C(=O)O)C)C)C2C1(C)C)C)C", "SAFE (Mild gut irritation possible only at extremely high extract dosages)"],
        [8, "Nigella sativa", "Ranunculaceae", "Black Cumin", "Hearst Papyrus, Par. 112: 𓋴𓄿𓏠𓏏𓆰 (Smet)", "The black seeds are ground up, mixed with oil, and applied to painful skin ulcers to dry them.", "Thymoquinone", "1M17", -7.4, "CC1=CC(=O)C(C=C1=O)C(C)C", "SAFE (Highly protective cellular profile; metabolic enhancer)"],
        [9, "Aloe vera", "Asphodelaceae", "Aloe", "Ebers Papyrus, Par. 603: 𓎼𓄿𓃭𓏤𓆰 (Grt)", "The gel is smoothed over raw skin burns and weeping sores to cool and close the barrier.", "Aloin", "3POZ", -7.9, "CC1=CC=CC2=C1C(=O)C3=C(C(=C(C=C3C2[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)O)O", "SAFE (Topically excellent; unprocessed raw leaf latex has strong laxative effects)"],
        [10, "Salix subserrata", "Salicaceae", "Safsaf Willow", "Ebers Papyrus, Par. 294: 𓏏𓆑𓏏𓆰 (Tft)", "Boil leaves of the willow to bind onto wounds that throw off fluid, lowering the hot fever.", "Salicin", "3LN1", -7.0, "C1=CC=C(C(=C1)CO)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O", "SAFE (Precursor to modern aspirin; avoid if allergic to aspirin/salicylates)"],
        [11, "Papaver somniferum", "Papaveraceae", "Opium Poppy", "Ebers Papyrus, Par. 782", "Used to calm crying children and cool deep-tissue pain.", "Morphine", "4DKL", -8.2, "CN1CCC23C4C1CC5=C6C2(C(CC4O)O)OC7=C6C(=CC=C7)C5", "CONTROLLED / TOXIC IN EXCESS (High risk of dependency; potent central analgesic)"],
        [12, "Ceratonia siliqua", "Fabaceae", "Carob Tree", "Ebers Papyrus, Par. 19", "Crushed with honey and beer to bind loose bowels and fight rot.", "Gallic Acid", "4UYD", -7.1, "C1=C(C=C(C(=C1O)O)O)C(=O)O", "SAFE (Nutritious seed pods; traditional gastrointestinal stabilizer)"],
        [13, "Hyoscyamus muticus", "Solanaceae", "Egyptian Henbane", "Edwin Smith, Par. 41", "Ground seeds applied to soothe localized severe muscle spasms.", "Scopolamine", "4U15", -7.8, "CN1[C@H]2CC[C@@H]1C[C@@H](C2)OC(=O)[C@H](CO)C3=CC=CC=C3", "HIGH TOXICITY WARNING (Strong anticholinergic; toxic if dosage isn't perfectly micro-calibrated)"],
        [14, "Juniperus phoenicea", "Cupressaceae", "Phoenician Juniper", "Hearst Papyrus, Par. 65", "Resin mixed with fat to expel putrefaction from swelling abscesses.", "Totarol", "3POZ", -8.3, "CC(C)C1=C(C(=C2CCC3C(C2=C1)(CCCC3(C)C)C)O)C", "SAFE (Strong natural topical diterpene antibiotic; avoid highly concentrated raw internal intake)"],
        [15, "Cuminum cyminum", "Apiaceae", "Cumin", "Ebers Papyrus, Par. 45", "Ground with wheat flour and applied to relieve aching, arthritic joints.", "Cuminaldehyde", "3LN1", -6.9, "CC(C)C1=CC=C(C=C1)C=O", "SAFE (Standard carminative culinary spice; anti-inflammatory properties)"]
    ]
    headers = [
        "Plant ID", "Botanical Name", "Family", "Common Name", 
        "Egyptian Text Reference", "English Translation", 
        "Active Phytochemical", "Target Receptor (PDB ID)", 
        "Binding Affinity (kcal/mol)", "SMILES String", "Safety Profile"
    ]
    return pd.DataFrame(raw_data, columns=headers)

df = load_data()

# 4. Sidebar Filter Controls
st.sidebar.header("🔍 Search & Filter Hierarchy")
search_query = st.sidebar.text_input("Search by Plant Name (Common or Scientific)", "")

families = ["All"] + sorted(df["Family"].unique().tolist())
selected_family = st.sidebar.selectbox("Filter by Botanical Family", families)

# Filter processing
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[
        filtered_df["Common Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Botanical Name"].str.contains(search_query, case=False, na=False)
    ]
if selected_family != "All":
    filtered_df = filtered_df[filtered_df["Family"] == selected_family]

# 5. Main Dashboard Display Logic
if filtered_df.empty:
    st.warning("No Egyptian plants match your search criteria.")
else:
    plant_list = filtered_df["Common Name"].tolist()
    selected_plant_name = st.selectbox("Select an Egyptian Plant to Inspect Details:", plant_list)
    plant_row = filtered_df[filtered_df["Common Name"] == selected_plant_name].iloc[0]
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.header("📜 Historical & Botanical Context")
        st.markdown(f"### **{plant_row['Common Name']}**")
        st.markdown(f"*Botanical Name:* **{plant_row['Botanical Name']}**")
        st.markdown(f"*Family:* `{plant_row['Family']}`")
        st.markdown("#### **Ancient Textual Reference**")
        st.info(f"**Source:** {plant_row['Egyptian Text Reference']}")
        st.write(f"**English Translation:** *\"{plant_row['English Translation']}\"*")
        
    with col2:
        st.header("🧬 Molecular Docking & Safety Metrics")
        affinity = plant_row['Binding Affinity (kcal/mol)']
        st.markdown(f"""
            <div class="metric-card">
                <p style='margin:0; font-size:14px; color:#555;'><strong>Binding Affinity (ΔG)</strong></p>
                <h2 style='margin:0; color:#1f385c;'>{affinity} kcal/mol</h2>
                <p style='margin:0; font-size:12px; color:#888;'>Target Receptor (PDB ID): {plant_row['Target Receptor (PDB ID)']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Active Phytochemical Drug Key:** `{plant_row['Active Phytochemical']}`")
        st.markdown(f"**SMILES Chemical Structure Representation:**")
        st.code(plant_row['SMILES String'], language="text")
        
        st.markdown("#### **Toxicological Profile**")
        safety_text = str(plant_row['Safety Profile'])
        if "WARNING" in safety_text.upper() or "TOXIC" in safety_text.upper():
            st.error(safety_text)
        else:
            st.success(safety_text)
            
    st.markdown("---")
    st.header("📋 Global Screening Matrix View")
    st.dataframe(df, use_container_width=True)
  
