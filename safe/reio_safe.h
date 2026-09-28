#ifndef REIO_SAFE_H
#define REIO_SAFE_H

/* ===============================================================================
 * REIO SYSTEMS - REIO-SAFE (SPU_102) HARDWARE-SOFTWARE INTERFACE SPECIFICATION
 * Language: C99 / C++ Compatible | Target: Hardened Storage Controller
 * Validation standard: REIO-RFC-002 V1 (Anti-Ransomware Physical Isolation)
 * =============================================================================== */

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Constante d'interception renvoyee par le materiel REIO-Safe
 * Si le disjoncteur SPU-102 se declenche, il fige le bus PRDATA sur cette valeur.
 */
#define REIO_SAFE_VAL_ALERTE         0xDEADBEEF

/**
 * @brief Codes de retour protocolaires de l'interface FFI
 */
#define REIO_SAFE_STATUS_NOMINAL     0x00000000  /* Acces transparent autorise */
#define REIO_SAFE_STATUS_ISOLATED    0x00000001  /* Flash verrouillee en Lecture Seule */

/**
 * @brief Structure de mappage memoire (MMIO) du periphérique REIO-Safe
 * Cette structure reflete au bit pres l'architecture interne VHDL du SPU-102.
 */
typedef struct {
    volatile uint32_t entropy_status; /**< Offset 0x00 : Compteur d'entropie / Tag d'alerte */
    volatile uint32_t reg_alpha_echo;  /**< Offset 0x04 : Echo de verification du Registre Alpha */
} ReioSafeRegisters;

/* ===============================================================================
 * SIGNATURES DES FONCTIONS EXPORTEES (Pont FFI Rust / C)
 * =============================================================================== */

/**
 * @brief Verifie explicitement l'etat de sûrete du controleur de stockage.
 * 
 * Cette fonction lit de maniere volatile les registres physiques du SPU-102. 
 * Si le tag 0xDEADBEEF est detecte, elle confirme le confinement actif du disque.
 * 
 * @param base_addr Adresse memoire brute (MMIO) du peripherique sur le bus APB.
 * @return uint32_t REIO_SAFE_STATUS_ISOLATED (1) ou REIO_SAFE_STATUS_NOMINAL (0).
 */
uint32_t verifier_stockage_safe(size_t base_addr);

#ifdef __cplusplus
}
#endif

#endif /* REIO_SAFE_H */
