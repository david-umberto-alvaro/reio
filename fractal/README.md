# REIO V4 — SYSTÈME MONOLITHIQUE SECURE

## 🏛️ Spécification Technique et Registre d'Attestation Matérielle

Ce répertoire centralise les bulletins métrologiques et les preuves d'implémentation physique de l'architecture REIO V4. L'intégralité du code source RTL (VHDL) et du firmware applicatif (Rust Bare-Metal `#![no_std]`) est conservée exclusivement sur un environnement local sécurisé hors-ligne.

### 🔬 Architecture Matérielle V4
La version 4 consolide l'infrastructure autour d'un cœur de contrôle unique et d'un décodeur d'interception à logique trivalente, éliminant la fragmentation des anciens modules périphériques.
*   **Canal Arithmétique Actif :** Routage haute vitesse sur blocs DSP48E1 pour le traitement des opérations intensives.
*   **Canal de Rétention Synchrone :** Alignement temporel sur bascules FDCE avec barrières anti-métastabilité pour sécuriser les changements de phase.
*   **Écrêtage Combinatoire Périphérique :** Interception sub-nanoseconde des fluctuations de tension et dérivation immédiate du signal vers le plan de masse (GND, 0V) via le module `reio_l3_decoder`.

### 📊 Indicateurs de Performance Silicium (AMD/Xilinx Vivado v2026.1)
L'évaluation post-routage sur cible Artix-7 Automotive Extended (`xa7a35tcsg324-1Q`) certifie les métriques réelles suivantes :

*   **Fermeture Temporelle (STA) :** **Worst Negative Slack (WNS) stable à +7,517 ns** (0 Failing Endpoints) sur le domaine synchrone à 100.00 MHz. Worst Hold Slack (WHS) mesuré à **+0,880 ns**.
*   **Surface Logique (Utilization) :** L'interception monolithique ne consomme que **12 Slice LUTs** (0,06 % du composant) et **1 unique registre (FF)**, attestant de la suppression totale de la fragmentation et du LUT combining.
*   **Bilan Électrique (Power) :** Enveloppe thermique consolidée à **73 mW** (72 mW de fuites statiques inhérentes au silicium / 1 mW de puissance active dynamique).
