import pickle
import numpy as np
import pandas as pd

def main():
    with open('link_tracker_wikipedia_crawl_with_link_tracker.pkl', 'rb') as file:
        #Dataframe of all the links
        df = pickle.load(file)

    #Normalize URL and Outlinks
    df['normalizedURL'] = df['url'].apply(normalization)
    df['normalizedOutlinks'] = df['outlinks'].apply(lambda links: {normalization(link) for link in links} if isinstance(links, (set, list)) else set())

    # Filter out any None or junk normalized URLs
    df = df[df['normalizedURL'].apply(validNodes)]

    #Build node list
    nodes = set(df['normalizedURL'])
    for outlinks in df['normalizedOutlinks']:
        nodes.update({link for link in outlinks if validNodes(link)})

    #Sort list of unique page names
    nodes = sorted(nodes)
    nodeIndex = {page: i for i, page in enumerate(nodes)}

    #Create empty adj. matrix
    n = len(nodes)
    adjMatrix = np.zeros((n, n), dtype=int)

    #Fill in matrix with edges
    for _, row in df.iterrows():
        source = row['normalizedURL']
        sourceIDX = nodeIndex.get(source)

        for target in row['normalizedOutlinks']:
            if target in nodeIndex:
                targetIDX = nodeIndex[target]
                adjMatrix[sourceIDX, targetIDX] = 1

    # Convert to DataFrame for PageRank input
    adjDF = pd.DataFrame(adjMatrix, index=nodes, columns=nodes)

    #Run pagerank
    ranks = page_rank(adjDF)

    rankDF = pd.DataFrame({
        'page': adjDF.index,
        'rank': ranks
    }).sort_values(by='rank', ascending=False)
    print(rankDF)
    rankDF.to_csv('pagerank_results.csv', index=False)

def normalization(url):
    if not isinstance(url, str):
        return None
    url = url.strip()

    #Keep only the part after /wiki/
    if '/wiki/' in url:
        return url.split('/wiki/')[-1].split('#')[0].split('?')[0].replace('.html', '')

    #Handle w/index.php?title=Article_Name&oldid=...
    if '/w/index.php?' in url and 'title=' in url:
        return url.split('title=')[-1].split('&')[0].replace('.html', '')

    #Drop protocols and prefixes for partial URLs
    if '://' in url:
        return url.split('/')[-1].replace('.html', '')

    #Trims everything else
    return url.replace('.html', '')

def validNodes(name):
    if not name:
        return False
    if name.startswith('index.php?'):
        return False
    if name.startswith('User:') or name.startswith('Special:'):
        return False
    return True

def page_rank(adj, tpprob = 0.15, maxiterations = 100, tol=1e-6):
    A = adj.values.astype(float)
    n = A.shape[0]

    #Normalize columns to handle dangling nodes
    columnSums = A.sum(axis=0)
    columnSums[columnSums == 0] = 1  # avoid division by zero for dangling nodes
    A = A / columnSums

    rank = np.ones(n)/n

    for i in range(maxiterations):
        newRank = tpprob / n + (1 - tpprob) * A.dot(rank)

        #Check for convergence
        if np.allclose(rank, newRank, atol=tol):
            break
        rank = newRank

    return rank

if __name__ == "__main__":
    main()