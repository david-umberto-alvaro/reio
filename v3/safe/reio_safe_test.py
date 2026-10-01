#!/usr/bin/env python3
# ===============================================================================
# REIO SYSTEMS - REIO-SAFE (SPU_102) DISCONNECTOR INTEGRATION TEST
# Language: Python 3.x | Interface: C-FFI Bridge (ctypes bare-metal integration)
# ===============================================================================
import ctypes
import os
import sys

def load_reio_safe():
    target_dir = r"H:\REIO\SAFE\RUST\target\release"
    lib_name = "reio_safe.dll" if sys.platform.startswith("win32") else "libreio_safe.so"
    lib_path = os.path.join(target_dir, lib_name)
    
    if not os.path.exists(lib_path):
        print(f"❌ Erreur : Impossible de localiser le binaire REIO-Safe à : {lib_path}")
        sys.exit(1)
    return ctypes.CDLL(lib_path)

def run_tests():
    lib = load_reio_safe()
    # uint32_t verifier_stockage_safe(size_t base_addr);
    lib.verifier_stockage_safe.argtypes = [ctypes.c_size_t]
    lib.verifier_stockage_safe.restype = ctypes.c_uint32
    
    print("\n🚀 Démarrage de la suite de tests REIO-Safe (SPU-102)...")
    
    # Simulation d'adresses de structures de registres MMIO en mémoire émulée
    addr_nominal = 0x20000000
    res_nominal = lib.verifier_stockage_safe(addr_nominal)
    print(f" -> [Test 1] Mode standard (Stockage libre). Code retourné : {res_nominal}")
    assert res_nominal == 0, "Échec Test 1"
    print(" ✅ Test 1 Réussi : Mode nominal valide")
    
    addr_null = 0x0
    res_null = lib.verifier_stockage_safe(addr_null)
    print(f" -> [Test 3] Injection adresse NULL. Code retourné : {res_null}")
    assert res_null == 1, "Échec Test 3"
    print(" ✅ Test 3 Réussi : Robustesse Fail-Safe mémoire validée")

if __name__ == "__main__":
    run_tests()
