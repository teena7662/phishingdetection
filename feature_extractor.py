
import re

def extract_features(url):
    features = {}
    features['length'] = len(url)
    features['has_https'] = int('https' in url)
    features['count_dots'] = url.count('.')
    return list(features.values())
