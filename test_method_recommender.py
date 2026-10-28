
from backend.services.method_recommender import recommend_method

profile_with_preference = {
    "learning_mode": "music",
    "learning_consistency": "regular",
    "goal": "Improve vocabulary",
    "previous_level": "B1",
}

profile_without_preference = {
    "learning_mode": "self-study",
    "learning_consistency": "sometimes",
    "goal": "Improve vocabulary",
    "previous_level": "B1",
}

print("TEST 1: Explicit preference")
print(recommend_method(profile_with_preference))

print("\nTEST 2: No explicit method preference")
print(recommend_method(profile_without_preference))
