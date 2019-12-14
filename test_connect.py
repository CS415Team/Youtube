import numpy as np 
from neo4j import GraphDatabase 





if __name__ == '__main__':

    uri = "bolt://localhost:7687"
    user = "neo4j"
    passw = "cpts415"

    #Connects to DB
    _driver = GraphDatabase.driver(uri, auth=(user, passw))
    
    #query = 'MATCH (video:Video) \n Return video LIMIT 5;'

    #pageRank Top k
    k = '5'
    query1 = 'CALL algo.pageRank.stream(\'Video\', NULL, {iterations:20, dampingFactor:0.85})\nYIELD nodeId, score\nRETURN algo.asNode(nodeId).id AS page, score\nORDER BY score DESC LIMIT ' + k + ';'


  
    #Average In Degree of all Videos
    query2 = 'MATCH (video:Video)<-[r]-(video1:Video)\nWITH count(r) as num\nRETURN avg(num) as avgIN;'

    #Max In Degree of all Videos
    query3 = 'MATCH (video:Video)<-[r]-(video1:Video)\nWITH count(r) as num\nRETURN max(num) as maxIN;'

    #Min In Degree of all Videos
    query4 = 'MATCH (video:Video)<-[r]-(video1:Video)\nWITH count(r) as num\nRETURN min(num) as minIN;'

    #Average Out Degree of all Videos
    query5 = 'MATCH (video:Video)-[r]->(video1:Video)\nWITH count(r) as num\nRETURN avg(num) as avgOUT;'

    #Max Out Degree of all Videos
    query6 = 'MATCH (video:Video)-[r]->(video1:Video)\nWITH count(r) as num\nRETURN max(num) as maxOUT;'

    query7 = 'MATCH (video:Video)-[r]->(video1:Video)\nWITH count(r) as num\nRETURN min(num) as minOUT;'

    #pageRank Bottom
    query8 = 'CALL algo.pageRank.stream(\'Video\', NULL, {iterations:20, dampingFactor:0.85})\nYIELD nodeId, score\nRETURN algo.asNode(nodeId).id AS page, score\nORDER BY score ASC LIMIT ' + k + ';'


    #In Degree - particular node
    vidid = "\"h6Ghupxbj9g\""
    query9 = 'MATCH (video:Video {id:' + vidid + '})<-[r]-(video1:Video)\nRETURN video.id, r, video1 AS in LIMIT 50;'

    #Out Degree - particular node
    query10 = 'MATCH (video:Video {id:' + vidid + '})-[r]->(video1:Video)\nRETURN video.id, r, video1 AS out LIMIT 20;'



    with _driver.session() as session:
        with session.begin_transaction() as tx:
            results = (tx.run(query3))
        session.close()

    
        #THIS SHIT BELOW FORMATS

        ''' Uncomment for pageRank  '''
        # col1 = []
        # col2 = []

        # for i in results:
        #     col1.append(i[0])
        #     col2.append(i[1])

        # col1 = np.array(col1)
        # col2 = np.array(col2)
        # l = col1.shape[0]
        
        # col1 = col1.reshape((l,1))
        # col2 = col2.reshape((l,1))
        
        # newdf = np.hstack((col1, col2))


        ''' IN and OUT Degrees '''

        #results is the value you want 

    


    # for i in newdf:
    #     print(i[1])
    #     c = input()
            
            

