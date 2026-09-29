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

| Axiome | Pilier Théorique | Traduction Matérielle (Vivado) | Impact sur la Sûreté Réelle |
| :---: | :--- | :--- | :--- |
| <nobr>**REIO-A1**</nobr> | Ancrage Matériel Pur | `Chain` • `Drive` • `Safe` • `AI` • `NVM` • `BUS` • `PWR` • `Int` | Confinement strict par exclusion d'états intermédiaires. L'IP Core bloque l'erreur sans saturer le processeur hôte. |
| <nobr>**REIO-A2**</nobr> | Isolation des Perceptions | `Drive` | Exclusion totale de l'intervention humaine pour prémunir les registres de toute altération malveillante. |
| <nobr>**REIO-A3**</nobr> | Convergence Orthogonale | `Chain` | Filtrage matériel en ligne. Rejet immédiat de toute donnée non ancrée aux primitives physiques (Résolution de Gettier). |
| <nobr>**REIO-A4**</nobr> | Confinement & Seuils | `Drive` • `Safe` • `NVM` • `Crypt` • `AI` • `BUS` • `PWR` • `Int` | Disjonction physique instantanée dès le franchissement des seuils critiques pour découpler les bus corrompus. |
| <nobr>**REIO-A5**</nobr> | Axiomatisation Récursive | `Chain` • `Safe` • `AI` • `CDC` | Élimination mathématique de la métastabilité inter-horloges pour garantir la persistance temporelle. |
| <nobr>**REIO-A6**</nobr> | Attestation Pragmatique | `Chain` • `Safe` • `Crypt` • `CDC` • `NVM` • `BUS` • `PWR` • `Int` | Scellement irréversible de chaque cycle d'évolution pour immuniser le SoC contre la gigue et les injections de pannes. |

---

## 🛠️ 2. Implémentation Physique & Métriques Vivado (PoC)

Proof of Concepts (PoC) en **VHDL** et **Rust/C FFI** synthétisés sur cible **AMD/Xilinx Artix-7**.

- 🧠 **[REIO-AI](./ai)**
  - **Fonction :** Superviseur logique paracohérent pour la sûreté des accélérateurs IA (NPU/TPU).
  - **Architecture de Sûreté :** Filtre de congruence paraconcurrent bloquant les hallucinations logiques et les injections adverses avec disjonction matérielle et confinement à 0 Volt.
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| WNS : **+6.116 ns** \| WHS : **+0.196 ns**). Isolation et forçage du bus sur le tag de sécurité `0xDEADBEEF` exécutés en exactement **1 cycle d'horloge**.
  - **Ressources :** **52 LUTs / 38 Registres / 0 bloc DSP**, consommation globale ultra-faible de **70 mW** (Dynamique : 1 mW, Statique : 68 mW).

- 🎛️ **[REIO-BUS](./bus)**
  - **Fonction :** Matrice d'interconnexion Crossbar sécurisée et décodeur d'adresse pour l'infrastructure interne du SoC.
  - **Architecture de Sûreté :** Routage géométrique étanche par partitionnement de bus et disjoncteur matériel à effondrement éclair en cas de jeton d'authentification invalide.
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| **WNS : inf** \| **WHS : inf**). Interception de violation, effondrement complet à 0 Volt et levée de l'alarme d'intrusion exécutés en exactement **1 cycle d'horloge (10.00 ns)**.
  - **Ressources :** **38 Slice LUTs / 67 Slice Registers**, consommation globale de **77 mW** (Logique interne active : 6 mW, Fuites statiques et I/O buffers : 71 mW).

- ⛓️ **[REIO-CDC](./cdc)**
  - **Fonction :** Synchroniseur multi-horloge d'étanchéité physique pour le croisement de domaines asynchrones (Clock Domain Crossing).
  - **Architecture de Sûreté :** Chaîne de capture séquentielle à triple étage de bascules durcies pour l'absorption et la neutralisation de la métastabilité active induite par la gigue ou les injections de pannes.
  - **Validation :** Validé au routage inter-domaines (**400 MHz ◄► 100 MHz**). Timing global validé sans aucune violation de setup/hold (`WNS: inf` \| `WHS: inf`). Stabilisation et transmission étanche du signal validées en exactement **3 cycles d'horloge**.
  - **Ressources :** **0 Slice LUT (1 LUT combinatoire d'ajustement de buffer) / 3 Slice Registers**, consommation globale de **336 mW** (Logique interne active : 7 mW, Fuites passives et I/O buffers : 329 mW).

- ⛓️ **[REIO-Chain](./chain)**
  - **Fonction :** Disjoncteur réseau Layer 3 synchrone sur bus 64 bits s'interfaçant avec un bus physique Ethernet.
  - **Validation :** Validé à **400.00 MHz** (Période : **2.50 ns** \| **WNS : +0,531 ns** \| **WHS : +0,142 ns**). Coupure réseau déterministe et masquage de transaction exécutés en exactement **1 seul cycle machine**.
  - **Ressources :** **53 Slice LUTs / 153 Slice Registers**, consommation globale de **59 mW** (Logique interne active : 3 mW, Fuites statiques passives : 56 mW).

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

* 💾 **[REIO-NVM](./nvm)**
  * **Fonction :** Filtre d'interception en ligne pour la sécurisation des mémoires non-volatiles (MRAM / RRAM).
  * **Architecture de Sûreté :** Analyse combinatoire continue de la congruence des flux d'écriture pour bloquer instantanément les dérives de charge physique et les injections de fautes.
  * **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| WNS : **inf** \| WHS : **inf**). Interception de motif de sabotage, mise à la masse de sécurité à 0 Volt et levée du signal d'alerte physique exécutées en exactement **1 seul cycle d'horloge (10.00 ns)**.
  * **Ressources :** **33 Slice LUTs / 33 Slice Registers**, consommation globale de **336 mW** (Logique interne active : 1 mW, Fuites statiques et I/O buffers : 335 mW).

- 🔋 **[REIO-PWR](./pwr)**
  - **Fonction :** Gestionnaire d'énergie et contrôleur de séquence de Reset ordonné pour l'infrastructure vitale du SoC.
  - **Architecture de Sûreté :** Automate de Power-On-Reset asymétrique avec détection de glitch de tension et gel instantané de l'exécution globale du silicium pour empêcher la corruption d'état.
  - **Validation :** Validé à **100.00 MHz** (Période : **10.00 ns** \| **WNS : +7,259 ns** \| **WHS : +0,212 ns**). Interception de baisse d'alimentation, effondrement des lignes de réveil et levée de l'alarme exécutés en exactement **1 seul cycle d'horloge (10.00 ns)**.
  - **Ressources :** **14 Slice LUTs / 10 Slice Registers**, consommation globale de **71 mW** (Logique interne active : 1 mW, Fuites statiques passives : 70 mW).

---

### 🌐 Architecture Fonctionnelle du Pipeline

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
                             v
           +-----------------------------------+

           |             REIO-PWR              |
           |   [ GESTIONNAIRE D'ÉNERGIE ]      | <--- [ Capteurs VCCINT / VCCAUX ]
           |  Séquenceur de Reset Asymétrique  |      (Gel global à 0V en 1 cycle)
           +-----------------------------------+
                             |
         +-------------------+-------------------+

         | [Palier 1]        | [Palier 2]        | [Palier 3]
         | RSTn_INTERCONN    | RSTn_PERIPH       | RSTn_COPROC
         v                   v                   v
+-----------------+ +-----------------+ +-----------------+ +-----------------+

|   REIO-CHAIN    | |   REIO-DRIVE    | |    REIO-SAFE    | |    REIO-NVM     |
|  (PoC Réseau)   | |   (PoC Auto)    | |   (PoC Flash)   | |   (PoC Mag/R)   |
|   -> 400 MHz    | |  -> 66.67 MHz   | |   -> 100 MHz    | |   -> 100 MHz    |
+-----------------+ +-----------------+ +-----------------+ +-----------------+

         |                   |                   |                   |
         | [Asynchrone]      | [Asynchrone]      | [Synchrone]       | [Synchrone]
         v                   v                   |                   |
+-------------------------------------+          |                   |

|              REIO-CDC               |          |                   |
| ----------------------------------- |          |                   |
|  - [Canal 1] 400 MHz -> 100 MHz     |          |                   |
|  - [Canal 2] 66.67 MHz -> 100 MHz   |          |                   |
+-------------------------------------+          |                   |

         |                   |                   |                   |
         +---------+---------+-------------------+-------------------+
                   |
                   v
+---------------------------------------------------------------------------+

|                                 REIO-BUS                                  |
|                 [ BUS SYSTEME UNIFIE ETANCHE : 100 MHz ]                  |
|  - Matrice Crossbar Sécurisée (Authentification par Jeton Matériel)       |
|  - Routage Géographique & Commutation de Zone Périphérique                |
+---------------------------------------------------------------------------+
                   |
                   +-------------------------+

                   |                         |
                   v                         v
        +---------------------+   +---------------------+

        |     REIO-CRYPT      |   |       REIO-AI       |
        |    (PoC Crypto)     |   |      (PoC IA)       |
        |     -> 100 MHz      |   |     -> 100 MHz      |
        +---------------------+   +---------------------+
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
