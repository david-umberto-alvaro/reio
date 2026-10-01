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
| :--- | :--- | :--- | :--- |
| **REIO-A1** | Ancrage Matériel Pur | `Chain` • `Drive` • `Safe` • `AI` • `NVM` • `BUS` • `PWR` • `Int` • `Uart` | Confinement strict par exclusion d'états intermédiaires. L'IP Core bloque l'erreur sans saturer le processeur hôte. |
| **REIO-A2** | Isolation des Perceptions | `Drive` | Exclusion totale de l'intervention humaine pour prémunir les registres de toute altération malveillante. |
| **REIO-A3** | Convergence Orthogonale | `Chain` | Filtrage matériel en ligne. Rejet immédiat de toute donnée non ancrée aux primitives physiques (Résolution de Gettier). |
| **REIO-A4** | Confinement & Seuils | `Drive` • `Safe` • `NVM` • `Crypt` • `AI` • `BUS` • `PWR` • `Int` • `Uart` | Disjonction physique instantanée dès le franchissement des seuils critiques pour découpler les bus corrompus. |
| **REIO-A5** | Axiomatisation Récursive | `Chain` • `Safe` • `AI` • `CDC` | Élimination mathématique de la métastabilité inter-horloges pour garantir la persistance temporelle. |
| **REIO-A6** | Attestation Pragmatique | `Chain` • `Safe` • `Crypt` • `CDC` • `NVM` • `BUS` • `PWR` • `Int` • `Uart` | Scellement irréversible de chaque cycle d'évolution pour immuniser le SoC contre la gigue et les injections de pannes. |

---

## 🏛️ REIO V4 FRACTAL (Système Monolithique)
👉 **Accéder au dossier de spécification : [REIO V4 Fractal](./fractal)**

La version 4 (Fractal) représente la rupture technologique majeure du framework, centralisant l'intégralité de la sécurité au sein d'un cœur de contrôle unique régi par une logique trivalente formelle.
* **Emplacement :** Répertoire [`/fractal`](./fractal)
* **Statut :** PRODUCTION VALIDÉE (Bitstream durci généré et micro-noyau compilé)
* **Performances Silicium :** Fermeture temporelle stable avec un **WNS de +6,134 ns** sur le domaine synchrone à 100.00 MHz.
* **Ressources & Énergie :** Empreinte ultra-compacte de **12 Slice LUTs / 1 Registre** pour une enveloppe thermique globale maîtrisée à **73 mW** (1 mW dynamique).

---

## 💾 ARCHIVE : REIO V3 (Preuve de Concept Modulaire)
👉 **Architecture périphérique segmentée (11 sous-systèmes autonomes)**

La version 3 constitue la base historique de validation distribuée du SoC. Chaque fonction critique est isolée dans un sous-module matériel indépendant interconnecté via une matrice Crossbar synchrone. Tous les modules ci-dessous sont fonctionnels, temporellement fermés (STA Vivado au vert) et compilent sous Rust en mode `release` :

*   🎛️ **[REIO-PWR](./v3/pwr)** : Séquenceur d'alimentation et gestion des réinitialisations matérielles.
*   🚗 **[REIO-Drive](./v3/drive)** : Interface de contrôle et de filtrage pour bus automobiles.
*   🔒 **[REIO-Safe](./v3/safe)** : Disjoncteur logique de sécurité pour les accès au stockage.
*   🔌 **[REIO-UART](./v3/uart)** : Contrôleur d'I/O série dédié aux tampons de diagnostic.
*   🔑 **[REIO-Crypt](./v3/crypt)** : Accélérateur cryptographique pour calculs arithmétiques intensifs.
*   🌐 **[REIO-Chain](./v3/chain)** : Pipeline de filtrage réseau haute fréquence (250 MHz).
*   🧠 **[REIO-AI](./v3/ai)** : Moniteur d'intégrité et d'analyse comportementale de flux.
*   📶 **[REIO-CDC](./v3/cdc)** : Barrière de synchronisation anti-métastabilité inter-domaines.
*   🚌 **[REIO-BUS](./v3/bus)** : Matrice d'interconnexion Crossbar et décodage système.
*   🚨 **[REIO-INT](./v3/int)** : Écrêteur de requêtes d'interruption et limitation de débit.
*   💾 **[REIO-NVM](./v3/nvm)** : Filtre d'interception et de protection de la mémoire Flash.

## 📦 ARCHIVE : REIO V3 (Preuve de Concept Modulaire)
👉 ** Documentation Technique V3: [REIO V3 Archives](./v3)**

---

### 🌐 Architecture Fonctionnelle du Pipeline

```text
```text
                       [ REIO FRAMEWORK ]
                               |
                               v
                       [   REIO-CORE   ]
                 (Micro-Noyau Rust #![no_std])
                               |
                               v
                       [   REIO-PWR    ] <-------- [ CAPTEURS PHYSIQUES ]
                 (Séquenceur de Reset Synchrone)   (Gel global à 0V en 1 cycle)
                               |
            +------------------+------------------+

            |                  |                  |
            v                  v                  v
     [  REIO-CHAIN  ]   [  REIO-DRIVE  ]   [  REIO-SAFE  ]
      (Filtre Réseau)   (Automotive IO)    (Storage Guard)
       -> 250 MHz         -> 66.67 MHz       -> 100 MHz

            |                  |                  |
            +------------------+------------------+
                               |
                               v [ Lignes IRQ Brutes ]
                       [   REIO-INT    ]
                 (Écrêteur d'IRQ Double Canal)
                               |
                               v [ Lignes IRQ Sécurisées ]
                       [   REIO-CDC    ]
                 (Barrière anti-métastabilité)
                               |
                               v
                       [   REIO-BUS    ] <-------- [   REIO-CRYPT  ]
                  (Matrice Crossbar Sec)     (Accélérateur ZKP DSP)
                               |                  -> 100 MHz
                               v
               [      REIO_IO_SUBSYSTEM     ]
               (Sous-Système d'I/O Fusionné)
               ---> Empreinte : 89 LUTs / 65 Reg
               +---------------------------+

               |  [ CANAL A ]   [ CANAL B ]|
               |   REIO-NVM      REIO-UART |
               |  (Flash Guard) (Diag Logs)|
               +---------------------------+
```

### 🛠️ Plateforme de Crash-Test & Injection de Fautes Globale
- 🧪 **[reio_soc_test.py](./reio_soc_test.py)** : Script d'intégration logicielle hybride (*Hardware-in-the-Loop* émulé). Il orchestre une injection d'attaques en cascade directement sur vos binaires machine Rust bare-metal (`reio_pwr.dll`, `reio_safe.dll`, `reio_uart.dll`, `reio_bus.dll`) pour certifier la disjonction et le confinement matériel immédiat à 0 Volt en cas d'intrusion [image_MgPE5w.png].

![Console de Crash-Test REIO-SoC](./reio_soc_test.png)

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
