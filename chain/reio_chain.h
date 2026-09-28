#ifndef REIO_CHAIN_H
#define REIO_CHAIN_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Structure de telemetrie alignee sur une ligne de cache de 32 octets.
 * Le bourrage explicite empeche toute desynchronisation avec Rust.
 */
typedef struct __attribute__((aligned(32))) {
    uint32_t packets_clean;     // Correspond a REG_CNT_CLEAN (Offset 0x0C) - 4 octets
    uint32_t packets_anomaly;   // Correspond a REG_CNT_ANOM (Offset 0x10) - 4 octets
    uint8_t  security_status;   // Statut logique du filtre - 1 octet
    uint8_t  reserved[23];      // Bourrage explicite pour atteindre strictement 32 octets (4+4+1+23 = 32)
} reio_chain_telemetry_t;

// Point d'entree du pilote de controle Rust (C-FFI Bridge)
uint32_t initialiser_filtre_chain(uint32_t base_address);
void lire_telemetrie_chain(reio_chain_telemetry_t *out_telemetry);

#ifdef __cplusplus
}
#endif

#endif /* REIO_CHAIN_H */
