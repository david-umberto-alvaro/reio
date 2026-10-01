# REIO V3 — ARCHIVES ARCHITECTURE PÉRIPHÉRIQUES FRAGMENTÉS

## 🏛️ Registre de Spécification et d'Attestation Métrologique (Historique)

Ce répertoire regroupe les rapports de certification, les cartographies de registres et l'analyse de sûreté de fonctionnement de la génération REIO V3. Cette version historique était basée sur une approche modulaire à périphériques fragmentés avant la transition vers le bloc monolithique de la V4 Fractal.

### 📁 Index de la Documentation Technique V3
Pour consulter les détails d'ingénierie de cette génération, accédez directement aux documents d'attestation :
*   🔌 **Brochage et Cartographie MMIO :** [`datasheet.md`](./datasheet.md)
*   🛡️ **Rapport de Conformité Réglementaire :** [`COMPLIANCE.md`](./COMPLIANCE.md)
*   📊 **Analyse des Modes de Défaillance :** [`FMEDA.md`](./FMEDA.md)

### 📊 Performances Physiques Certifiées (Génération Historique)
Les rapports d'usine Vivado post-routage pour cette version modulaire avaient validé les métriques suivantes :
*   **Worst Negative Slack (WNS) :** **+4,723 ns** sur le domaine synchrone à 100 MHz.
*   **Surface Logique Occupée :** **89 Slice LUTs** et **65 Registres (FF)**.
*   **Enveloppe Thermique :** Consommation dynamique active mesurée à **6 mW**.
