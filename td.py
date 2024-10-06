import math
import random

critiques = {
    'Lisa Rose': {'Lady': 2.5, 'Snakes': 3.5, 'Luck': 3.0, 'Superman': 3.5, 'Dupree': 2.5, 'Night': 3.0},
    'Gene Seymour': {'Lady': 3.0, 'Snakes': 3.5, 'Luck': 1.5, 'Superman': 5.0, 'Dupree': 3.5, 'Night': 3.0},
    'Michael Phillips': {'Lady': 2.5, 'Snakes': 3.0, 'Superman': 3.5, 'Night': 4.0},
    'Claudia Puig': {'Snakes': 3.5, 'Luck': 3.0, 'Superman': 4.0, 'Dupree': 2.5, 'Night': 4.5},
    'Mick Lasalle': {'Lady': 3.0, 'Snakes': 4.0, 'Luck': 2.0, 'Superman': 3.0, 'Dupree': 2.0, 'Night': 3.0},
    'Jack Matthews': {'Lady': 3.0, 'Snakes': 4.0, 'Superman': 5.0, 'Dupree': 3.5, 'Night': 3.0},
    'Toby': {'Snakes': 4.5, 'Superman': 4.0, 'Dupree': 1.0},
    'Anne': {'Lady': 1.5, 'Luck': 4.0, 'Dupree': 2.0}
}
films_to_recommend = ["Snakes", "Superman", "Night"]
films = [f"Film{i}" for i in range(1, 21)]  # 20 films
critiquesModified = [f"Critique{i}" for i in range(1, 16)]  # 15 critiques



# 2(a)(i)
def sim_distanceManhattan(person1, person2):
    common_films = [film for film in person1 if film in person2]
    if not common_films:
        return 0

    sum_of_differences = sum(
        [abs(person1[film] - person2[film]) for film in common_films])
    return sum_of_differences


def sim_distanceEuclidienne(person1, person2):
    common_films = [film for film in person1 if film in person2]
    if not common_films:
        return 0

    sum_of_squares = sum([(person1[film] - person2[film])
                         ** 2 for film in common_films])
    return math.sqrt(sum_of_squares)


print(sim_distanceEuclidienne(
    critiques['Lisa Rose'], critiques['Gene Seymour']))

# 2(a)(ii)


def computeNearestNeighborM(nouveauCritique, Critiques):
    distances = []
    for critique in Critiques:
        if critique != nouveauCritique:
            distance = sim_distanceManhattan(Critiques[critique],
                                             Critiques[nouveauCritique])
            distances.append((distance, critique))
    distances.sort()
    return distances

def computeNearestNeighborE(nouveauCritique, Critiques):
    distances = []
    for critique in Critiques:
        if critique != nouveauCritique:
            distance = sim_distanceEuclidienne(Critiques[critique],
                                             Critiques[nouveauCritique])
            distances.append((distance, critique))
    distances.sort()
    return distances


def recommendM(nouveauCritique, Critiques):
    # retourner le voisin le plus proche de 'nouveauCritique'
    nearest = computeNearestNeighborM(nouveauCritique, Critiques)[0][1]
    recommendations = []

    for film in Critiques[nearest]:
        # retourner ts les films du plus proche voisin que 'nouveauCritique'
        if film not in Critiques[nouveauCritique]:
            # n'a pas vu
            recommendations.append((film, Critiques[nearest][film]))

    return sorted(recommendations, key=lambda x: x[1], reverse=True)

def recommendE(nouveauCritique, Critiques):
    # retourner le voisin le plus proche de 'nouveauCritique'
    nearest = computeNearestNeighborE(nouveauCritique, Critiques)[0][1]
    recommendations = []

    for film in Critiques[nearest]:
        # retourner ts les films du plus proche voisin que 'nouveauCritique'
        if film not in Critiques[nouveauCritique]:
            # n'a pas vu
            recommendations.append((film, Critiques[nearest][film]))

    return sorted(recommendations, key=lambda x: x[1], reverse=True)

# 2(b)(i)


def calculate_score_poids_normal(film, nouveauCritique, Critiques):
    total = 0
    sim_sum = 0
    for critique in critiques:
        if critique != nouveauCritique and film in Critiques[critique]:
            distance = sim_distanceManhattan(
                Critiques[critique], Critiques[nouveauCritique])
            weight = 1 / (1 + distance)
            total += weight * Critiques[critique][film]
            sim_sum += weight
    return total / sim_sum if sim_sum > 0 else 0


def Bestrecommend(nouveauCritique, Critiques,films_to_recommend):
    scores = [(film, calculate_score_poids_normal(film, nouveauCritique, critiques))
              for film in films_to_recommend if film not in Critiques[nouveauCritique]]
    if not scores:
        return None  # Aucune recommandation possible

    # Retourne le nom du film avec le score le plus élevé
    return max(scores, key=lambda x: x[1])[0]


def calculate_score_poids_square(film, nouveauCritique, Critiques):
    total = 0
    sim_sum = 0
    for critique in Critiques:
        if critique != nouveauCritique and film in Critiques[critique]:
            distance = sim_distanceManhattan(
                Critiques[critique], Critiques[nouveauCritique])
            weight = 1 / (1 + distance**2)  # poids square
            total += weight * Critiques[critique][film]
            sim_sum += weight
    return total / sim_sum if sim_sum > 0 else 0


def OtherBestrec(nouveauCritique, Critiques,films_to_recommend):
    scores = [(film, calculate_score_poids_square(film, nouveauCritique, critiques))
              for film in films_to_recommend if film not in Critiques[nouveauCritique]]
    if not scores:
        return None  # Aucune recommandation possible

    # Retourne le nom du film avec le score le plus élevé
    return max(scores, key=lambda x: x[1])[0]

def pearson(person1, person2):
    sum_xy=0
    sum_x=0
    sum_y=0
    sum_x2=0
    sum_y2=0
    n=0
    common_films = [film for film in person1 if film in person2]
    n = len(common_films)
    
    if n ==0 : 
        return 0
    for key in person1:
        if key in person2:
            n += 1
            x=person1[key]
            y=person2[key]
            sum_xy +=x*y
            sum_x += x
            sum_y += y
            sum_x2 += x**2
            sum_y2 += y**2
    denominator = math.sqrt(sum_x2 - (sum_x**2) / n) * math.sqrt(sum_y2 - (sum_y**2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) /n ) / denominator



def calculate_score_pearson(film, nouveauCritique, Critiques):
    total = 0
    sim_sum = 0
    for critique in Critiques:
        if critique != nouveauCritique and film in Critiques[critique]:
            similarity = pearson(
                Critiques[critique], Critiques[nouveauCritique])
            total += similarity * Critiques[critique][film]
            sim_sum += abs(similarity)
    return total / sim_sum if sim_sum > 0 else 0


def PearsonRecommend(nouveauCritique, Critiques,films_to_recommend):
    scores = [(film, calculate_score_pearson(film, nouveauCritique, Critiques))
              for film in films_to_recommend if film not in Critiques[nouveauCritique]]

    if not scores:
        return None  # Aucune recommandation possible

    # Retourne le nom du film avec le score le plus élevé
    return max(scores, key=lambda x: x[1])[0]


def cosinus_similarity(person1, person2):
    common_films = [film for film in person1 if film in person2]

    if not common_films:
        return 0

    sum_xy = sum([person1[film] * person2[film] for film in common_films])
    sum_x2 = sum([person1[film]**2 for film in common_films])
    sum_y2 = sum([person2[film]**2 for film in common_films])

    return sum_xy / (math.sqrt(sum_x2) * math.sqrt(sum_y2))


def calculate_score_cosinus(film, nouveauCritique, Critiques):
    total = 0
    sim_sum = 0
    for critique in Critiques:
        if critique != nouveauCritique and film in Critiques[critique]:
            similarity = cosinus_similarity(
                Critiques[critique], Critiques[nouveauCritique])
            total += similarity * Critiques[critique][film]
            sim_sum += similarity
    return total / sim_sum if sim_sum > 0 else 0


def CosinusRecommend(nouveauCritique, Critiques,films_to_recommend):
    scores = [(film, calculate_score_cosinus(film, nouveauCritique, Critiques))
              for film in films_to_recommend if film not in Critiques[nouveauCritique]]
    if not scores:
        return None  # Aucune recommandation possible
    # Retourne le nom du film avec le score le plus élevé
    return max(scores, key=lambda x: x[1])[0]

def calculate_score_jaccard(film, nouveauCritique, Critiques):
    scores = []
    for critique in Critiques:
        if critique != nouveauCritique and film in Critiques[critique]:
            set1 = set(Critiques[nouveauCritique].keys())
            set2 = set(Critiques[critique].keys())
            similarity = len(set1.intersection(set2)) / len(set1.union(set2))
            scores.append(similarity * Critiques[critique][film])
    return sum(scores) / len(scores) if scores else 0

def JaccardRecommend(nouveauCritique, Critiques, films_to_recommend):
    scores = [(film, calculate_score_jaccard(film, nouveauCritique, Critiques))
              for film in films_to_recommend if film not in Critiques[nouveauCritique]]
    if not scores:
        return None  # Aucune recommandation possible
    # Retourne le nom du film avec le score le plus élevé
    return max(scores, key=lambda x: x[1])[0]

def calculate_score_dice(film, nouveauCritique, Critiques):
    scores = []
    for critique in Critiques:
        if critique != nouveauCritique and film in Critiques[critique]:
            set1 = set(Critiques[nouveauCritique].keys())
            set2 = set(Critiques[critique].keys())
            similarity = 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))
            scores.append(similarity * Critiques[critique][film])
    return sum(scores) / len(scores) if scores else 0

def DiceRecommend(nouveauCritique, Critiques, films_to_recommend):
    scores = [(film, calculate_score_dice(film, nouveauCritique, Critiques))
              for film in films_to_recommend if film not in Critiques[nouveauCritique]]
    if not scores:
        return None  # Aucune recommandation possible
    # Retourne le nom du film avec le score le plus élevé
    return max(scores, key=lambda x: x[1])[0]

print(recommendE('Anne',critiques))
print(Bestrecommend('Anne', critiques,films_to_recommend))
print(OtherBestrec('Anne', critiques,films_to_recommend))
print(PearsonRecommend('Anne', critiques,films_to_recommend))
print(CosinusRecommend('Anne', critiques,films_to_recommend))


similarity_functions = [Bestrecommend,OtherBestrec,PearsonRecommend,CosinusRecommend,JaccardRecommend,DiceRecommend]
def recommend(nouveauCritique, Critiques, similar_func):
    # For recommendE and recommendM
    if similar_func in [recommendE, recommendM]:
        recommendations = similar_func(nouveauCritique, Critiques)
        return recommendations[0][0] if recommendations else None

    # For Bestrecommend, OtherBestrec, PearsonRecommend, CosinusRecommend
    elif similar_func in [Bestrecommend, OtherBestrec, PearsonRecommend, CosinusRecommend, JaccardRecommend, DiceRecommend]:
        # These functions expect a third argument films_to_recommend
        # Generate it here
        films_to_recommend = [film for film in films if film not in Critiques[nouveauCritique]]
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

# Adjust data for common recommendation with additional debug prints
# Adjust data for common recommendation with a maximum iteration limit
# Adjust data for common recommendation with additional debug prints
# Adjust data for common recommendation with additional debug prints
def adjust_data_for_common_recommendation(Critiques, similarity_functions, max_iterations=1000):
    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        print(f"Iteration: {iteration}")
        common_recommendation = find_common_recommendation(Critiques, similarity_functions)
        if common_recommendation:
            print(f"Common recommendation found: {common_recommendation}")
            return Critiques, common_recommendation

        # If no common recommendation, adjust the data slightly
        target_film = random.choice([film for film in films if film not in Critiques["NouveauCritique"]])
        print(f"Adjusting data for target film: {target_film}")
        for critique in Critiques:
            if critique != "NouveauCritique" and target_film in Critiques[critique]:
                Critiques[critique][target_film] = round(random.uniform(4.5, 5), 1)  # Favor this film
                print(f"Adjusted {critique}'s rating for {target_film} to {Critiques[critique][target_film]}")

    print("Maximum iterations reached without finding a common recommendation.")
    return Critiques, None  # Return None if no common recommendation is found within the limit


# Génération et ajustement des données
print("Génération et ajustement des données... 1")
Critiques = generate_data_with_constraints()
print("Génération et ajustement des données... 2")
Critiques, recommended_film = adjust_data_for_common_recommendation(Critiques, similarity_functions)
print("Génération et ajustement des données... 3")


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
