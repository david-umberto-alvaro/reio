#!/usr/bin/env python3
# ===============================================================================
# REIO SYSTEMS - REIO-SAFE (SPU_102) DISCONNECTOR INTEGRATION TEST
# Language: Python 3.x | Interface: C-FFI Bridge (ctypes bare-metal integration)
# Validation standard: REIO-SAFE Anti-Ransomware Framework
# Concu pour execution autonome : Zero dependance Cargo / Rust / .rs en production
# ===============================================================================

import ctypes
import os
import sys

def load_reio_safe_library():
    """
    Localise et charge dynamiquement le binaire partage REIO-Safe.
    Prend en charge la structure autonome (sans .rs) et le fallback de dev Cargo.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Identification de la plateforme et de l'extension du binaire
    if sys.platform.startswith("linux"):
        lib_name = "libreio_safe.so"
    elif sys.platform.startswith("win32"):
        lib_name = "reio_safe.dll"
    elif sys.platform.startswith("darwin"):
        lib_name = "libreio_safe.dylib"
    else:
        raise OSError(f"Plateforme non supportee : {sys.platform}")

    # Chemin 1 : Recherche autonome a cote du script (Pour les utilisateurs finaux)
    lib_path = os.path.join(script_dir, lib_name)
    
    # Chemin 2 : Fallback vers le dossier de dev RUST situe a la racine SAFE
    if not os.path.exists(lib_path):
        lib_path = os.path.join(script_dir, "RUST", "target", "release", lib_name)

    # Securite si la bibliotheque reste introuvable
    if not os.path.exists(lib_path):
        print(f"❌ Erreur : Impossible de localiser la bibliotheque '{lib_name}'")
        print(f"   Placez le fichier dans le dossier ou compilez via 'cargo build --release'.")
        sys.exit(1)

    print(f"✅ Binaire REIO-Safe charge avec succes : {lib_path}")
    return ctypes.CDLL(lib_path)

def configure_safe_interface(lib):
    """
    Configure la signature FFI de la fonction Rust bare-metal du SPU-102.
    """
    try:
        # uint32_t verifier_stockage_safe(size_t base_addr);
        lib.verifier_stockage_safe.argtypes = [ctypes.c_size_t]
        lib.verifier_stockage_safe.restype = ctypes.c_uint32
        print("✅ Signature FFI C-Bridge configuree (1 argument : base_addr)")
    except AttributeError:
        print("❌ Erreur : La fonction 'verifier_stockage_safe' est introuvable.")
        sys.exit(1)

def run_safe_integration_tests(lib):
    """
    Simule la reponse du pilote face a un etat nominal ou un blocage DEADBEEF.
    """
    print("\n🚀 Demarrage de la suite de tests REIO-Safe...")
    
    # Simulation d'un espace memoire virtuel de test (MMIO virtuel)
    # Offset 0x00: entropy_status | Offset 0x04: reg_alpha_echo
    fake_buffer_nominal = (ctypes.c_uint32 * 2)(0x00000000, 0xA5A5A5A5) # Etat nominal
    fake_buffer_sabotage = (ctypes.c_uint32 * 2)(0xDEADBEEF, 0xA5A5A5A5) # Etat d'alerte matériel
    
    addr_nominal = ctypes.addressof(fake_buffer_nominal)
    addr_sabotage = ctypes.addressof(fake_buffer_sabotage)

    # ---------------------------------------------------------------------------
    # TEST 1 : Mode Nominal (Pas d'attaque ransomware, stockage transparent)
    # ---------------------------------------------------------------------------
    res_nominal = lib.verifier_stockage_safe(addr_nominal)
    print(f" -> [Test 1] Etat nominal inspecte. Retour FFI : {res_nominal}")
    assert res_nominal == 0, "❌ Echec Test 1 : Le stockage nominal a decline l'acces !"
    print(" ✅ Test 1 Reussi : Flux nominal sain autorise")

    # ---------------------------------------------------------------------------
    # TEST 2 : Mode Interception Active (Tag DEADBEEF detecte)
    # ---------------------------------------------------------------------------
    res_sabotage = lib.verifier_stockage_safe(addr_sabotage)
    print(f" -> [Test 2] Alerte ransomware injectee. Retour FFI : {res_sabotage}")
    assert res_sabotage == 1, "❌ Echec Test 2 : L'isolation physique de la Flash n'a pas ete detectee !"
    print(" ✅ Test 2 Reussi : Disjoncteur actif, stockage verouille en lecture seule")

    print("\n🏆 [SUCCESS] L'ecosysteme logiciel REIO-Safe est 100% conforme !")

if __name__ == "__main__":
    reio_safe_lib = load_reio_safe_library()
    configure_safe_interface(reio_safe_lib)
    run_safe_integration_tests(reio_safe_lib)
