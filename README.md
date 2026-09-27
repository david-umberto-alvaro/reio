# REIO — Framework de Co-Design Hardware/Software pour la Sûreté des Systèmes Embarqués

## 🔬 1. Positionnement Scientifique & Sûreté de Fonctionnement

Le framework **REIO** (**Réalisme Expérimental Instrumenté Optimisé**) couple modélisation formelle et contraintes physiques de routage (FPGA). 

* **Réalisme Expérimental :** Validation des concepts logiques face aux contraintes strictes du silicium.
* **Instrumenté :** Certification des métriques réelles (Slacks, primitives, puissance) via les rapports de CAO Vivado.
* **Optimisé :** Densification extrême du circuit et réduction de l'empreinte logique par co-conception assistée.

### 🔬 Fondations Théoriques & Spécifications (Zenodo DOI)

* **REIO-CORE :** Cadre logique formel s'appuyant sur une approche paraconsistante et des machines d'états (FSM) durcies pour garantir un confinement contextuel déterministe malgré les fautes physiques (*bit-flips*). Document de recherche officiel enregistré sous l'identifiant académique permanent : [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20743411.svg)](https://doi.org/10.5281/zenodo.20743411)

### 📐 Cartographie de Co-Design : De la Logique Pure au Silicium

L'infrastructure matérielle implémentée sous Vivado est la traduction physique directe des règles de sûreté formalisées dans ma notice d'architecture :

| Pilier de Sûreté Théorique | Traduction Matérielle (Vivado) | Impact sur la Sûreté Réelle |
| :--- | :--- | :--- |
| **Confinement Paracohérent & Seuils**<br>*(REIO-A4)* | `REIO-Drive` (Ports `safety_status / emergency_trigger`) | Isolation physique instantanée du bus automobile en 1 cycle d'horloge (10 ns) lors d'une injection de fault (`0x7F`) en neutralisant le principe d'explosion. |
| **Ancrage Matériel Pur**<br>*(REIO-A1 & REIO-A2)* | `REIO-Drive` (6 Slice LUTs / Logique de transition pure) | Confinement strict des données corrompues. L'IP Core empêche la propagation de l'erreur sans saturer le processeur hôte par exclusion d'états intermédiaires. |
| **Convergence Orthogonale**<br>*(REIO-A3)* | `REIO-Chain` (Bus synchrone 64 bits cadencé à 400 MHz) | Filtrage matériel pur des paquets réseau. Rejet immédiat de toute donnée non ancrée aux primitives physiques (Résolution des incertitudes de Gettier). |
| **Axiomatisation Récursive**<br>*(REIO-A5 & REIO-A6)* | `REIO-Chain` (Gestion CDC / Marge WNS +1,596 ns) | Élimination mathématique des risques de métastabilité et scellement intègre des cycles d'horloges asynchrones pour la persistance temporelle. |

---

## 🛠 2. Implémentation Physique & Métriques Vivado (PoC)

Deux Proof of Concepts (PoC) en **VHDL** et **Rust/C FFI** ont été synthétisés sur cible **AMD/Xilinx Artix-7**.

- ⛓️ **[REIO-Chain (SPU_103)](./chain)**
  - **Fonction :** Disjoncteur matériel sur bus 64 bits.
  - **Validation :** Cible à 400 MHz (WNS : +1,596 ns, WHS : +0,142 ns).
  - **Ressources :** 12 LUTs / 111 Registres, consommation ~1 mW.

- 🚗 **[REIO-Drive (SPU_105)](./drive)**
  - **Fonction :** Bouclier pour bus d'interception (Couplage Direct Stream 100 MHz).
  - **Architecture de Sûreté :** Conception inspirée des principes de résilience ISO 26262 / ASIL-D (Pattern de redondance matérielle Lockstep et mode Fail-Safe matériel).
  - **Validation :** Validé à 100 MHz (WNS : +7,606 ns, WHS : +0,279 ns). Interception déterministe en 1 cycle.

---

### 🌐 Architecture Globale du Framework

```text
                     [ REIO FRAMEWORK ]
                             |
                             v
        +-----------------------------------------+

        |                REIO-CORE                |
        |    (Spécification Théorique Initiale)   |
        |   -> Archivé sur Zenodo avec son DOI    |
        +-----------------------------------------+
                             |
              +--------------+--------------+

              |                             |
              v                             v
  +-----------------------+     +-----------------------+

  |      REIO-CHAIN       |     |      REIO-DRIVE       |
  |  (PoC Réseau - Impl.) |     |   (PoC Auto - Impl.)  |
  | -> Pipeline 64 bits   |     | -> Interception Direct|
  | -> Cadencement 400 MHz|     | -> Cadencement 100 MHz|
  +-----------------------+     +-----------------------+
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
