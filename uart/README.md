# 🔌 REIO-UART — Contrôleur d'E/S de Diagnostic Isolé

### 📌 Présentation Générale
REIO-UART est le bloc d'infrastructure matérielle (IP Core) du SoC REIO chargé d'assurer la transmission sécurisée de la télémétrie et des logs de diagnostic à 115200 bauds. Il intègre un tampon matériel rigide couplé à un automate de disjonction combinatoire pour contrer les attaques par débordement de tampon (*Buffer Overflow*).

### 📊 Spécifications du Matériel (FPGA) et Synthèse Vivado
* **Fréquence / Vitesse :** Bus système à 100.00 MHz, transmission à 115200 Bauds.
* **Temps de Réaction :** 1 cycle d'horloge (10.00 ns) en cas d'overflow.
* **Timing & Utilisation :** WNS à +5,457 ns, WHS à +0,218 ns, pour une empreinte de 30 Slice Registers et 35 Slice LUTs.
* **Puissance & Température :** 71 mW au total, température de jonction stabilisée à 25.3 °C.

### 🌐 Architecture Fonctionnelle du Pipeline REIO-UART
*(Schéma fonctionnel complet d'E/S intégrant l'interface MMIO, le disjoncteur de port de diagnostic et l'aiguillage entre l'état nominal de transmission et l'état de clamp d'isolement en cas d'attaque).*

```text
       +-------------------------------------------------------+

       |               INTERFACE BUS SYSTÈME MMIO              |
       |       (UART_WDATA / UART_WRITE_EN / UART_RDATA)       |
       +-------------------------------------------------------+
                                   |
                                   | Surveillance du débit
                                   v
       +=======================================================+

       |                       SILICIUM                        |
       | ----------------------------------------------------- |
       |              TAMPON MATÉRIEL RIGIDE D'ÉCONOMIE        |
       |          (35 Slice LUTs / 30 Slice Registers)         |
       |                                                       |
       |     [Compteur Octets] ---> [Seuil Critique >= 4]      |
       +=======================================================+

                 |                                     |
                 | Débit Intègre                       | Débordement Intercepté
                 | (Transmission 115200 Bauds)         | (Confinement Éclair)
                 v                                     v
       +-----------------------+             +-----------------------+

       |       ST_IDLE         |             |  ST_ISOLATION_CLAMP   |
       |          |            |             | --------------------- |
       |          v            |             | -> TX <= '0' (0 Volt) |
       |  ST_TRANSMIT_START    |             |                       |
       |          |            |             | -> UART_FAULT_FLAG    |
       |          v            |             |    <= '1' (Alarme)    |
       |  ST_TRANSMIT_DATA     |             |                       |
       |   (Sérialisation TX)  |             |                       |
       +-----------------------+             +-----------------------+
```


### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)
Validation complète de l'étanchéité de l'interface MMIO à travers les tests unitaires bare-metal (`PASS`) :
* **[Test FFI 1]** Dépôt Nominal d'Octet.
* **[Test FFI 2]** Interception de Débordement.
* **[Test FFI 3]** Sécurité Pointeur NULL.

