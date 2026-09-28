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

| Axiome | Pilier de Sûreté Théorique | Traduction Matérielle (Vivado) | Impact sur la Sûreté Réelle |
| :--- | :--- | :--- | :--- |
| **REIO-A1** | Ancrage Matériel Pur | - **REIO-Drive** (6 Slice LUTs / Logique de transition pure)<br>- **REIO-Safe** (28 Slice LUTs / Isolation géométrique)<br>- **REIO-AI** (52 Slice LUTs / Filtre paraconcurrent) | Confinement strict des données corrompues. L'IP Core empêche la propagation de l'erreur sans saturer le processeur hôte par exclusion d'états intermédiaires. |
| **REIO-A2** | Isolation des Perceptions | - **REIO-Drive** (Génération des prémisses par capteurs indexés) | Exclusion totale de l'intervention humaine directe pour prémunir les registres de toute altération malveillante ou asymétrique. |
| **REIO-A3** | Convergence Orthogonale | - **REIO-Chain** (Bus réseau synchrone cadencé à 125 MHz / 400 MHz) | Filtrage matériel des paquets réseau. Rejet immédiat de toute donnée non ancrée aux primitives physiques (La résolution des incertitudes de Gettier). |
| **REIO-A4** | Confinement Paracohérent & Seuils | - **REIO-Drive** (Ports `security_status` / `emergency_trigger`) <br>- **REIO-Safe** (Seuil critique de 16 écritures)<br>- **REIO-Crypt** (Ligne d'immunité active à 9.5 ns)<br>- **REIO-AI** (Rupture instantanée en 1 cycle horloge) | Isolation physique instantanée :<br>- Bus automobile en 3 cycles (45.00 ns à 66.67 MHz).<br>- Bus de stockage Flash à 0 Volt en 1 cycle d'horloge (10.00 ns à 100 MHz).<br>- Coprocesseur crypto mis à la masse sous 9.50 ns.<br>- Superviseur IA activant la disjonction NPU en 10.00 ns. |
| **REIO-A5** | Axiomatisation Récursive Dynamique | - **REIO-Chain** (Marge WNS +1.596 ns)<br>- **REIO-Safe** (Arbre synchrone pin F4 / Marge WNS +5.222 ns)<br>- **REIO-AI** (Marge WNS exceptionnelle de +6.116 ns)<br>- **REIO-CDC** (Bascules `ASYNC_REG` contiguës) | Élimination mathématique des risques de métastabilité inter-horloges et scellement intègre des cycles d'horloges asynchrones pour la persistance temporelle. |
| **REIO-A6** | Attestation Pragmatique Cryptographique | - **REIO-Chain** (Preuve ZK Réseau)<br>- **REIO-Safe** (Tag volatil `0xDEADBEEF`) <br>- **REIO-Crypt** (Pipeline 16 cycles / Hash `0xA508BF53`) <br>- **REIO-CDC** (Stabilisation stricte en 3 cycles) | Isolation asynchrone étanche protégeant le transfert des primitives physiques et jetons de sûreté contre la gigue et les injections de pannes. |

---

## 🛠️ 2. Implémentation Physique & Métriques Vivado (PoC)

Proof of Concepts (PoC) en **VHDL** et **Rust/C FFI** synthétisés sur cible **AMD/Xilinx Artix-7**.

- 🧠 **[REIO-AI](./ai)**
  - **Fonction :** Superviseur logique paracohérent pour la sûreté des accélérateurs IA (NPU/TPU).
  - **Architecture de Sûreté :** Filtre de congruence paraconcurrent bloquant les hallucinations logiques et les injections adverses avec disjonction matérielle et confinement à 0 Volt.
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| WNS : **+6.116 ns** \| WHS : **+0.196 ns**). Isolation et forçage du bus sur le tag de sécurité `0xDEADBEEF` exécutés en exactement **1 cycle d'horloge**.
  - **Ressources :** **52 LUTs / 38 Registres / 0 bloc DSP**, consommation globale ultra-faible de **70 mW** (Dynamique : 1 mW, Statique : 68 mW).

- ⛓️ **[REIO-CDC](./cdc)**
  - **Fonction :** Synchroniseur multi-horloge d'étanchéité physique pour le croisement de domaines asynchrones (Clock Domain Crossing).
  - **Architecture de Sûreté :** Chaîne de capture séquentielle à triple étage de bascules durcies pour l'absorption et la neutralisation de la métastabilité active induite par la gigue ou les injections de pannes.
  - **Validation :** Validé au routage inter-domaines (**400 MHz ◄► 100 MHz**). Timing global validé sans aucune violation de setup/hold (`WNS: inf` \| `WHS: inf`). Stabilisation et transmission étanche du signal validées en exactement **3 cycles d'horloge**.
  - **Ressources :** **0 Slice LUT (1 LUT combinatoire d'ajustement de buffer) / 3 Slice Registers**, consommation globale de **336 mW** (Logique interne active : 7 mW, Fuites passives et I/O buffers : 329 mW).

- ⛓️ **[REIO-Chain](./chain)**
  - **Fonction :** Disjoncteur matériel sur bus 64 bits.
  - **Validation :** Cible à **400 MHz** (WNS : **+1,596 ns**, WHS : **+0,142 ns**).
  - **Ressources :** **12 LUTs / 111 Registres**, consommation **~1 mW**.

- 🔑 **[REIO-Crypt](./crypt)**
  - **Fonction :** Accélérateur cryptographique découplé matériel pour preuve Zero-Knowledge (ZKP).
  - **Architecture de Sûreté :** Modèle Hétérogène Découplé (AHD) avec pipeline synchrone à deux étages (brise le chemin critique d'arithmétique non-linéaire) et capteur de détection de glitch de tension.
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| WNS : **+0.345 ns** \| WHS : **+0.106 ns**). Preuve calculée en 16 cycles d'horloge et disjonction par mise à la masse immédiate en cas d'attaque par injection.
  - **Ressources :** **169 LUTs / 139 Registres / 3 Blocs DSP48E1**, consommation globale ultra-faible de **75 mW** (Dynamique : 3 mW, Statique : 72 mW).

- 🚗 **[REIO-Drive](./drive)**
  - **Fonction :** Bouclier pour bus d'interception (Couplage Direct Stream).
  - **Architecture de Sûreté :** Conception inspirée des principes de résilience ISO 26262 / ASIL-D (Pattern d'interception combinatoire durcie avec compteur de stabilisation et mode Fail-Safe matériel).
  - **Validation :** Validé à **66.67 MHz** (Période : **15.00 ns** \| WNS : **+1.039 ns** \| WHS : **+0.279 ns**). Interception et isolation physique du bus automobile exécutées de manière déterministe en **3 cycles d'horloge (45.00 ns)**.
  - **Ressources :** **6 LUTs / 4 Registres**, consommation active inférieure à **1 mW** (Statique : 72 mW).

- 🛡️ **[REIO-Safe](./safe)**
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
           +-----------------------------------+
                             |
         +-------------+-----+-------------+

         |             |                   |
         v             v                   v
  +-------------+ +-------------+     +-------------+

  |             | |             |     |             |
  |  REIO-CHAIN | |  REIO-DRIVE |     |  REIO-SAFE  |
  | (PoC Réseau)| |  (PoC Auto) |     | (PoC Stock.)|
  | -> 400 MHz  | | -> 66.67MHz |     | -> 100 MHz  |
  +-------------+ +-------------+     +-------------+

         |               |                   |
         v               |                   |
  +-------------+        |                   |

  |  REIO-CDC   |        |                   |
  | (Pont Clock)|        |                   |
  |  3 Registers|        |                   |
  | -> 3 Cycles |        |                   |
  +-------------+        |                   |

         |               |                   |
         +---------------+-------------------+
                         |
               +---------+---------+

               |                   |
               v                   v
        +-------------+     +-------------+

        |             |     |             |
        |  REIO-CRYPT |     |   REIO-AI   |
        | (PoC Crypto)|     |   (PoC IA)  |
        | -> 100 MHz  |     | -> 100 MHz  |
        +-------------+     +-------------+

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
