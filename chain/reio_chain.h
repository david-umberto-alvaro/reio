#ifndef REIO_CHAIN_H
#define REIO_CHAIN_H

#include <stdint.h>
#include <stddef.h>

typedef struct __attribute__((aligned(32))) {
    uint32_t packets_clean;     // Correspond à REG_CNT_CLEAN (Offset 0x0C)
    uint32_t packets_anomaly;   // Correspond à REG_CNT_ANOM  (Offset 0x10)
    uint8_t  security_status;   // Avec un "i" !
    // Le compilateur ajoute automatiquement le padding pour atteindre 32 octets
} reio_chain_telemetry_t;

// Point d'entrée du pilote de contrôle Rust (C-FFI Bridge)
uint32_t initialiser_filtre_chain(uint32_t base_address);
void lire_telemetrie_chain(reio_chain_telemetry_t *out_telemetry);

#endif /* REIO_CHAIN_H */
