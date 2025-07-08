import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from property_apps.models import Property


def _parse_address(address: str):
    """
    Parse address like:
    'Bhadrakali, Pokhara' → ('bhadrakali', 'pokhara')
    'Lamachaur, Pokhara, Kaski' → ('lamachaur', 'pokhara')
    'Prithvichowk, Pokhara' → ('prithvichowk', 'pokhara')
    """
    if not address:
        return "", ""

    parts = [p.strip().lower() for p in address.split(",")]
    locality = parts[0] if len(parts) > 0 else ""
    city = parts[1] if len(parts) > 1 else parts[0]  # fallback to locality
    return locality, city


def _build_feature_vector(property_obj):
    """
    Create a feature list: [locality * 2, city, property_type]
    This boosts the weight of locality during similarity scoring.
    """
    locality, city = _parse_address(property_obj.address)
    property_type = property_obj.property_type.lower()
    return [locality, locality, city, property_type]


def get_property_features():
    properties = list(Property.objects.all())
    feature_matrix = [_build_feature_vector(prop) for prop in properties]
    return np.array(feature_matrix), properties


def recommend_similar_properties(user_favorites, top_n=5):
    if not user_favorites:
        return []

    # Extract all features and property list
    all_features, all_properties = get_property_features()

    # Features for user's favorite properties
    favorite_features = np.array([
        _build_feature_vector(fav.property)
        for fav in user_favorites
    ])

    # Stack for one-hot encoding
    combined = np.vstack([all_features, favorite_features])

    # One-hot encode all categorical features
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(combined)

    all_encoded = encoded[:len(all_features)]
    fav_encoded = encoded[len(all_features):]

    # Calculate average cosine similarity
    similarity_scores = cosine_similarity(fav_encoded, all_encoded).mean(axis=0)
    sorted_indices = np.argsort(-similarity_scores)

    favorite_ids = set(f.property.id for f in user_favorites)

    # ✅ Create sets of allowed localities and cities based on favorites
    allowed_localities = set()
    allowed_cities = set()
    for fav in user_favorites:
        locality, city = _parse_address(fav.property.address)
        if locality:
            allowed_localities.add(locality)
        if city:
            allowed_cities.add(city)

    # Select recommendations that match locality first, or city
    recommendations = []
    for idx in sorted_indices:
        prop = all_properties[idx]
        if prop.id in favorite_ids:
            continue

        locality, city = _parse_address(prop.address)
        if locality in allowed_localities or city in allowed_cities:
            recommendations.append(prop)

        if len(recommendations) >= top_n:
            break

    return recommendations
