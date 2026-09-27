#ifndef REIO_DRIVE_H
#define REIO_DRIVE_H

#include <stdint.h>
#include <stddef.h>

// Structure de télémétrie REIO-Drive alignée sur 32 octets pour le cache CPU
typedef struct __attribute__((aligned(32))) {
    uint32_t packets_clean;
    uint32_t packets_anomaly;
    uint8_t  security_status;
    // Le compilateur insère automatiquement le padding nécessaire
} reio_telemetry_t;

// Point d'entrée de l'intercepteur combinatoire (C-FFI Bridge)
uint32_t verifier_flux_reio(const uint8_t * buffer_ptr, 
                            size_t taille, 
                            uint32_t annee_actuelle, 
                            uint32_t mois_actuel, 
                            uint32_t jour_actuel);

#endif /* REIO_DRIVE_H */
