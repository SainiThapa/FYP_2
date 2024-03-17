import math
import re
# from nltk.corpus import stopwords
import numpy as np

with open('C:/Users/Lenovo/Desktop/Lawyer/FYP/Lawyer/Feature1/stopwords.txt', 'r') as file:
    stopwords = file.readlines()
STOP_WORDS = [word.strip() for word in stopwords]

# STOP_WORDS = set(["the", "and", "is", "in", "it", "to", "of", "this", "that", "for","lawyer"])

def remove_special_characters(word):
    pattern = r"[^\w\s]"
    cleaned_word = re.sub(pattern, "", word)
    return cleaned_word

def calculate_tf(terms):
    tf_dict = {}
    total_terms = len(terms)
    for term in terms:
        term = remove_special_characters(term)
        if term not in tf_dict:
            tf_dict[term] = 0
        tf_dict[term] += 1 / total_terms
    return tf_dict

def calculate_idf(term, cleaned_documents):
    term = remove_special_characters(term).strip().lower()
    num_documents_with_term = sum(
        1 for document in cleaned_documents if term in document.lower()
    )

    if num_documents_with_term > 0:
        log_result = 1 + math.log(
            len(cleaned_documents) / num_documents_with_term
        )  # 1 is added for smoothing
        return log_result
    else:
        return 0

def preprocess(file):
    terms = re.split(r'[,\s]+', file)
    cleaned_terms = [
        remove_special_characters(term)
        for term in terms
        if term.lower() not in STOP_WORDS
    ]
    return cleaned_terms

def clean_files(files):
    cleaned_files = [
        " ".join(preprocess(file)) for file in files.values()
    ]
    return cleaned_files

def tf_idf_vectorize(document, vocabulary, cleaned_documents):
    terms = preprocess(document)
    tf_idf_vector = np.zeros(len(vocabulary))
    tf = calculate_tf(terms)

    for i, term in enumerate(vocabulary):
        term = remove_special_characters(term)
        if term in tf:
            tf_idf_vector[i] = tf[term] * calculate_idf(term, cleaned_documents)
    return tf_idf_vector

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # Check for zero division
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    else:
        return dot_product / (norm_vec1 * norm_vec2)

def get_recommendations(fileinfo, pastfiles):
    cleaned_files = clean_files(pastfiles)
    vocabulary = list(set([term for pastfile in cleaned_files for term in pastfile.split()]))
    tfidf_matrix = []

    for id, pastfile in pastfiles.items():
        tf_idf_vector = tf_idf_vectorize(pastfile, vocabulary, cleaned_files)
        tfidf_matrix.append((id, tf_idf_vector))

    fileinfo_tfidf = tf_idf_vectorize(fileinfo, vocabulary, cleaned_files)
    similarities = []
    for _, doc_tfidf in tfidf_matrix:
        similarities.append(cosine_similarity(fileinfo_tfidf, doc_tfidf))

    sorted_indices = np.argsort(similarities)[::-1]

    recommendations = [(tfidf_matrix[i][0], similarities[i]) for i in sorted_indices]
    return recommendations
