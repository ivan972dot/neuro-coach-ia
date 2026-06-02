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

    analysis= f"analyse logique: l'utilisateur dit {user_input}"

    if "python" in clean_input:
        analysis = "Analyse logique : la demande concerne Python. Il faut découper le problème en étapes simples."
        

    if "anglais" in clean_input:
        analysis = "Analyse logique : La demande concerne l' apprentissage de l'anglais"
        

    if "projet"in clean_input:
        analysis = "Analyse logique : la demande concerne l'organisation ou la construction."

    

    return analysis

def right_agent(user_input):

    clean_input = user_input.lower().strip()

    analysis= f"analyse causale: l'utilisateur dit {user_input}"
    
    if "bloque" in clean_input:
        analysis=" Le blocage peut venir d'une difficulté trop élevée"

    
    if "fatigue" in clean_input:
        analysis=" la fatigue peut réduire la concentration : préconisation d'une séance légère"

    if "motivation" in clean_input:
        analysis= " La baisse de motivation peut venir d'un objectif trop grand ou un manque de victoire rapide"


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





while True:
    
    user_input= input("YOU:  " )

    if user_input.lower().strip() == "stop":
         print("fin de conversation")
         break

    if user_input.lower().strip() == "memory":
            print(memory)
            continue

  
    left_analysis= left_agent(user_input)
    right_analysis= right_agent(user_input)
    final_response= central_agent(user_input,left_analysis,right_analysis)

    print(final_response)
    save_memory(user_input,final_response,memory)



