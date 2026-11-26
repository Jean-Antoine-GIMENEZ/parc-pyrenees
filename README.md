# Portrait des communes du Parc national des Pyrénées

### Fichier

- `index.html` : la carte (MapLibre GL 6.16)
- `preparer_communes.py` : calcule les croisements communes × Parc et écrit les deux GeoJSON
- `donnees/communes_parc.geojson` : les 69 communes retenues (polygones)
- `donnees/communes_parc_points.geojson` : les mêmes communes en points, pour les cercles de population
- `donnees/communes_64_65.gpkg`, `pnp_coeur.geojson`, `pnp_aire_adhesion.geojson` : données sources (voir `LISEZMOI.txt`)

## 1. Choix

Une commune est retenue si au moins de 1 ha de son territoire se trouve dans le cœur ou dans l'aire d'adhésion du Parc.

- Les intersections sont calculées en Lambert-93.
- Les parts sont rapportées à la surface recalculée sur le tracé précis, pour que numérateur et dénominateur viennent de la même géométrie.

Résultat : 69 communes (51 dans les Hautes-Pyrénées, 18 dans les Pyrénées-Atlantiques), réparties ainsi :

| Statut | Communes |
|---|---|
| aire d'adhésion seulement | 55 |
| cœur et aire d'adhésion | 10 |
| cœur seulement (le reste hors aire d'adhésion) | 4 |

## 2. Limites

- Le cercle n'est pas placé là où vivent les gens. Il est sur un point intérieur choisi géométriquement, pas sur le chef-lieu.
- L'aplat colore toute la commune, y compris sa partie hors du Parc.
- Une part n'est pas une surface. Les km² ne sont donnés que dans la fiche.
- L'aire d'adhésion vient de la couche DREAL. Une commune « cœur seulement » a du cœur sur son territoire, mais le reste de son territoire n'est pas en aire d'adhésion dans cette couche.
- Les seuils 15 / 30 / 45 % sont arbitraires.
- Les dates diffèrent : population 2022, limites communales 2026, limites du Parc validées en 2024.

## Sources et crédits

- Communes : IGN, ADMIN EXPRESS COG CARTO PE et ADMIN EXPRESS COG, édition 2026. Population : INSEE, population municipale (via ADMIN EXPRESS). Licence Ouverte 2.0.
- Cœur et aire d'adhésion : DREAL Nouvelle-Aquitaine, WFS SIGENA, couche `n_enp_pn_s_r75`, validation du 15/09/2024. Licence Ouverte 2.0.
- Fonds : Plan IGN, BD ORTHO © IGN. Relief : © Mapterhorn.
