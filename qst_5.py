similarity_functions = [recommendE,recommendM,Bestrecommend,OtherBestrec,PearsonRecommend,CosinusRecommend]
def recommend(nouveauCritique, Critiques, similar_func):
    # Pour recommendE et recommendM
    if similar_func in [recommendE, recommendM]:
        recommendations = similar_func(nouveauCritique, Critiques)
        return recommendations[0][0] if recommendations else None
    
    # Pour Bestrecommend, OtherBestrec, PearsonRecommend, CosinusRecommend
    elif similar_func in [Bestrecommend, OtherBestrec, PearsonRecommend, CosinusRecommend]:
        # Ces fonctions attendent un troisième argument films_to_recommend
        # Nous devons le générer ici
        films_to_recommend = [film for film in Critiques[list(Critiques.keys())[0]] 
                              if film not in Critiques[nouveauCritique]]
        return similar_func(nouveauCritique, Critiques, films_to_recommend)

def pourcentagecasesvides(Critiques):
    total_cases = len(Critiques) * len(films)
    cases_remplies = sum(len(critique) for critique in Critiques.values())
    return (1 - cases_remplies / total_cases) * 100


def generate_data_with_constraints():
    while True:
        Critiques = {}
        for critique in critiquesModified:
            Critiques[critique] = {}
            for film in films:
                if random.random() > 0.45:
                    Critiques[critique][film] = random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

        # Nouveau critique qui n'a pas vu au moins la moitié des films
        nouveau_critique = "NouveauCritique"
        Critiques[nouveau_critique] = {}
        films_vus = random.sample(films, random.randint(1, 10))  # Au plus 10 films vus (moins de la moitié)
        for film in films_vus:
            Critiques[nouveau_critique][film] = random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

        if 30 <= pourcentagecasesvides(Critiques) <= 60:
            return Critiques

def find_common_recommendation(Critiques, similarity_functions):
    nouveau_critique = "NouveauCritique"
    films_non_vus = [film for film in films if film not in Critiques[nouveau_critique]]
    
    for film in films_non_vus:
        if all(recommend(nouveau_critique, Critiques, func) == film for func in similarity_functions):
            return film
    
    return None

def adjust_data_for_common_recommendation(Critiques, similarity_functions):
    while True:
        common_recommendation = find_common_recommendation(Critiques, similarity_functions)
        if common_recommendation:
            return Critiques, common_recommendation

        # Si pas de recommandation commune, ajuster légèrement les données
        target_film = random.choice([film for film in films if film not in Critiques["NouveauCritique"]])
        for critique in Critiques:
            if critique != "NouveauCritique" and target_film in Critiques[critique]:
                Critiques[critique][target_film] = round(random.uniform(4.5, 5), 1)  # Favoriser ce film



# Génération et ajustement des données
Critiques = generate_data_with_constraints()
Critiques, recommended_film = adjust_data_for_common_recommendation(Critiques, similarity_functions)

# Vérification et affichage des résultats
nouveau_critique = "NouveauCritique"
films_vus = len(Critiques[nouveau_critique])
pourcentage_vide = pourcentagecasesvides(Critiques)

print(f"Nombre de films vus par le nouveau critique : {films_vus}")
print(f"Pourcentage de cases vides : {pourcentage_vide:.2f}%")
print(f"Film recommandé : {recommended_film}")

# Vérification finale
recommendations = [recommend(nouveau_critique, Critiques, func) for func in similarity_functions]
print(f"Toutes les recommandations sont identiques : {len(set(recommendations)) == 1}")
print(f"Recommandations : {recommendations}")
