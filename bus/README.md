# 🎛️ REIO-BUS — Matrice d'Interconnexion Crossbar Sécurisée

### 📌 Présentation Générale
REIO-BUS est la colonne vertébrale matérielle (Interconnect IP Core) du SoC. Il assure le routage étanche des paquets à travers une matrice de décodage d'adresse géométrique, isolant les périphériques esclaves et détruisant instantanément toute transaction ne transportant pas le jeton d'authentification durci.

### 📊 Spécifications du Matériel (FPGA)
* **Fréquence du Bus Système :** 100.00 MHz (Période nominale : 10.00 ns).
* **Temps de Réaction de Sécurité :** Interception de tag invalide, effondrement complet du bus à 0V et levée du signal d'alerte activés en exactement **1 cycle d'horloge (10.00 ns)**.

### 📊 Synthèse d'Audit et Fermeture Temporelle (Vivado Static Timing)
* **Worst Negative Slack (WNS) :** Fermeture temporelle impeccable validée sans aucune violation sur le domaine synchrone principal.
* **Confinement des Fautes :** Le signal physique d'alarme `BUS_FAULT_FLAG` isole instantanément la matrice en cas d'injection de clé corrompue.

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)
L'exécution du plan de contrôle en Rust bare-metal (`#![no_std]`) certifie la conformité de l'interface :
* **[Test 1] Routage Esclave 1 :** Commutation réussie du flux vers la zone basse (Décodage bit 15 à 0).
* **[Test 2] Routage Esclave 2 :** Commutation réussie du flux vers la zone haute (Décodage bit 15 à 1).
* **[Test 3] Interception Intrusion :** Tag invalide détecté, isolement actif à 0V et levée immédiate de la ligne d'alerte (`BUS_FAULT_FLAG` <= '1').

🏆 CERTIFICATION DU PILOTE CORE REIO-BUS EFFECTUÉE AVEC SUCCÈS !
