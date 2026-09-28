# 🧠 REIO-AI — Superviseur Paracohérent pour Calcul Neuromorphique

REIO-AI est un module de supervision logique matériel (IP Core) conçu pour intercepter les hallucinations cognitives, les dérives de registres et les attaques adverses sur les architectures NPU/TPU embarquées.

### 🔬 Architecture Spécifique & Invariant V6-Alpha

Le superviseur s'interpose directement sur les flux de probabilités neuronales à la nanoseconde près :
* **Filtre Anti-Hallucination :** Analyse en continu la congruence logique des prémisses neuronales. Si deux neurones antagonistes sont activés simultanément (contradiction logique absolue), le circuit engage la rupture.
* **Confinement Éclair (1 Cycle) :** La détection d'une contradiction force le passage immédiat de la FSM dans l'état de sécurité `ST_HALT` en exactement 10 ns (1 cycle à 100 MHz).
* **Isolation Active :** Le bus de données de sortie est écrasé instantanément pour renvoyer le tag de quarantaine immuable `0xDEADBEEF`, protégeant le système global contre toute décision aberrante.

### 🚀 Validation du Pilote Logiciel (Intégration Rust / Python FFI)

L'exécution de la suite de tests unitaires sur le plan de contrôle en Rust bare-metal (`#![no_std]`) certifie la conformité de l'infrastructure :
* **Test 1 (Flux Standard) :** Transmission transparente et stabilisée de la donnée du neurone sain (`0x2a`).
* **Test 2 (Contradiction NPU) :** Isolation active et forçage immédiat du bus sur le tag protecteur `0xdeadbeef`.
* **Test 3 (Erreur Pointeur) :** Robustesse logicielle validée avec succès face à l'injection d'une adresse NULL.

🔐 **Note de Sûreté et Propriété Intellectuelle** : Les architectures internes de ce bloc de protection neuromorphique sont confidentielles et soumises aux accords de licence Open-Core. Les rapports physiques de CAO Vivado (.rpt) et les chronogrammes restent publiquement accessibles aux auditeurs.
