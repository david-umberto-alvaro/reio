# ⛓️ REIO-CDC — Synchroniseur Multi-Horloge Anti-Métastabilité

REIO-CDC est un bloc de propriété intellectuelle (IP Core) matériel de bas niveau conçu pour sécuriser le transfert de signaux critiques à travers des domaines d'horloges asynchrones (Clock Domain Crossing). Il agit comme le liant d'étanchéité physique reliant le domaine réseau haute fréquence (400 MHz) au domaine de contrôle système (100 MHz).

### 🔬 Architecture d'Immunité & Invariant Temporel

Le module neutralise mathématiquement le risque de métastabilité induit par la gigue temporelle ou les injections de pannes (glitchs d'horloges) :
* **Cascade Séquentielle à 3 Étages :** Implémentation d'une chaîne de trois bascules synchrones de type `FDCE` régies par l'attribut de synthèse strict `ASYNC_REG == TRUE`. Cet agencement force le placement contigu des cellules pour absorber l'énergie oscillatoire résiduelle en cas de violation de setup/hold.
* **Fermeture Temporelle Durcie :** L'intégration de la contrainte matérielle `set_false_path` instruit le moteur de routage d'ignorer les faux chemins critiques combinatoires, éliminant les incertitudes de phase d'horloge.
* **Temps de Stabilisation :** Le signal asynchrone est capturé, filtré et restitué fermement dans le domaine d'arrivée en exactement **3 cycles d'horloge destination**.

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)

L'exécution de la suite de tests unitaires sur le plan de contrôle Rust (`#![no_std]`) certifie la parfaite conformité de l'interface MMIO :
* **[Test 1] Statut de Repos :** Validation du bus de statut au niveau bas nominal stable (`0x0`).
* **[Test 2] Capture Inter-Domaines :** Stabilisation matérielle et lecture réussie du signal de transition à l'état haut (`0x1`).
* **[Test 3] Erreur Pointeur :** Robustesse logicielle validée face à l'injection d'une adresse de registre NULL.
