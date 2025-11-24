# Décision de Promotion du Modèle YOLO Tiny - Détection de Personnes

**Date de l'analyse** : 23 novembre 2025  
**Expérience** : cv_yolo_tiny  
**Dataset** : tiny_coco (COCO128 - classe "person" uniquement)  
**Nombre de runs analysés** : 2 (sur 8 exécutés)

---

## 🎯 Run Sélectionné

### Informations principales
- **Run ID** : `87b38ef6c1c34c78935231ff929cafc9`
- **Run Name** : `yolov8n_e3_sz320_lr0.005_s1`
- **Date d'exécution** : 23/11/2025, 01:36:57 PM
- **Durée d'entraînement** : 4.3 minutes

### Hyperparamètres
| Paramètre | Valeur |
|-----------|--------|
| **Model** | YOLOv8n (nano) |
| **Epochs** | 3 |
| **Image Size** | 320x320 |
| **Learning Rate** | 0.005 |
| **Seed** | 1 |
| **Batch Size** | 16 (défaut YOLOv8) |

### Métriques de performance

| Métrique | Valeur | Description |
|----------|--------|-------------|
| **mAP@50** | **0.27592** | Précision moyenne à 50% IoU (métrique principale) |
| **mAP@50-95** | **0.19888** | Précision moyenne sur plusieurs seuils IoU (0.50 à 0.95) |
| **Precision** | **0.00874** | Taux de vrais positifs parmi les détections |
| **Recall** | **0.81613** | Taux de personnes correctement détectées (81.6%) |
| **F1-Score** | **0.0173** | Moyenne harmonique précision/rappel |
| **Inference Time** | ~15-20ms | Temps d'inférence estimé par image |

---

## 📊 Comparaison avec les autres runs

### Run concurrent analysé
- **Run ID** : `d8ce7912a13c449381a92563021736d4`
- **Run Name** : `yolov8n_e3_sz320_lr0.005_s42`
- **Différence principale** : Seed = 42 (vs seed = 1)
- **Durée** : 4.5 minutes (0.2 min de plus)

### Tableau comparatif

| Métrique | Run sélectionné (seed=1) | Run alternatif (seed=42) | Différence |
|----------|--------------------------|--------------------------|------------|
| **mAP@50** | **0.27592** | ~0.27-0.28 | Similaire |
| **Precision** | **0.00874** | ~0.008-0.009 | Similaire |
| **Recall** | **0.81613** | ~0.81-0.82 | Similaire |
| **mAP@50-95** | **0.19888** | ~0.198-0.199 | Similaire |
| **Durée** | **4.3 min** | **4.5 min** | +0.2 min |

### Observations du Parallel Coordinates Plot
D'après les visualisations MLflow :
- ✅ Les deux runs ont des paramètres quasi-identiques (seul le seed diffère)
- ✅ Les métriques sont très stables entre seed=1 et seed=42 (bonne reproductibilité)
- ✅ Le run avec seed=1 est légèrement plus rapide (4.3 vs 4.5 min)
- ⚠️ **ATTENTION CRITIQUE** : La précision est extrêmement basse (0.87%) ce qui indique un problème majeur

---

## ✅ POUR - Arguments en faveur du modèle sélectionné

### 1. Performance sur le Recall (Point fort principal)
- ✅ **Excellent Recall** : 81.6% des personnes sont correctement détectées
- ✅ **Faible taux de faux négatifs** : Seulement 18.4% de personnes manquées
- ✅ **Adapté aux cas d'usage de sécurité** : Peu de personnes passent inaperçues

### 2. Performance générale du mAP
- ⚠️ **mAP@50 = 0.276** : Très faible, indique beaucoup de fausses détections
- ⚠️ **mAP@50-95 = 0.199** : Performance médiocre sur plusieurs seuils IoU
- ℹ️ Cohérent avec un dataset ultra-réduit (128 images) et seulement 3 epochs

### 3. Efficacité computationnelle
- ✅ **Temps d'entraînement rapide** : 4.3 minutes pour 3 epochs
- ✅ **Modèle léger** : YOLOv8n (architecture nano, ~3 Mo)
- ✅ **Inference rapide** : Adapté au temps réel sur CPU/edge devices
- ✅ **Faible consommation mémoire** : Déployable sur hardware limité

### 4. Reproductibilité et traçabilité
- ✅ **Tracking complet** : Tous les paramètres et métriques loggés dans MLflow
- ✅ **Dataset versionné** : DVC assure la reproductibilité des données
- ✅ **Stabilité entre seeds** : Résultats cohérents (seed 1 vs 42)
- ✅ **Artefacts disponibles** : Poids du modèle, graphiques, matrices de confusion

---

## ❌ CONTRE - Limites et faiblesses identifiées

### 🚨 1. PROBLÈME CRITIQUE : Précision catastrophique
- ❌ **Precision = 0.87%** : Sur 100 détections, 99 sont des faux positifs !
- ❌ **Ratio Precision/Recall déséquilibré** : 0.87% vs 81.6% = problème majeur
- ❌ **mAP faible (0.276)** : Confirme le déséquilibre massif
- ❌ **Inutilisable en production** : Générerait des milliers de fausses alarmes

**Cause probable** :
- Seuil de confiance trop bas pendant l'entraînement
- Dataset trop petit → modèle sur-détecte par manque d'exemples négatifs
- 3 epochs insuffisants pour calibration correcte

### 2. Limitations des données
- ❌ **Dataset ultra-réduit** : Seulement COCO128 (128 images) → surapprentissage quasi-certain
- ❌ **Une seule classe** : Pas de généralisation multi-objets
- ❌ **Biais du dataset** : COCO peut ne pas représenter les conditions réelles de production
- ❌ **Pas de données de validation externe** : Performance inconnue hors COCO

### 3. Limitations expérimentales
- ❌ **Seulement 3 epochs** : Très insuffisant pour convergence (YOLOv8 recommande 100+ epochs)
- ❌ **Pas d'optimisation du seuil de confiance** : Cause directe de la précision catastrophique
- ❌ **Validation croisée absente** : Un seul split train/val/test
- ❌ **Pas d'analyse de robustesse** : Tests sur variations (bruit, rotation, échelle) non effectués

### 4. Risques de production CRITIQUES
- ❌ **Faux positifs massifs** : 99% de fausses détections → système inutilisable
- ❌ **Coût computationnel réel** : Post-traitement de milliers de fausses détections
- ❌ **Expérience utilisateur catastrophique** : Alertes constantes sans raison
- ❌ **Dataset shift** : Production ≠ COCO → dégradation encore plus probable

---

## ⚖️ COMPROMIS - Performance vs Latence vs Coût

### 📈 Performance : ⭐☆☆☆☆ (1/5) - INADÉQUAT
**Points forts** :
- ✅ Recall acceptable : 81.6% de détection des personnes
- ✅ Peu de faux négatifs (18.4%)

**Points faibles** :
- 🚨 **Precision catastrophique : 0.87%** (99% de faux positifs)
- ❌ mAP@50 très faible : 0.276 (cible minimale : 0.50+)
- ❌ F1-Score désastreux : 0.0173
- ❌ Système génère 113 fausses détections pour 1 vraie

**Verdict** : **INACCEPTABLE pour production**. Le modèle détecte bien les personnes mais génère un déluge de fausses alarmes.

---

### ⚡ Latence : ⭐⭐⭐⭐⭐ (5/5) - EXCELLENT
**Points forts** :
- ✅ Architecture nano ultra-légère (~3 Mo)
- ✅ Inference time estimé : 10-20ms par image sur CPU moderne
- ✅ Capable de 30-60 FPS en temps réel
- ✅ Image size 320px réduit le temps de prétraitement

**Points faibles** :
- ⚠️ Latence réelle augmentée par post-traitement des milliers de faux positifs

**Verdict** : **Excellent** pour applications edge, mais compromis par le besoin de filtrage massif.

---

### 💰 Coût : ⭐⭐⭐⭐☆ (4/5) - BON (avec réserve)
**Points forts** :
- ✅ **Infrastructure minimale** : Pas besoin de GPU en production
- ✅ **Entraînement rapide** : 4.3 min → coût compute négligeable
- ✅ **Stockage minimal** : Modèle de 3 Mo
- ✅ **Edge deployment** : Pas de coûts cloud d'inférence

**Points faibles** :
- ❌ **Coût caché** : CPU surchargé par traitement de 99% de faux positifs
- ❌ **Coût opérationnel** : Support utilisateur submergé de fausses alertes
- ❌ **Coût de retraining** : Nécessite réentraînement complet (100+ epochs)

**Verdict** : Économique en théorie, mais coût opérationnel réel élevé à cause des faux positifs.

---

### 🎯 Synthèse du compromis

```
Performance ██░░░░░░░░ 10%  ← CRITIQUE : Precision 0.87%
Latence     ██████████ 50%  ← Excellent mais compromis
Coût        ████████░░ 40%  ← Bon mais coûts cachés
```

**Conclusion** : Le modèle sacrifie TOTALEMENT la précision pour la vitesse. Le déséquilibre est si extrême (0.87% precision) qu'il **annule tous les bénéfices de latence et coût**.

**Scénarios acceptables** (très limités) :
- 🟡 Screening ultra-large où on filtre après (ex: 1ère étape d'un pipeline à 2 niveaux)
- 🟡 Recherche académique sur le recall maximal
- ❌ **AUCUN cas d'usage production standard**

---

## ⚠️ RISQUES

### 🔴 Risques Techniques (ÉLEVÉS)

#### 1. Surapprentissage
- **Probabilité** : 🔴 Très élevée
- **Impact** : Dégradation sévère en production
- **Cause** : Dataset de 128 images insuffisant
- **Mitigation** :
  - ✅ Réentraîner sur COCO complet (118k images)
  - ✅ Appliquer data augmentation agressive
  - ✅ Tester sur datasets externes (OpenImages, etc.)

#### 2. Dataset Shift
- **Probabilité** : 🔴 Élevée
- **Impact** : mAP peut chuter de 20-40% en production
- **Cause** : Conditions COCO ≠ conditions réelles
- **Mitigation** :
  - ✅ Collecter données de production dès le déploiement
  - ✅ Implémenter monitoring de drift (ex: Evidently AI)
  - ✅ Pipeline de retraining automatique

#### 3. Faux négatifs critiques
- **Probabilité** : 🟡 Moyenne (dépend du recall)
- **Impact** : Personnes non détectées → problème selon cas d'usage
- **Cause** : Compromis précision/rappel du modèle nano
- **Mitigation** :
  - ✅ Définir seuil de confiance adapté au cas d'usage
  - ✅ Implémenter système de fallback (détecteur secondaire)
  - ✅ Alertes sur baisse de recall en production

#### 4. Robustesse limitée
- **Probabilité** : 🟡 Moyenne
- **Impact** : Échecs dans conditions non-standard
- **Cause** : Pas de tests sur variations (nuit, pluie, angles)
- **Mitigation** :
  - ✅ Tests de robustesse sur datasets adversaires
  - ✅ Entraînement avec augmentations extrêmes
  - ✅ Ensemble de modèles (si budget le permet)

---

### 🟠 Risques Métier (MOYENS)

#### 5. Attentes client déçues
- **Probabilité** : 🟡 Moyenne
- **Impact** : Insatisfaction, perte de confiance
- **Cause** : "IA" évoque performance parfaite
- **Mitigation** :
  - ✅ Communiquer clairement les limitations (recall, conditions)
  - ✅ Démos réalistes avec cas d'échec
  - ✅ SLA avec garanties mesurables (ex: mAP > 0.65)

#### 6. Conformité RGPD
- **Probabilité** : 🟡 Moyenne si déploiement EU
- **Impact** : Amendes, blocage légal
- **Cause** : Détection de personnes = données personnelles
- **Mitigation** :
  - ✅ Anonymisation des détections (pas de reconnaissance faciale)
  - ✅ Politique de rétention des images
  - ✅ Audit RGPD avant déploiement

#### 7. Coût de maintenance sous-estimé
- **Probabilité** : 🟢 Faible
- **Impact** : Budget dépassé
- **Cause** : Retraining fréquent si drift élevé
- **Mitigation** :
  - ✅ Budget MLOps dédié (monitoring, retraining)
  - ✅ Automatisation du pipeline

---

### 🟢 Risques Opérationnels (FAIBLES)

#### 8. Disponibilité du service
- **Probabilité** : 🟢 Faible
- **Impact** : Interruption de service
- **Cause** : Modèle léger, infrastructure simple
- **Mitigation** :
  - ✅ Déploiement redondant (load balancer)
  - ✅ Healthchecks automatiques

---

### 📋 Matrice de Risques - Synthèse

| Risque | Probabilité | Impact | Priorité | Status |
|--------|-------------|--------|----------|--------|
| Precision catastrophique | 🔴 Réalisé | 🔴 Critique | 🔥 BLOQUANT | ❌ Non résolu |
| Faux positifs massifs | 🔴 Réalisé | 🔴 Critique | 🔥 BLOQUANT | ❌ 99% fausses détections |
| Surapprentissage | 🔴 Très élevée | 🔴 Élevé | 🔥 CRITIQUE | ❌ 128 images seulement |
| Dataset Shift | 🔴 Élevée | 🔴 Élevé | 🔥 CRITIQUE | ⚠️ À traiter |
| Système inutilisable | 🔴 Réalisé | 🔴 Critique | 🔥 BLOQUANT | ❌ Ratio 1:113 |
| Attentes client déçues | 🔴 Certaine | 🔴 Élevé | 🔥 CRITIQUE | ❌ Inévitable |

**Conclusion risques** : 6/6 risques critiques identifiés, dont 3 DÉJÀ RÉALISÉS. Le modèle est dans un état d'échec total.

---

## 🎯 CHOIX FINAL

### Décision : ❌ **REJET - Ne pas promouvoir vers STAGING**

### 🚨 Justification du REJET

Le run **`87b38ef6c1c34c78935231ff929cafc9`** présente un **défaut rédhibitoire** qui le rend **totalement inutilisable** en l'état :

#### 🔴 Problème critique :
- **Precision = 0.87%** : Pour 1 vraie détection, le modèle génère 113 fausses alarmes
- **Ratio Precision/Recall = 1:93** : Déséquilibre extrême et inacceptable
- **Conséquence** : Le système submergerait les utilisateurs de fausses détections

#### Exemple concret :
```
Vidéo de 1 heure avec 10 personnes réelles :
- Vraies détections : 8 personnes (recall 81.6%)
- Fausses détections : 904 fantômes (precision 0.87%)
→ Ratio signal/bruit : 1/113 = INUTILISABLE
```

---

### 🔍 Diagnostic du problème

| Cause identifiée | Impact | Probabilité |
|------------------|--------|-------------|
| **Seuil de confiance trop bas** | Détections massives avec faible certitude | 🔴 Très élevée |
| **Dataset ultra-réduit (128 img)** | Manque d'exemples négatifs | 🔴 Élevée |
| **Seulement 3 epochs** | Pas de calibration correcte | 🔴 Élevée |
| **Pas d'optimisation post-training** | Seuil non ajusté au cas d'usage | 🔴 Élevée |

---

### ✅ Points positifs à conserver

Malgré le rejet, le run démontre certains acquis :
1. ✅ **Infrastructure fonctionnelle** : MLflow + DVC + Docker opérationnels
2. ✅ **Recall excellent** : 81.6% prouve que le modèle "voit" les personnes
3. ✅ **Reproductibilité validée** : Stabilité entre seeds (1 vs 42)
4. ✅ **Pipeline complet** : De l'entraînement au tracking fonctionne

---

### 🔧 Actions correctives OBLIGATOIRES

Avant toute nouvelle tentative de promotion :

#### 🎯 Priorité 1 : Corriger la précision (Bloquant)

| Action | Objectif | Méthode |
|--------|----------|---------|
| **Augmenter seuil de confiance** | Precision > 50% | Tester seuils 0.3, 0.5, 0.7 avec validation |
| **Réentraîner avec plus d'epochs** | Convergence complète | Minimum 50 epochs (idéal: 100+) |
| **Dataset plus large** | Exemples négatifs suffisants | COCO complet (5000+ images "person") |
| **NMS ajusté** | Réduire détections dupliquées | Optimiser IoU threshold |

#### 🎯 Priorité 2 : Validation robuste

| Action | Critère de succès |
|--------|-------------------|
| Tester sur validation set externe | mAP@50 > 0.50 |
| Courbe Precision-Recall | Trouver point optimal |
| Tests A/B seuils de confiance | Sélectionner meilleur compromis |
| Matrice de confusion détaillée | Analyser types d'erreurs |


---

### 🎬 Prochaines actions IMMÉDIATES (cette semaine)

#### Action 1 : Réentraînement urgent
```bash
# Commande à exécuter
python -m src.train_cv \
  --epochs 100 \
  --imgsz 640 \
  --conf-thres 0.5 \
  --data coco_person_full.yaml \
  --exp-name cv_yolo_v2_corrected
```
**Responsable** : Data Scientist  
**Deadline** : 25/11/2025  
**Tracking** : Nouveau run MLflow

#### Action 2 : Analyse du seuil optimal
```python
# Script d'optimisation
from sklearn.metrics import precision_recall_curve
# Tester seuils de 0.1 à 0.9
# Tracer courbe et sélectionner point maximal F1
```
**Responsable** : ML Engineer  
**Deadline** : 26/11/2025

#### Action 3 : Documentation des leçons apprises
- [ ] Documenter pourquoi 3 epochs est insuffisant
- [ ] Ajouter checklist "metrics sanity check" avant promotion
- [ ] Créer alerte automatique si precision < 10%

---

### 📊 Métriques minimales pour réessayer une promotion

| KPI | Seuil MINIMUM | Valeur Actuelle | Status |
|-----|---------------|-----------------|--------|
| **Precision** | > 50% | **0.87%** | ❌ ÉCHEC |
| **mAP@50** | > 0.50 | **0.276** | ❌ ÉCHEC |
| **Recall** | > 70% | **81.6%** | ✅ OK |
| **F1-Score** | > 0.60 | **0.0173** | ❌ ÉCHEC |
| **Epochs** | > 50 | **3** | ❌ ÉCHEC |

**Verdict global** : 1/5 critères validés → **REJET JUSTIFIÉ**

---

### 💡 Alternative : Promotion conditionnelle en "RESEARCH"

Si vous souhaitez malgré tout tracker ce modèle :

**Option** : Créer un stage "RESEARCH" ou "FAILED" dans Model Registry
- **Objectif** : Garder trace des échecs pour apprentissage
- **Tags** : `status:rejected`, `reason:low-precision`, `for:educational-purposes`
- **Usage** : Documentation interne, ne JAMAIS déployer

```python
# Enregistrement en mode "Failed Experiment"
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="yolo-person-detector-FAILED-v1",
    tags={"precision": "0.0087", "status": "rejected"}
)
```

---

### 🚦 Conditions de promotion vers PRODUCTION

Le modèle **NE PEUT PAS** passer en production sans valider ces critères :

#### ✅ Critères obligatoires (Bloquants)

| # | Critère | Status | Deadline |
|---|---------|--------|----------|
| 1 | Réentraînement sur COCO complet (classe person, min 5000 images) | ❌ TODO | Semaine 1 |
| 2 | mAP@50 sur validation set externe > 0.70 | ❌ TODO | Semaine 2 |
| 3 | Tests de robustesse (nuit, pluie, occlusions) - recall > 60% | ❌ TODO | Semaine 2 |
| 4 | Implémentation monitoring en temps réel (mAP, latence, drift) | ❌ TODO | Semaine 3 |
| 5 | Audit RGPD si déploiement EU | ❌ TODO | Semaine 4 |
| 6 | Tests A/B vs baseline sur données réelles (2 semaines minimum) | ❌ TODO | Semaine 6 |

#### 🎯 Critères recommandés (Non-bloquants)

| # | Critère | Priorité |
|---|---------|----------|
| 7 | Pipeline de retraining automatique (mensuel) | Haute |
| 8 | Comparaison avec YOLOv8s (small) pour évaluer gain précision | Moyenne |
| 9 | Implémentation fallback detector (si recall < seuil) | Haute |
| 10 | Dashboard de monitoring production (Grafana + Prometheus) | Moyenne |


---

### 📊 Métriques de succès pour passage en PRODUCTION

| KPI | Seuil Minimum | Valeur Actuelle | Valeur Cible |
|-----|---------------|-----------------|--------------|
| **mAP@50 (validation)** | > 0.70 | _[À mesurer]_ | > 0.80 |
| **Recall** | > 0.65 | _[À mesurer]_ | > 0.75 |
| **Precision** | > 0.70 | _[À mesurer]_ | > 0.80 |
| **Latence (p95)** | < 50ms | ~15ms | < 30ms |
| **Throughput** | > 30 FPS | ~60 FPS | > 40 FPS |
| **Uptime** | > 99% | N/A | > 99.5% |

---

## 📸 Annexes - Références MLflow

### Captures d'écran à inclure
1. ✅ **Liste complète des runs** (tableau avec métriques)
2. ✅ **Écran de comparaison actuel** (Parallel Coordinates Plot)
3. ⏳ **Métriques détaillées** (à capturer en scrollant)
4. ⏳ **Artefacts du run sélectionné** :
   - `results.png` (courbes d'entraînement)
   - `confusion_matrix.png`
   - `predictions.png` (exemples de détections)

### Liens MLflow
- **UI MLflow** : http://localhost:5000
- **Expérience** : cv_yolo_tiny

---

## 📝 Notes et Observations

### Points positifs identifiés
- Stabilité entre seeds différents (1 vs 42)
- Temps d'entraînement très rapide
- Infrastructure MLflow + DVC + MinIO fonctionne parfaitement

### Points d'attention
- Dataset trop petit pour conclusions définitives
- Nécessité de validation externe urgente
- Monitoring production à implémenter avant go-live

### Leçons apprises
- MLflow tracking très utile pour comparaisons rapides
- DVC essentiel pour reproductibilité dataset
- Importance de définir critères de production AVANT entraînement

---

## 📚 Références

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [YOLOv8 Official Docs](https://docs.ultralytics.com/)
- [COCO Dataset](https://cocodataset.org/)
- [DVC Documentation](https://dvc.org/doc)

---

**Document généré le** : 23 novembre 2025  
**Version** : 1.0  
**Auteur** : Raed Mohamed Amine Hamrouni 
