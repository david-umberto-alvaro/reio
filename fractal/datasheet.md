# REIO V4 FRACTAL — HARDWARE DATASHEET

## 🔌 Interface Physique & Cartographie des Registres MMIO

### 📟 1. Brochage Logique du Core Monolithique
L'interface externe de la puce se résume à une frontière simplifiée pour éliminer la fragmentation d'I/O :

| Port Nom | Direction | Largeur | Type | Rôle Physique |
| :--- | :---: | :---: | :---: | :--- |
| **CLK** | Entrée | 1 bit | std_logic | Horloge système maîtresse (Cible 100.00 MHz) |
| **RESETn** | Entrée | 1 bit | std_logic | Ligne de réinitialisation synchrone active à l'état bas |
| **I_PADDR** | Entrée | 32 bits | std_logic_vector | Bus d'adresses d'entrée provenant du maître APB |
| **I_PWDATA** | Entrée | 32 bits | std_logic_vector | Bus de données d'entrée (Chargement du tampon UART) |
| **I_PSEL** | Entrée | 1 bit | std_logic | Signal de sélection périphérique |
| **I_PENABLE** | Entrée | 1 bit | std_logic | Signal de validation de phase |
| **I_PWRITE** | Entrée | 1 bit | std_logic | Strobe d'activation de cycle d'écriture |
| **O_UART_TXD** | Sortie | 1 bit | std_logic | Ligne physique d'émission série du tampon de diagnostic |
| **O_SECURE_LATCH**| Sortie | 1 bit | std_logic | Ligne d'autorisation de maintien de charge utile |
| **O_TRIVALENT_FAULT**| Sortie | 1 bit | std_logic | Indicateur matériel de disjonction et d'interception |
| **O_CLAMPED_EN** | Sortie | 1 bit | std_logic | Sortie de validation filtrée pour esclaves secondaires |

### 🎛️ 2. Memory-Mapped Registers (MMIO)
Le plan de contrôle logiciel Rust (`reio_core_v4`) pilote l'infrastructure via un accès direct à l'adresse de base unique de la matrice :

*   **`BASE_BUS_ADDR` (`0x4000_5000`) :** 
    *   **En Lecture :** Capture le registre d'état du décodeur trivalent. Le Bit 0 à `'1'` indique la détection d'une anomalie ou d'un glitch de tension sur le bus.
    *   **En Écriture :** Charge le tampon de transmission de l'I/O série de diagnostic (`O_UART_TXD`) pour l'envoi asynchrone des octets de télémétrie. Un cycle d'écriture forcé à `0x0000_0000` déclenche l'effondrement immédiat et le verrouillage de la puce.

### 🧠 3. Schéma Cinématique du Micro-Noyau et du Planificateur

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
