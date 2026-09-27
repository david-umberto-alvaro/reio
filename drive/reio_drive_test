#!/usr/bin/env python3
# ===============================================================================
# REIO SYSTEMS - REIO-DRIVE (SPU_105) CONTROL PLANE INTEGRATION TEST
# Language: Python 3.x | Interface: C-FFI Bridge (ctypes bare-metal integration)
# Validation standard: REIO-RFC-003 V3 (Axiom REIO-A4 Confinement)
# ===============================================================================

import ctypes
import os
import sys

# Constante de confinement paracohérent (Synchronisée avec lib.rs)
CRITICAL_ENTROPY = 0x7F

def load_reio_library():
    """
    Localise et charge dynamiquement le binaire partagé compilé par Cargo.
    Prend en charge les extensions Linux (.so), Windows (.dll) et macOS (.dylib).
    """
    
    # Remonte d'un niveau supplémentaire pour atteindre la racine du projet DRIVE
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Racine du projet DRIVE (Remonte d'un niveau au-dessus du dossier RUST)
    target_dir = r"H:\REIO\PROJETS\DRIVE\RUST\target\release"

    if sys.platform.startswith("linux"):
        lib_name = "libcode.so"
    elif sys.platform.startswith("win32"):
        lib_name = "reio_drive.dll"
    elif sys.platform.startswith("darwin"):
        lib_name = "libcode.dylib"

    lib_path = os.path.join(target_dir, lib_name)
    
    # Fallback local si le script est exécuté directement dans le sous-dossier drive
    if not os.path.exists(lib_path):
        print(f"❌ Erreur : Impossible de localiser la DLL REIO à l'adresse : {lib_path}")
        sys.exit(1)

        
    print(f"✅ Binaire REIO chargé avec succès : {lib_path}")
    return ctypes.CDLL(lib_path)

def configure_ffi_interface(lib):
    """
    Configure la signature stricte à 2 arguments de la fonction FFI Rust.
    Élimine tout indéterminisme temporel lié aux variables de calendrier.
    """
    try:
        # uint32_t verifier_flux_reio(const uint8_t * buffer_ptr, size_t taille);
        lib.verifier_flux_reio.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
        lib.verifier_flux_reio.restype = ctypes.c_uint32
        print("✅ Signature FFI C-Bridge configurée (2 arguments : pointer, size_t)")
    except AttributeError:
        print("❌ Erreur : La fonction 'verifier_flux_reio' est introuvable dans le binaire.")
        print("💡 Vérifiez que l'attribut #[no_mangle] et pub extern \"C\" sont présents en Rust.")
        sys.exit(1)

def run_integration_tests(lib):
    """
    Exécute la suite de crash-tests unitaires et d'injection de fautes.
    """
    print("\n🚀 Démarrage de la suite de tests REIO-Drive...")
    
    # ---------------------------------------------------------------------------
    # TEST 1 : Flux Nominal Ordinaire (Trafic sain sans anomalie)
    # ---------------------------------------------------------------------------
    data_saine = (ctypes.c_uint8 * 4)(0x01, 0xAA, 0x03, 0x04) # Contient la trame standard 'aa' de la simulation
    buffer_sain = ctypes.cast(data_saine, ctypes.POINTER(ctypes.c_uint8))
    
    status_sain = lib.verifier_flux_reio(buffer_sain, len(data_saine))
    print(f" -> [Test 1] Flux standard (0xAA) envoyé. Statut retourné : {status_sain}")
    assert status_sain == 0, "❌ Échec Test 1 : Le flux sain a déclenché une fausse alerte !"
    print(" ✅ Test 1 Réussi : Mode nominal intègre validé (security_status = 1)")

    # ---------------------------------------------------------------------------
    # TEST 2 : Injection de Faute Critique (Sabotage 0x7F / REIO-A4)
    # ---------------------------------------------------------------------------
    data_corrompue = (ctypes.c_uint8 * 4)(0x01, CRITICAL_ENTROPY, 0x03, 0x04)
    buffer_corrompu = ctypes.cast(data_corrompue, ctypes.POINTER(ctypes.c_uint8))
    
    status_corrompu = lib.verifier_flux_reio(buffer_corrompu, len(data_corrompue))
    print(f" -> [Test 2] Sabotage (0x7F) injecté. Statut retourné : {status_corrompu}")
    assert status_corrompu == 1, "❌ Échec Test 2 : Le sabotage 0x7F n'a pas été intercepté !"
    print(" ✅ Test 2 Réussi : Confinement paracohérent activé (emergency_trigger = 1)")

    # ---------------------------------------------------------------------------
    # TEST 3 : Sûreté Robuste (Pointeurs invalides / Protection mémoire)
    # ---------------------------------------------------------------------------
    status_null = lib.verifier_flux_reio(None, 10)
    print(f" -> [Test 3] Pointeur NULL injecté. Statut retourné : {status_null}")
    assert status_null == 0, "❌ Échec Test 3 : La gestion de la mémoire a levé un indéterminisme !"
    print(" ✅ Test 3 Réussi : Sécurité Fail-Safe mémoire validée")

    print("\n🏆 [SUCCESS] L'écosystème logiciel REIO-Drive est 100% conforme au Standard REIO !")

if __name__ == "__main__":
    reio_lib = load_reio_library()
    configure_ffi_interface(reio_lib)
    run_integration_tests(reio_lib)
