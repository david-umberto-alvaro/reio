# 🔑 REIO-Crypt — Accélérateur Cryptographique Hétérogène Découplé

REIO-Crypt est un coprocesseur arithmétique matériel dédié à la génération de preuves à divulgation nulle de connaissance (Zero-Knowledge Proofs - ZKP) et au durcissement de clés sur courbes elliptiques (ECC).

### 🔬 Architecture Logique & Primitives Câblées

L'architecture s'appuie sur le Modèle Hétérogène Découplé (AHD) pour isoler le traitement arithmétique lourd du processeur hôte :
* **Matrice de Calcul :** **100 LUTs** logiques et **5 macro-blocs** de calcul arithmétique matériel `DSP48E1` hautement optimisés.
* **Pipeline Temporel :** **135 registres** synchrones de type `FDCE` cadencés sur un triple pipeline intermédiaire avec isolation d'arbre.
* **Broche d'Immunité Physique :** Ligne d'alerte active `VOLTAGE_GLITCH_DETECT` couplée au forçage asynchrone à 0 Volt pour contrer les injections de pannes.

### 🔬 Performances Matérielles Certifiées (AMD/Xilinx Vivado v2026.1)

Les rapports d'implémentation post-routage sur cible Artix-7 certifient les métriques physiques réelles issues de vos nouveaux rapports :

- **Fréquence Horloge Système :** Validée à **100.00 MHz** (Période de **10.00 ns**) [https://github.com/david-umberto-alvaro/reio/blob/main/crypt/reio_crypt_timing_summary_routed.rpt].
- **Worst Negative Slack (WNS) :** Fermé à **+1,158 ns** (0 Failing Endpoints) [https://github.com/david-umberto-alvaro/reio/blob/main/crypt/reio_crypt_timing_summary_routed.rpt].
- **Worst Hold Slack (WHS) :** Optimisé à **+0.196 ns** [https://github.com/david-umberto-alvaro/reio/blob/main/crypt/reio_crypt_timing_summary_routed.rpt].

### 📊 Empreinte Géométrique & Signature Thermique

- **Ressources Silicium :** **100 Slice LUTs** (0.48%), **135 Slice Registers** (0.32%), et **5 blocs DSP48E1** (5.56%) [https://github.com/david-umberto-alvaro/reio/blob/main/crypt/reio_crypt_utilization_synth.rpt].
- **Puissance Électrique Totale :** Enveloppe thermique mesurée post-routage à **81 mW** (Statique : 70 mW, Dynamique : 11 mW) [https://github.com/david-umberto-alvaro/reio/blob/main/crypt/reio_crypt_power_routed.rpt].
- **I/O Physiques :** Configuration de **69 broches physiques** (36 `IBUF`, 33 `OBUF`) [https://github.com/david-umberto-alvaro/reio/blob/main/crypt/reio_crypt_utilization_synth.rpt].

### 🌐 Architecture Fonctionnelle du Pipeline

```text
+--------------------------------------------------------+

|                    APPLICATION HÔTE                    |
|             (Interface d'Évaluation Python)            |
+--------------------------------------------------------+
                           |
                           | Liaison Directe (C-FFI Bridge)
                           v
+--------------------------------------------------------+

|                 PILOTE DE CONTRÔLE RUST                |
|   Configuration MMIO & Registres Alignés (#![no_std])  |
+--------------------------------------------------------+
                           |
                           | Lecture Volatile du Jeton ZK (Bus AMBA APB)
                           v
+========================================================+

|                        SILICIUM                        |
| ------------------------------------------------------ |
|               COPROCESSEUR MATÉRIEL VHDL               |
|     Modèle Hétérogène Découplé & Pipeline 3 Étages     |
|                                                        |
|      [100 Optimized Slice LUTs]  [135 Registers]       |
|      [5 Blocs DSP48E1 Câblés]    [16-Cycle Processing] |
+========================================================+
                           ^
                           | Interception Ultra-Rapide (Sub-nanoseconde)
                           | [ LIGNE VOLTAGE_GLITCH_DETECT ]
```

### 📊 Validation Fonctionnelle & Formes d'Ondes (Testbench RTL)

![Chronogramme des formes d'ondes REIO-Crypt](reio_crypt_simulation.png)

### 🛠️ Architecture du Framework Unifié

1. **RTL Core (VHDL) :** Double fichier unifiant le wrapper de bus esclave AMBA APB 32 bits et le cœur arithmétique polynomial pipeliné.
2. **Control Plane (Rust 2024) :** Pilote de bas niveau en `#![no_std]` avec structures MMIO alignées et gestionnaire de panique autonome bloquant.
3. **Host Interface (C-FFI) :** Pont FFI universel exportant la primitive `verifier_jeton_zk` vers l'application hôte.

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)

L'exécution de la suite de tests unitaires certifie la parfaite résilience du plan de contrôle et l'interception instantanée des comportements asymétriques :

*   **Test 1 (Flux Standard) :** Traitement nominal validé avec génération du Hash de confiance scellé par le pipeline (`0xa508bf53`).
*   **Test 2 (Injection Glitch) :** Simulation d'une injection de panne matérielle contrée par une isolation active avec mise à la masse immédiate du bus à 0V.
*   **Test 3 (Erreur Pointeur) :** Robustesse du code face au passage d'une adresse NULL interceptée de manière bloquante pour empêcher toute fuite mémoire.

![Rapport de validation du pilote REIO-Crypt](reio_crypt_test.png)
