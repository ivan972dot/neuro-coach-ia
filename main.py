import json

memory=[]



def load_memory():
    try:
      with open("memory.json","r", encoding='utf-8') as file:
          donnees = json.load(file)
          return donnees
      
    except:
        return []


memory = load_memory()


def left_agent(user_input):

    clean_input= user_input.lower().strip()

    logical_patterns = {
        "python":{
            "keywords": ["python","code","fonction", "boucle"],
            "analysis":"La demande concerne Python. Il faut découper le problème en étapes simples."
        },

        "anglais":{
            "keywords": ["anglais","english","speaking","shadowing"],
            "analysis": "La demande concerne l’apprentissage de l’anglais."
        },

        "projet":{
            "keywords":["projet","application","construire","idée"],
            "analysis": "La demande concerne l’organisation ou la construction d’un projet."

        }
    }

    analysis= "La demande doit être clarifié et structurée."

    for _ , data in logical_patterns.items():
        keywords = data["keywords"]
        category_analyse = data["analysis"]

        if any (keyword in clean_input for keyword in keywords):
            analysis = category_analyse

    return analysis

def right_agent(user_input):

    clean_input = user_input.lower().strip()
    causal_patterns = {
        "blocage" :{
            "keywords":["bloque", "difficulté", "comprend pas" ],
            "analysis": "Le  blocage peut venir d'une difficulté trop élévéé."
        },

        "fatigue" :{
            "keywords": ["fatigue","épuisé", "crevé"],
            "analysis": "La fatigue peut réduire la concentration."
        },

        "motivation" :{
            "keywords": ["motivation basse", "pas motivé", "motivation"],
            "analysis":"La baisse de motivation peut venir d'un objectif trop grand ou un manque de victoire rapide."
        },

        "stress" :{
            "keywords": [" stressé","angoissé","tendu", " nerveux"],
            "analysis":"Le stress peut venir d'une surcharge mentale ou d'une pression forte."

        },
        "peur" :{
            "keywords": ["peur"," échouer", "pas confiance", ],
            "analysis":"La peur peut venir de la crainte de l'échec ou du jugement."
        }
}
    
    for _ , data in causal_patterns.items():

        keywords = data["keywords"]

        category_analysis = data["analysis"]

        if any (  keyword in clean_input for keyword in keywords):
            analysis = category_analysis

    return analysis
    
    




def central_agent(user_input,left_analysis,right_analysis):

    clean_left = left_analysis.lower().strip()
    clean_right = right_analysis.lower().strip()
    conclusion = "phrase generale : je combine les deux analyses pour proposer une action adaptée"

    if "python" in clean_left and "blocage" in clean_right:
       conclusion = " on découpe le problème en petite étapes"

    if "anglais"in clean_left and "fatigue" in clean_right:
        conclusion = "on peut  faire une séance courte : de l'écoute active + shadowing"

    if "python" in clean_left and "motivation" in clean_right:
        conclusion = "on créer une  mini-victoire rapide en python"
     
    final_response = f"""
    
        Message utilisateur:  {user_input}

        {left_analysis}

        
    {right_analysis}

    conclusion finale : {conclusion}"""

    
    return final_response



def save_memory(user_input,final_response,memory):
    exchange= {
     "user": user_input,
        "assistant": final_response
     }
    memory.append(exchange)

    with open ("memory.json",'w') as file:
         json.dump(memory,file)




def show_memory(memory):

    if memory==[]:
        print("Aucun échange en mémoire")
        return   
    for exchange in memory:
        print( " Utilisateur......: " + exchange["user"])
        print("Assistant ......: " + exchange["assistant"])

    

def clear_memory(memory):
    memory.clear()
    with open("memory.json", "w") as file:
      json.dump(memory,file)
  





while True:
    
    user_input= input("YOU:  " )

    if user_input.lower().strip() == "stop":
         print("fin de conversation")
         break

    if user_input.lower().strip() == "memory":
            show_memory(memory)
            continue
    if user_input.lower().strip()== "clear_memory":
            clear_memory(memory)
            continue

  
    left_analysis= left_agent(user_input)
    right_analysis= right_agent(user_input)
    final_response= central_agent(user_input,left_analysis,right_analysis)

    print(final_response)
    save_memory(user_input,final_response,memory)



