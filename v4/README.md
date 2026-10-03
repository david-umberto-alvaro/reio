# REIO V4 — GÉNÉRATION TRIVALENTE

Ce répertoire centralise les briques technologiques de la **Génération V4** du framework REIO (Réalisme Expérimental Instrumenté Optimisé). Cette génération marque l'abandon de la fragmentation périphérique pour imposer la convergence matérielle et logicielle en base ternaire.

## 🗺️ Organisation des Sous-Modules

*   📂 **[`amt/`](./amt/) (Architecture Monolithique Trivalente) :** Base historique et archives de validation de la première architecture monolithique stable (STA Vivado validée, rapports de compliance et codes d'origine isolés).
*   📂 **[`cpu/`](./cpu/) (Cœur CPU Trivalent Isolé) :** Implémentation du processeur arithmétique gérant le micro-noyau bare-metal (Certifié résistant à une rafale de 1000 injections stochastiques de radiations).

## 🧠 Caractéristiques Communes de Sûreté

L'ensemble de la flotte de composants de la Génération V4 repose sur l'intégration conjointe de deux ruptures fondamentales, interconnectant la logique mathématique pure et la physique du silicium :

### 1. Logique Trivalente Formelle (Base Ternaire Non-Analytique)
Contrairement aux architectures booléennes classiques restreintes au binarisme strict (`0` et `1`), les structures logiques de la V4 implémentent un troisième état matériel d'indétermination active (`trite_2` ou configuration de bus `10`).
*   **Propagation Déterministe :** Cet état ne représente pas une absence de signal, mais une indétermination mathématique matérialisée. Le système peut manipuler et propager ce doute à travers l'ALU sans provoquer de comportement indéfini.
*   **Confinement Algorithmique :** L'apparition d'un `trite_2` isole instantanément la variable compromise, interdisant toute corruption des registres sains adjacents et éliminant à la racine les hallucinations logiques.

### 2. Homéostasie Active Matérielle
Inspirée des mécanismes de régulation biologique des milieux complexes, l'homéostasie active est la faculté des transistors à déclencher de manière autonome une force de rappel asynchrone face aux agressions physiques externes.
*   **Disjonction Sub-Nanoseconde :** Dès qu'une violation de temps de configuration (setup/hold) ou qu'un glitch électromagnétique est capté sur une ligne, les barrières anti-métastabilité forcent un écrasement du bus vers l'état neutre stable.
*   **Sûreté en 1 Cycle :** Cette régulation est entièrement câblée dans le silicium (Hardware enforcement) et s'exécute en très exactement **1 cycle d'horloge**. Elle s'affranchit totalement du micro-noyau Rust, garantissant une isolation d'urgence infaillible même en cas de gel complet du logiciel.
