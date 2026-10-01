# 🏛️ REIO V4 — Cœur de Contrôle Monolithique (CPU)

Cette section héberge les rapports de certification physique et d'implémentation du microprocesseur durci **REIO V4**, conçu pour assurer un confinement d'anomalie ultra-déterministe au sein d'architectures embarquées critiques.

## 📊 Bulletins de Certification Métrologique (Vivado Post-Routage)

Les rapports officiels générés par AMD/Xilinx Vivado v2026.1 valident les performances physiques et temporelles du processeur sur cible automobile **xa7a35tcsg324-1Q** :

*   🔬 [**Rapport d'Utilisation des Ressources (.rpt)**](./reio_v4_utilization.rpt) : Certifie une empreinte microscopique de seulement **7 Slice LUTs** et **6 Registres (FF)** (soit 0,03% du silicium), garantissant un coût d'intégration nul.
*   ⏱️ [**Rapport de Clôture Temporelle (.rpt)**](./reio_v4_timing.rpt) : Valide un Worst Negative Slack (**WNS**) d'élite à **+8,936 ns** (chemin critique combinatoire de **1,035 ns**). Le cœur est nativement capable d'absorber une fréquence d'horloge supérieure à **850 MHz**.
*   🔋 [**Rapport d'Enveloppe Énergétique (.rpt)**](./reio_v4_power.rpt) : Valide une dissipation globale contenue à **76 mW**, dont seulement **2 mW** de consommation dynamique en commutation active.

## 🧠 Spécifications et Possibilités du Cœur V4

Le processeur REIO V4 se distingue des cœurs de calcul traditionnels par ses propriétés matérielles exclusives :

1.  **Logique Trivalente Native :** Capacité à interpréter et traiter trois états logiques distincts afin de détecter instantanément les indéterminations ou corruptions sur les bus internes.
2.  **Surveillance MMIO Synchrone :** Interrogation déterministe et cyclique à **100 MHz** de l'adresse de frontière matérielle **`0x4000_5000`**.
3.  **Disjonction Matérielle Éclair :** Déroutement immédiat du pointeur de programme en moins d'un cycle d'horloge pour écraser le bus maître à **0 Volt** dès la détection d'une anomalie ou d'un glitch d'instruction.

## ⚙️ Co-Simulation Matérielle / Logicielle (HW/SW)

Le cœur d'exécution intègre une mémoire ROM interne de démarrage (BRAM) pré-initialisée à l'aide de la matrice hexadécimale textuelle issue de la compilation de son micro-noyau applicatif codé en **Rust bare-metal** (`no_std`). 
L'évaluation comportementale mixte sous le moteur **XSim** certifie un fonctionnement synchrone et un confinement validé au vert fixe (`exit 0`).

---
*Classification : Document d'Évaluation Technique - Code Source Propriétaire (Non publié pour préservation du Secret Industriel).*
