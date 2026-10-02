# REIO V4 — HARDWARE CPU DATASHEET

## 🔌 Interface Physique & Frontière Logique du Cœur Isolé

### 📟 1. Brochage Logique de l'Entité Matérielle (`reio_v4_cpu_top`)

L'interface externe de votre cœur de calcul trivalent se limite aux signaux d'infrastructure et aux bus de Trytes natifs pour éliminer toute logique périphérique parasite :

| Port Nom | Direction | Largeur | Type | Rôle Physique |
| :--- | :--- | :--- | :--- | :--- |
| **CLK** | Entrée | 1 bit | std_logic | Horloge système maîtresse (Cible stable à 100.00 MHz) |
| **RESETn** | Entrée | 1 bit | std_logic | Ligne de réinitialisation asynchrone active à l'état bas |
| **I_CPU_TRYTE_INSTR** | Entrée | 3 trites | tryte | Bus d'instruction ternaire d'entrée (Code Opcode) |
| **I_CPU_INSTR_VALID** | Entrée | 1 bit | std_logic | Strobe de validation de l'instruction présente sur le bus |
| **I_CPU_OPERAND_A** | Entrée | 3 trites | tryte | Premier opérande de calcul pour l'ALU paraconsistante |
| **I_CPU_OPERAND_B** | Entrée | 3 trites | tryte | Second opérande de calcul pour l'ALU paraconsistante |
| **O_CPU_TRYTE_RES** | Sortie | 3 trites | tryte | Bus de sortie transportant le résultat arithmétique synchrone |
| **O_CPU_FAULT_FLAG** | Sortie | 1 bit | std_logic | Indicateur physique de faille et d'absorption cryogénique |

---

## 🎛️ 2. Organisation Interne et Liaison des Blocs Spécifiques

Le processeur unifie ses **20 Slice LUTs** et ses **10 Registres** autour de deux sous-modules câblés en logique orthogonale :

```text
       I_CPU_TRYTE_INSTR       I_CPU_OPERAND_A      I_CPU_OPERAND_B

               |                      |                    |
               v                      |                    |
      +-----------------+             |                    |

      | REIO_V4_DECODER |             |                    |
      |  (DEC_BLOC)     |             |                    |
      +-----------------+             |                    |

               |                      |                    |
               v s_opcode_link (2b)   v                    v
      +------------------------------------------------------------+

      |                      REIO_V4_ALU                           |
      |                      (ALU_BLOC)                            |
      +------------------------------------------------------------+

               |                                           |
               v                                           v
        O_CPU_TRYTE_RES                             O_CPU_FAULT_FLAG
   (Résultat Trivalent)                        (Drapeau de Confinement)
```

### 🧬 Signaux d'Interconnexion Internes
* **s_opcode_link (1 downto 0) :** Liaison bus 2 bits transférant l'instruction décodée de `DEC_BLOC` vers `ALU_BLOC` ("01" = ADD_T, "10" = MUL_T, "11" = CRIT_HALT).
* **s_fault_dec & s_fault_alu :** Signaux de pannes unitaires sommés par une porte OR combinatoire asynchrone pour piloter immédiatement la broche physique `O_CPU_FAULT_FLAG`.

---

## 📊 3. Chronogramme d'Interception et d'Absorption Temporelle

Le graphe transitoire ci-dessous illustre l'absorption d'une anomalie en un minimum de cycles d'horloge. Dès qu'un Tryte indéterminé ou invalide est présenté sur le bus d'instruction, le signal de faille se lève au front montant suivant.

```text
                      <- Phase Nominale -> <-- Glitch d'Entrée (0x2) -->
                     0ns               10ns              20ns              30ns

                      |                 |                 |                 |
CLK          _________|¯¯¯¯¯¯¯¯¯|_________|¯¯¯¯¯¯¯¯¯|_________|¯¯¯¯¯¯¯¯¯|_________|¯¯¯¯
RESETn       ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
I_INSTR_VALID ________|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
I_TRYTE_INSTR ========X=== ('0','0','0') =========X=== ('2','2','2') =============
O_TRYTE_RES   ========X=== ('2','2','2') =========X=== ('2','2','2') =============
O_FAULT_FLAG  ____________________________________|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                                                  ^
                                           [Interception]
```
