import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

tfidf = TfidfVectorizer(stop_words='english')
pd.set_option('display.max_columns', 24)

df1 = pd.read_csv('tmdb_5000_credits.csv')  # movie_id, title, cast, crew
df2 = pd.read_csv('tmdb_5000_movies.csv')  # budget, title, id, keywords, etc
df1.columns = ['id', 'title', 'cast', 'crew']
df1[['id', 'cast', 'crew']]
df2 = df2.merge(df1[['id', 'cast', 'crew']], on='id')

# print(df2['overview'].isnull().values.any())
df2['overview'] = df2['overview'].fillna('')  # preprocessing
tfidf_matrix = tfidf.fit_transform(df2['overview'])  # vectorization
# print(tfidf_matrix.shape)

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)  # cosine similarity
# print(cosine_sim.shape)

##title을 넣으면 그에 맞는 index 번호를 반환할수있게 함 == title이 index가 됨
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()  # Series=1차원 배열

# print(indices.head(1))


##영화의 제목을 입력받으면 코사인 유사도를 통해 가장 유사도가 높은 상위 10개 영화 목록 반환##
def get_recomm(title, cosine_sim=cosine_sim):
    idx = indices[title]
    # cosine_sim 매트릭스에서 idx에 해당하는 데이터를 (index, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))  ##enumerate returns (index, element)
    # sim_scores의 [1]번째 값(=유사도)으로 내림차순 정렬하기
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 자기 자신 제외 10개
    sim_scores = sim_scores[1:11]
    # 영화 index 정보 추출
    movie_indices = [i[0] for i in sim_scores]
    # index 통해 제목 추출
    return df2['title'].iloc[movie_indices]

# print(get_recomm('The Avengers'))
