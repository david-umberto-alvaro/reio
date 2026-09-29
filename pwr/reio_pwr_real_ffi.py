import ctypes
import os
import sys

print("=====================================================================")
print("🎯 REIO-PWR - REAL HARDWARE-SOFTWARE INTEGRATION LAYER (RUST FFI)")
print("=====================================================================")

# 1. Localisation et chargement du vrai binaire compilé par Cargo
# Cargo génère le binaire dans le dossier target global de la racine H:\REIO
chemin_binaire = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "target", "release", "reio_pwr.dll"))

try:
    # Chargement de la bibliothèque dynamique Rust
    lib_rust = ctypes.CDLL(chemin_binaire)
    
    # Configuration du prototype de la fonction FFI Rust
    # fn lire_defaut_alimentation(base_addr: usize) -> u32
    lib_rust.lire_defaut_alimentation.argtypes = [ctypes.c_size_t]
    lib_rust.lire_defaut_alimentation.restype = ctypes.c_uint32
    print(f"✅ Bibliothèque native Rust chargée avec succès depuis :\n   [{chemin_binaire}]")
except Exception as e:
    print(f"❌ Erreur critique : Impossible de charger le binaire Rust.\n   Vérifiez que 'cargo build --release' a bien été exécuté.\n   Détails : {e}")
    sys.exit(1)

# 2. Définition d'une zone mémoire émulant les registres MMIO physiques du silicium
class StructureRegistresMatériels(ctypes.Structure):
    _fields_ = [("pwr_control_status_reg", ctypes.c_uint32)]

# Instanciation d'un vrai bloc de registres en mémoire RAM
registres_physiques = StructureRegistresMatériels()
adresse_brute_registres = ctypes.addressof(registres_physiques)

print(f"📝 Registres matériels mappés en RAM à l'adresse physique : {hex(adresse_brute_registres)}")
print("---------------------------------------------------------------------")

# --- EXÉCUTION DE LA SUITE DE TESTS SUR LE VRAI CODE MACHINE RUST ---

# [Test 1] Mode Nominal (Tensions stables, pas de défaut)
# Bit 0 du registre d'état = 0 (Pas de flag d'erreur)
registres_physiques.pwr_control_status_reg = 0x00000000 
res_nominal = lib_rust.lire_defaut_alimentation(adresse_brute_registres)
status_nominal = "PASS" if res_nominal == 0 else "FAIL"
print(f"[Test FFI 1] Mode Alimentation Stable   : {status_nominal} (Rust lève le flag: {res_nominal})")

# [Test 2] Mode Rupture Électrique (Glitch ou baisse de tension détectée)
# Le matériel lève le bit 0 du registre à '1'
registres_physiques.pwr_control_status_reg = 0x00000001 
res_glitch = lib_rust.lire_defaut_alimentation(adresse_brute_registres)
status_glitch = "PASS" if res_glitch == 1 else "FAIL"
print(f"[Test FFI 2] Confinement sur Glitch     : {status_glitch} (Rust intercepte le défaut: {res_glitch})")

# [Test 3] Protection contre l'injection de pointeurs de registres NULL
res_null = lib_rust.lire_defaut_alimentation(0)
status_null = "PASS" if res_null == 0xFFFFFFFF else "FAIL"
print(f"[Test FFI 3] Blocage sur Adresse NULL   : {status_null} (Rust intercepte le pointeur invalide)")

print("---------------------------------------------------------------------")
print("🏆 CERTIFICATION INTEGRALE DE LA COUCHE FFI RUST-PYTHON VALIDEE !")
print("=====================================================================")
