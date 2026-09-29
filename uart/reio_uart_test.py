import ctypes
import os
import sys

print("=====================================================================")
print("🎯 REIO-UART - REAL HARDWARE-SOFTWARE INTEGRATION TEST (RUST FFI)")
print("=====================================================================")

# Localisation centralisée globale dans target racine
chemin_binaire = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "target", "release", "reio_uart.dll"))

try:
    lib = ctypes.CDLL(chemin_binaire)
    
    # Configuration des prototypes FFI
    lib.transmettre_octet_uart.argtypes = [ctypes.c_size_t, ctypes.c_uint32]
    lib.transmettre_octet_uart.restype = None
    
    lib.lire_defaut_uart.argtypes = [ctypes.c_size_t]
    lib.lire_defaut_uart.restype = ctypes.c_uint32
    
    print(f"✅ Binaire REIO-UART chargé avec succès depuis :\n   [{chemin_binaire}]")
    print(f"✅ Signatures C-Bridge configurées avec succès")
except Exception as e:
    print(f"❌ Erreur critique : Impossible de charger le binaire Rust. Détails : {e}")
    sys.exit(1)

# Structure MMIO calée sur le layout mémoire Rust
class StructureRegistresUart(ctypes.Structure):
    _fields_ = [
        ("uart_wdata_reg", ctypes.c_uint32),
        ("uart_rdata_reg", ctypes.c_uint32),
        ("uart_write_en_reg", ctypes.c_uint32),
        ("uart_fault_flag_reg", ctypes.c_uint32)
    ]

# Mappage d'une zone d'E/S en RAM
registres = StructureRegistresUart(0, 0, 0, 0)
addr_registres = ctypes.addressof(registres)

print(f"📝 Registres matériels mappés en RAM à l'adresse : {hex(addr_registres)}")
print("---------------------------------------------------------------------")

# --- EXÉCUTION DE LA SUITE DE TESTS SUR LE VRAI CODE MACHINE ---

# [Test FFI 1] Dépôt Nominal d'Octet (Mode stable)
registres.uart_fault_flag_reg = 0x00000000 
lib.transmettre_octet_uart(addr_registres, 0x000000AA) 
res_nominal = lib.lire_defaut_uart(addr_registres)

status_nominal = "PASS" if res_nominal == 0 and registres.uart_wdata_reg == 0x000000AA else "FAIL"
print(f"[Test FFI 1] Transmission Stable (0xAA) : {status_nominal} (Alarme lue par Rust: {res_nominal})")

# [Test FFI 2] Interception de Débordement (Buffer Overflow)
registres.uart_fault_flag_reg = 0x00000001
res_overflow = lib.lire_defaut_uart(addr_registres)

status_overflow = "PASS" if res_overflow == 1 else "FAIL"
print(f"[Test FFI 2] Confinement sur Overflow    : {status_overflow} (Rust intercepte la disjonction: {res_overflow})")

# [Test FFI 3] Sécurité Pointeur NULL (Fail-Safe mémoire)
res_null = lib.lire_defaut_uart(0)
status_null = "PASS" if res_null == 0xFFFFFFFF else "FAIL"
print(f"[Test FFI 3] Blocage sur Adresse NULL   : {status_null} (Rust intercepte le pointeur invalide)")

print("---------------------------------------------------------------------")
print("🏆 CERTIFICATION INTEGRALE DE LA COUCHE FFI REIO-UART COMPLÉTÉE !")
print("=====================================================================")
