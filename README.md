# REIO — Framework de Co-Design Hardware/Software pour la Sûreté des Systèmes Embarqués

## 🔬 1. Positionnement Scientifique & Sûreté de Fonctionnement

Le framework **REIO** (**Réalisme Expérimental Instrumenté Optimisé**) couple modélisation formelle et contraintes physiques de routage (FPGA). 

* **Réalisme Expérimental :** Validation des concepts logiques face aux contraintes strictes du silicium.
* **Instrumenté :** Certification des métriques réelles (Slacks, primitives, puissance) via les rapports de CAO Vivado.
* **Optimisé :** Maximisation de l'exécution informatique par une double formulation systématique (interprétation sémantique et formalisation en logique symbolique pure) éliminant les indéterminations logiques.

### 🔬 Fondations Théoriques & Spécifications (Zenodo DOI)

* **REIO-CORE :** Cadre logique formel s'appuyant sur une approche logique paraconsistante et des machines d'états (FSM) durcies pour garantir un confinement contextuel déterministe malgré les fautes physiques (*bit-flips*). Document de recherche officiel enregistré sous l'identifiant académique permanent : [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20743411.svg)](https://doi.org/10.5281/zenodo.20743411)

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
## 🎯 Présentation du Projet REIO (Réalisme Expérimental Instrumenté Optimisé)

**REIO** est un framework d'architecture matérielle sécurisée conçu pour immuniser les systèmes embarqués critiques (comme l'automobile ou l'aérospatial) contre les cyberattaques et les injections de pannes physiques. 

Le projet retrace l'évolution technologique d'un framework d'intégrité embarqué à travers deux générations majeures :
1. 📦 [**Génération V3 (Archive)**](./v3/README.md) : Une approche modulaire composée de 11 périphériques fragmentés qui surveillaient le système de manière distribuée.
2. 🏛️ [**Génération V4 (Production)**](./v4/README.md) : Une rupture technologique majeure qui centralise toute la sécurité au sein d'un cœur de contrôle unique et monolithique. Ce cœur de contrôle est régi par une logique mathématique trivalente formelle, capable de détecter et de confiner une anomalie en moins d'un cycle d'horloge.

## 🏛️ [REIO V4 (Système Monolithique)](./v4/README.md)

Cette quatrième génération concrétise la convergence matérielle et logicielle du framework, garantissant un confinement d'anomalie ultra-déterministe sans le moindre compromis sur les performances physiques de la puce.

*   **Statut du Jalon :** **PRODUCTION VALIDÉE** 🚀 (Bitstream matériel câblé généré et micro-noyau OS compilé en Rust bare-metal).
*   **Performances Silicium :** Fermeture temporelle d'élite avec un **WNS de +8,936 ns** sur le domaine synchrone d'usine à 100.00 MHz (Chemin critique de 1,064 ns).
*   **Ressources & Énergie :** Empreinte ultra-compacte de seulement **7 Slice LUTs** et **6 Registres (FF)** pour une enveloppe thermique globale maîtrisée à **76 mW** (2 mW dynamique).


### 🧠 Aperçu de la Boucle d'Exécution Monolithique V4

```text
                 +--------------------------------+

                 |       POINT D'ENTRÉE RUST      |
                 |          fn _start()           |
                 +--------------------------------+
                                 |
                                 v
                 +--------------------------------+

                 |    Initialisation Statique     |
                 | (Network, Drive, Storage = +1) |
                 +--------------------------------+
                                 |
                                 v
                     //--- BOUCLE PRINCIPALE ---//
+---------> +------------------------------------------+

|           |  PHASE 1 : Lecture Volatile BASE_BUS     |
|           |          (0x4000_5000)                   |
|           +------------------------------------------+

|                                |
|                                v
|                 /----------------------------\
|                /   Bit d'anomalie détecté     \
|                \      par le silicium ?       /
|                 \----------------------------/
|                     /                    \
|           [OUI]    /                      \ [NON]
|                   v                        v
|     +---------------------------+    +---------------------------+

|     | PHASE 2 : CONFINEMENT     |    | PHASE 3 : PLANIFICATEUR   |
|     | - Net/Drive state = 0     |    | - Exécution Net   (Si +1) |
|     | - Écrasement BUS à 0 Volt |    | - Exécution Drive (Si +1) |
|     +---------------------------+    | - Exécution Store (Si +1) |
|                   |                  +---------------------------+
|                   v                                |
+-------------------+--------------------------------+
```

---

## 💾 ARCHIVE : [REIO V3](./v3/README.md) (Preuve de Concept Modulaire)
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
