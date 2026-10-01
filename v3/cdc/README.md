# ⛓ REIO-CDC — Synchroniseur Multi-Horloge Anti-Métastabilité

### 📌 Présentation Générale
REIO-CDC est un IP Core matériel assurant le transfert sécurisé de signaux à travers des domaines d'horloges asynchrones (Canal 1 Haute Vitesse à 400 MHz vers 100 MHz et Canal 2 Automobile à 66.67 MHz vers 100 MHz) [index_0.1.15].

### 📊 Spécifications et Performances (FPGA / Vivado)
* **Plan de contrôle :** 100.00 MHz (temps de réponse de 3 cycles d'horloge / 30.00 ns) [index_0.1.15].
* **Fermeture temporelle (Timing) :** WNS à +8,926 ns, WHS à +0,131 ns, WPWS à +4,500 ns [index_0.1.18].
* **Empreinte silicium :** 3 Slice Registers et 1 Slice LUT [index_0.1.15, index_0.1.19].
* **Consommation :** 71 mW total, température de jonction à 25.3 °C [index_0.1.17].

### 🌐 Architecture Fonctionnelle
Le schéma complet du pipeline de capture anti-métastabilité à 3 registres sous `CLK_DEST` (100 MHz) est disponible dans le document de référence [index_0.1.15, index_0.1.19].

### 🚀 Validation Logicielle (Rust / Python FFI)
La suite de tests unitaires valide l'étanchéité de l'interface MMIO (tests de repos, capture inter-domaines et gestion d'erreur pointeur NULL) [index_0.1.15].

### 🌐 Architecture Fonctionnelle du Pipeline REIO-CDC

```text
       +-------------------------------------------------------+

       |                  DOMAINE ASYNCHRONE                   |
       |         (Flux Haute Fréquence ou Auto : 400M / 66M)   |
       +-------------------------------------------------------+
                                   |
                                   | ASYNC_IN (Signal de Rupture brute)
                                   v
       +=======================================================+

       |                       SILICIUM                        |
       | ----------------------------------------------------- |
       |          CHAINE DE CAPTURE ANTI-MÉTASTABILITÉ         |
       |          (3 Slice Registers / ASYNC_REG = TRUE)       |
       |                                                       |
       |   +------------+     +------------+     +------------+ |
       |   | sync_reg0  | --> | sync_reg1  | --> | sync_reg2  | |
       |   | (Capture)  |     | (Stabline) |     | (Sortie)   | |
       |   +------------+     +------------+     +------------+ |
       |         ^                 ^                 ^         |
       +=========|=================|=================|=========+

                 |                 |                 |
                 +-----------------+-----------------+--- CLK_DEST (100 MHz)

                                                     |
                                                     v
                                          +--------------------+

                                          |   DOMAINE CIBLE    |
                                          | SYNC_OUT (Stable)  |
                                          | -> Bus 100 MHz     |
                                          +--------------------+
```

### 📊 Validation Fonctionnelle & Formes d'Ondes (Testbench RTL)

![Chronogramme des formes d'ondes](reio_cdc_simulation.png)

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)
L'exécution de la suite de tests unitaires sur le plan de contrôle en Rust bare-metal (`#![no_std]`) certifie la parfaite étanchéité de l'interface MMIO :
*   **[Test 1] Statut de Repos (Bus à 0) :** Validation du bus de statut au niveau bas nominal stable (`PASS` | Valeur lue : `0x0`).
*   **[Test 2] Capture Inter-Domaines (Signal 1) :** Absorption complète de la gigue asynchrone et lecture stabilisée du bit à l'état haut (`PASS` | Valeur lue : `0x1`).
*   **[Test 3] Erreur Pointeur (Adresse NULL) :** Robustesse logicielle validée avec succès par interception immédiate et bloquante de la couche FFI (`PASS` | Valeur lue : `0xffffffff`).

![Rapport de validation du script Python](reio_cdc_test.png)
