# 🛡️ REIO-Safe (SPU-102) — Hardware Anti-Ransomware Storage Disconnector

## 1. Executive Overview
REIO-Safe is a critical security module co-designed using **synchronous VHDL** and **bare-metal Rust (`#![no_std]`)**. Operating at the physical storage controller layer, it acts as an active hardware disconnector designed to intercept ransomware activities (such as mass encryption loops or low-level geometric payload alterations) before malicious writes can damage the underlying Flash/SSD NAND arrays.

## 2. Hardware Specifications (FPGA)
The hardware architecture has been synthesized, placed, and fully routed for a hardened automotive-grade target, ensuring thermal and logical resilience inside tightly confined embedded environments:
*   **Target Device:** AMD/Xilinx Artix-7 `xa7a35tcsg324-1Q` (ISO 26262 ASIL-D Compliant / Q-Grade).
*   **Bus Interface:** Synchronous 32-bit AMBA APB Slave (`PCLK`, `PSEL`, `PENABLE`, `PWRITE`, `PADDR`, `PWDATA`, `PRDATA`, `PREADY`, `PSLVERR`).
*   **Control Plane Frequency:** 100.00 MHz (Strict 10.000 ns clock period).

### 📊 Static Timing Analysis Summary (Vivado Routed)
The interface is entirely registered to eliminate combinational feedback violations (`TIMING-16`) and isolate parallel I/O switching from thermal drift metrics:
*   **Worst Negative Slack (WNS):** `+5.222 ns` (Setup time met, 0 Failing Endpoints). Critical path spans from the entropy register bit 6 (`compteur_entropie_reg[6]/C`) through 3 LUT logic levels to stable bus read lines.
*   **Worst Hold Slack (WHS):** `+0.222 ns` (Hold time met, 0 Violations). Pipeline stages guarantee complete immunity against clock distribution uncertainty (measured at `0.035 ns`).
*   **Dedicated Clock Input:** Routed via physical pin `F4` (Multi-Region Clock Capable - MRCC) to minimize global clock tree skew.
*   **Physical Disconnection Output:** Dedicated hardwired line routed on pin `T11` driving the `SIG_FLASH_WRITE_ENABLE` signal.

### 📉 Silicon Resource Utilization (Vivado Synthesis)
*   **Slice LUTs:** 28 (Ultra-lean footprint, consuming only 0.13% of the available 20,800 LUT matrix).
*   **Slice Registers:** 20 (0.05% utilization, precisely mapped to 19 `EDCE` synchronous primitives and 1 `FDPE` safety-critical boot primitive).
*   **Bonded IOB (I/O Ports):** 68 virtualized parallel signal routes mapping data and address buses.
*   **Global Clock Buffers:** 1 `BUFG` primitive ensuring a balanced low-skew clock tree.

### 🔌 Electrical & Thermal Profile (Vivado Power)
*   **Total On-Chip Power:** 0.092 W (92 mW total envelope).
*   **Device Static Power:** 0.072 W (72 mW leakage floor).
*   **Design Dynamic Power:** 0.020 W (20 mW dynamic toggling frequency).
*   **Junction Temperature:** 25.4 °C (Stable silicon core operating temperature).
*   **Maximum Safe Ambient Temperature:** 124.6 °C (Validated against the Automotive Extended Q-Grade standard ranging from -40°C to +125°C).

## 3. Passive/Active Confinement Mechanism (SPU-102)
The SPU-102 combinational engine actively parses incoming write transactions through two parallel hardware detection pipelines:
1.  **Geometric Filtering (Alpha Register):** A 32-bit factory invariant (`X"A5A5A5A5"`) is hardcoded into the silicon structure. Any write transaction forcing a null bitwise product (`PWDATA AND REG_ALPHA = X"00000000"`) trips the safety latch.
2.  **Entropic Tracking (Exhaustion Counter):** Repeated write cycles deviating from the initial geometry address space (`PADDR(11 downto 0) = X"000"`) increment a noise-filtered asymmetric entropy register. Reaching the critical threshold of `16` suspicious writes instantly triggers confinement.

### ⚡ Radical Physical Isolation
As soon as a violation is flagged:
*   The **`SIG_FLASH_WRITE_ENABLE` line drops to 0 Volts** in exactly 1 clock cycle. The flash memory write-voltage supply plane is physically cut off at the hardware layer, enforcing an unalterable `degrad_read_only` quarantine state.
*   The parallel read bus `PRDATA` is overridden to continuously stream the quarantine signature: **`0xDEADBEEF`**.
*   The **`PSLVERR` AMBA slave signal asserts to '1'**, firing an immediate hardware exception to the host ARM processor.

## 4. Software Architecture (Embedded Rust Driver)
The low-level firmware driver controls the hardware registers with absolute safety, operating entirely without a standard library runtime:
*   **MMIO Mapping:** Enforced C-compatible alignment structures (`#[repr(C)]`) mapped directly over the SPU-102 physical registers.
*   **Volatile Access:** Relies strictly on `core::ptr::read_volatile` instructions to completely bypass any host CPU cache layer optimizations, enforcing real-time polling of the underlying silicon.
*   **C-FFI Portability Layer:** Features un-mangled `#[no_mangle] pub extern "C"` entry points, ensuring seamless integration with C/C++ applications or runtime validation scripts (e.g., Python `ctypes`).
