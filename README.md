# REIO — Framework de Co-Design Hardware/Software pour la Sûreté des Systèmes Embarqués

## 🔬 1. Positionnement Scientifique & Sûreté de Fonctionnement

Le framework **REIO** (**Réalisme Expérimental Instrumenté Optimisé**) couple modélisation formelle et contraintes physiques de routage (FPGA). 

* **Réalisme Expérimental :** Validation des concepts logiques face aux contraintes strictes du silicium.
* **Instrumenté :** Certification des métriques réelles (Slacks, primitives, puissance) via les rapports de CAO Vivado.
* **Optimisé :** Maximisation de l'exécution informatique par une double formulation systématique (interprétation sémantique et formalisation en logique symbolique pure) éliminant les indéterminations logiques.

### 🔬 Fondations Théoriques & Spécifications (Zenodo DOI)

* **REIO-CORE :** Cadre logique formel s'appuyant sur une approche logique paraconsistante et des machines d'états (FSM) durcies pour garantir un confinement contextuel déterministe malgré les fautes physiques (*bit-flips*). Document de recherche officiel enregistré sous l'identifiant académique permanent : [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20743411.svg)](https://doi.org/10.5281/zenodo.20743411)

### 📐 Cartographie de Co-Design : De la Logique Pure au Silicium

L'infrastructure matérielle implémentée sous Vivado est la traduction physique directe des règles de sûreté formalisées dans la notice d'architecture :

### 📐 Cartographie de Co-Design : De la Logique Pure au Silicium

L'infrastructure matérielle implémentée sous Vivado est la traduction physique directe des règles de sûreté formalisées dans la notice d'architecture :

| Axiome | Pilier de Sûreté Théorique | Traduction Matérielle (Vivado) | Impact sur la Sûreté Réelle |
| :--- | :--- | :--- | :--- |
| **REIO&#8209;A1** | Ancrage Matériel Pur | **REIO-Drive** (6 Slice LUTs / Logique de transition pure)<br><br>**REIO-Safe** (28 Slice LUTs / Isolation géométrique SPU-102) | Confinement strict des données corrompues. L'IP Core empêche la propagation de l'erreur sans saturer le processeur hôte par exclusion d'états intermédiaires. |
| **REIO&#8209;A2** | Isolation des Perceptions | **REIO-Drive** (Génération des prémisses par capteurs indexés) | Exclusion totale de l'intervention humaine directe pour prémunir les registres de toute altération malveillante ou asymétrique. |
| **REIO&#8209;A3** | Convergence Orthogonale | **REIO-Chain** (Bus réseau synchrone cadencé à 125 MHz / 400 MHz) | Filtrage matériel des paquets réseau. Rejet immédiat de toute donnée non ancrée aux primitives physiques (Résolution des incertitudes de Gettier). |
| **REIO&#8209;A4** | Confinement Paracohérent & Seuils | **REIO-Drive** (Ports `security_status` / `emergency_trigger`) <br><br>**REIO-Safe** (Seuil critique de 16 écritures)<br><br>**REIO-Crypt** (Ligne d'immunité active à 9.5 ns) | Isolation physique instantanée :<br>- Bus automobile en 3 cycles (45.00 ns à 66.67 MHz).<br>- Bus de stockage Flash à 0 Volt en 1 cycle d'horloge (10.00 ns à 100 MHz).<br>- Coprocesseur crypto mis à la masse sous 9.50 ns. |
| **REIO&#8209;A5** | Axiomatisation Récursive Dynamique | **REIO-Chain** (Marge WNS +1.596 ns)<br><br>**REIO-Safe** (Arbre synchrone pin F4 / Marge WNS +5.222 ns) | Élimination mathématique des risques de métastabilité et scellement intègre des cycles d'horloges asynchrones pour la persistance temporelle. |
| **REIO&#8209;A6** | Attestation Pragmatique Cryptographique | **REIO-Chain** (Preuve ZK Réseau)<br><br>**REIO-Safe** (Tag volatil `0xDEADBEEF`) <br><br>**REIO-Crypt** (Pipeline synchrone 16 cycles / Hash `0xA508BF53`) | Scellement irréversible de chaque cycle d'évolution du protocole pour préserver l'invariance des structures au sein des environnements cyber-physiques. |


---

## 🛠️ 2. Implémentation Physique & Métriques Vivado (PoC)

Proof of Concepts (PoC) en **VHDL** et **Rust/C FFI** synthétisés sur cible **AMD/Xilinx Artix-7**.

- ⛓️ **[REIO-Chain (SPU_103)](./chain)**
  - **Fonction :** Disjoncteur matériel sur bus 64 bits.
  - **Validation :** Cible à **400 MHz** (WNS : **+1,596 ns**, WHS : **+0,142 ns**).
  - **Ressources :** **12 LUTs / 111 Registres**, consommation **~1 mW**.

- 🔑 **[REIO-Crypt (SPU_106)](./crypt)**
  - **Fonction :** Accélérateur cryptographique découplé matériel pour preuve Zero-Knowledge (ZKP).
  - **Architecture de Sûreté :** Modèle Hétérogène Découplé (AHD) avec pipeline synchrone à deux étages (brise le chemin critique d'arithmétique non-linéaire) et capteur de détection de glitch de tension.
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| WNS : **+0.345 ns** \| WHS : **+0.106 ns**). Preuve calculée en 16 cycles d'horloge et disjonction par mise à la masse immédiate en cas d'attaque par injection.
  - **Ressources :** **169 LUTs / 139 Registres / 3 Blocs DSP48E1**, consommation globale ultra-faible de **75 mW** (Dynamique : 3 mW, Statique : 72 mW).

- 🚗 **[REIO-Drive (SPU_105)](./drive)**
  - **Fonction :** Bouclier pour bus d'interception (Couplage Direct Stream).
  - **Architecture de Sûreté :** Conception inspirée des principes de résilience ISO 26262 / ASIL-D (Pattern d'interception combinatoire durcie avec compteur de stabilisation et mode Fail-Safe matériel).
  - **Validation :** Validé à **66.67 MHz** (Période : **15.00 ns** \| WNS : **+1.039 ns** \| WHS : **+0.279 ns**). Interception et isolation physique du bus automobile exécutées de manière déterministe en **3 cycles d'horloge (45.00 ns)**.
  - **Ressources :** **6 LUTs / 4 Registres**, consommation active inférieure à **1 mW** (Statique : 72 mW).

- 🛡️ **[REIO-Safe (SPU_102)](./safe)**
  - **Fonction :** Filtre combinatoire d'interception matériel anti-ransomware de stockage.
  - **Architecture de Sûreté :** Double canal parallèle (Analyse géométrique via Registre Alpha et suivi entropique asymétrique filtré contre le bruit avec seuil critique). 
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| WNS : **+5.222 ns** \| WHS : **+0.222 ns**). Coupure électrique nette de l'alimentation d'écriture à **0 Volt** et injection du tag de quarantaine exécutées en **1 seul cycle d'horloge (10.00 ns)**.
  - **Ressources :** **28 LUTs / 20 Registres**, consommation globale **92 mW** (Statique : 72 mW, Dynamique : 20 mW).

---

### 🌐 Architecture Globale du Framework

```text
               [ REIO FRAMEWORK ]
                       |
                       v
     +-----------------------------------+

     |                                   |
     |             REIO-CORE             |
     |  (Spécification Théorique Init.)  |
     |  -> Archivé sur Zenodo avec DOI   |
     |                                   |
     +-----------------------------------+
                       |
         +-------------+-------------+

         |             |             |
         v             v             v
  +-------------+ +-------------+ +-------------+

  |             | |             | |             |
  |  REIO-CHAIN | |  REIO-DRIVE | |  REIO-SAFE  |
  | (PoC Réseau)| |  (PoC Auto) | | (PoC Stock.)|
  | -> Pipeline | | -> Intercept| | -> SPU-102  |
  |   64 bits   | |   Direct    | |  Synchrone  |
  | -> 400 MHz  | | -> 66.67MHz | | -> 100 MHz  |
  |             | |             | |             |
  +-------------+ +-------------+ +-------------+
```


## 📦 3. Structure du Dépôt & Politique d'Accès

Ce dépôt sert de portfolio technique pour démontrer mes compétences en co-design et en intégration matérielle.

### Accès Libre (Modèle Open-Core) :
*   **Documentation & Méthodologie :** Fichiers textuels d'analyse (`.md`).
*   **Interfaces de Liaison :** Fichiers d'en-tête standardisés (`.h`) pour l'intégration logicielle.
*   **Rapports de Synthèse :** Journaux physiques Vivado (`.rpt`) certifiant l'utilisation des ressources logiques, de puissance et le timing post-routage.

## ⚖ Licence & Propriété Intellectuelle

Ce framework est distribué sous un modèle Open-Core strict. Pour consulter l'accord d'audit public et les restrictions de rétro-ingénierie, veuillez vous référer au fichier [LICENSE.md](./LICENSE.md).

---

💼 **Besoin d'intégrer REIO sur vos architectures FPGA ou calculateurs critiques ?**
Pour toute demande d'évaluation du code source complet, d'adaptation d'architecture sur mesure ou de consultation industrielle, l'accès peut être accordé après signature d'un Accord de Confidentialité (NDA). Veuillez soumettre une demande officielle via mon **[Profil LinkedIn](https://www.linkedin.com/in/david-umberto-alvaro-715841399/)**.
