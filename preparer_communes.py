import geopandas as gpd

communes = gpd.read_file("donnees/communes_64_65.gpkg", layer="communes")
precis = gpd.read_file("donnees/communes_64_65.gpkg", layer="communes_precis")
coeur = gpd.read_file("donnees/pnp_coeur.geojson").to_crs(2154).geometry.union_all()
aire = gpd.read_file("donnees/pnp_aire_adhesion.geojson").to_crs(2154).geometry.union_all()

precis["surf_calc_km2"] = precis.area / 1e6
precis["coeur_km2"] = precis.intersection(coeur).area / 1e6
precis["aire_km2"] = precis.intersection(aire).area / 1e6

for champ in ("coeur_km2", "aire_km2"):
    precis.loc[precis[champ] < 0.01, champ] = 0.0

tab = communes.merge(precis[["code_insee", "surf_calc_km2", "coeur_km2", "aire_km2"]], on="code_insee")
tab = tab[(tab.coeur_km2 > 0) | (tab.aire_km2 > 0)].copy()
tab["part_coeur"] = (100 * tab.coeur_km2 / tab.surf_calc_km2).round(1)
tab["part_aire"] = (100 * tab.aire_km2 / tab.surf_calc_km2).round(1)
tab["coeur_km2"] = tab.coeur_km2.round(2)
tab["aire_km2"] = tab.aire_km2.round(2)
tab["statut"] = "aire seulement"

tab.loc[(tab.coeur_km2 > 0) & (tab.aire_km2 > 0), "statut"] = "cœur et aire"
tab.loc[(tab.coeur_km2 > 0) & (tab.aire_km2 == 0), "statut"] = "cœur seulement"
tab["departement"] = tab.departement.map({"64": "Pyrénées-Atlantiques (64)", "65": "Hautes-Pyrénées (65)"})

champs = ["code_insee", "nom", "departement", "population", "date_population", "surface_km2", "statut", "coeur_km2", "part_coeur", "aire_km2", "part_aire"]

tab = tab[champs + ["geometry"]].sort_values("code_insee")
tab.to_crs(4326).to_file("donnees/communes_parc.geojson", driver="GeoJSON", COORDINATE_PRECISION=5, engine="pyogrio")

points = tab.copy()

points["geometry"] = tab.representative_point()

points = points.sort_values("population", ascending=False)
points.to_crs(4326).to_file("donnees/communes_parc_points.geojson", driver="GeoJSON", COORDINATE_PRECISION=5, engine="pyogrio")

ecart = (tab.surface_km2 - tab.merge(precis[["code_insee", "surf_calc_km2"]], on="code_insee").surf_calc_km2.values).abs().max()

