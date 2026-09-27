#ifndef REIO_DRIVE_H
#define REIO_DRIVE_H

#include <stdint.h>
#include <stddef.h>

// Structure de télémétrie REIO-Drive alignée sur 32 octets pour le cache CPU
typedef struct __attribute__((aligned(32))) {
    uint32_t packets_clean;
    uint32_t packets_anomaly;
    uint8_t  security_status;
} reio_telemetry_t;

// Point d'entrée de l'interceptor synchrone aligné sur le bus 100 MHz du XDC
uint32_t verifier_flux_reio(const uint8_t * buffer_ptr, size_t taille);

#endif /* REIO_DRIVE_H */

