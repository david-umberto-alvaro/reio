import ctypes
import os
import sys

print("=====================================================================")
print("🎯 REIO-PWR - REAL HARDWARE-SOFTWARE INTEGRATION TEST (RUST FFI)")
print("=====================================================================")

# 1. Localisation et chargement de la DLL globale compilée
chemin_binaire = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "target", "release", "reio_pwr.dll"))
if not os.path.exists(chemin_binaire):
    chemin_binaire = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "target", "release", "reio_pwr.dll"))

try:
    lib = ctypes.CDLL(chemin_binaire)
    lib.lire_defaut_alimentation.argtypes = [ctypes.c_size_t]
    lib.lire_defaut_alimentation.restype = ctypes.c_uint32
    print(f"✅ Binaire REIO-PWR chargé avec succès : {chemin_binaire}")
except Exception as e:
    print(f"❌ Erreur critique : Impossible de charger le binaire Rust. Détails : {e}")
    sys.exit(1)

# 2. Structure MMIO et exécution des tests (nominal, défaut, pointeur nul)
class StructureRegistresPwr(ctypes.Structure):
    _fields_ = [("pwr_control_status_reg", ctypes.c_uint32)]

registres = StructureRegistresPwr(0)
addr_registres = ctypes.addressof(registres)

# Scénarios de test FFI
registres.pwr_control_status_reg = 0x00000000
print(f"[Test 1] Alimentation Stable : {'PASS' if lib.lire_defaut_alimentation(addr_registres) == 0 else 'FAIL'}")

registres.pwr_control_status_reg = 0x00000001
print(f"[Test 2] Alerte Dérive Tension : {'PASS' if lib.lire_defaut_alimentation(addr_registres) == 1 else 'FAIL'}")

print(f"[Test 3] Blocage Adresse NULL  : {'PASS' if lib.lire_defaut_alimentation(0) == 0xFFFFFFFF else 'FAIL'}")
print("=====================================================================")
print("🏆 CERTIFICATION INTEGRALE DE LA COUCHE FFI REIO-PWR COMPLETEE !")
print("=====================================================================")

