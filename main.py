import json
import os

memory=[]



def load_memory():
    try:
      with open("memory.json","r", encoding='utf-8') as file:
          donnees = json.load(file)
          return donnees
      
    except:
        return []


memory = load_memory()


def load_rules ():
    try:
        with open("rules.json","r", encoding= 'utf-8') as file:
            donnees = json.load(file)
        return donnees

    except:
        return []

memory = load_memory()
rules = load_rules()




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

    causal_patterns = rules["causal_patterns"]
    
    analysis = "Analyse causale générale : aucune cause précise détectée."

    for _ , data in causal_patterns.items():

        keywords = data["keywords"]

        category_analysis = data["analysis"]

        if any (keyword in clean_input for keyword in keywords):
            analysis = category_analysis

    return analysis
    
    
def memory_agent(user_input, memory):
    
    if memory == []:
        memory_analysis = "Mémoire : aucun historique disponible"
    else:
        python_count= 0
        anglais_count = 0
        blocage_count = 0
        fatigue_count = 0
        
        for exchange in memory:
            
            user_message = exchange["user"]
            user_message = user_message.lower()
    
            if "python" in user_message:
                python_count+= 1

            if "anglais" in user_message:
                anglais_count+= 1

            if "bloque" in user_message or "blocage" in user_message or "bloqué" in user_message:
                blocage_count += 1

            if "fatigue" in user_message:
                fatigue_count += 1


        if python_count > anglais_count :
         dominant_topic ="python"


        elif anglais_count > python_count:
         dominant_topic = "Anglais"


        else:
         dominant_topic = "Aucun sujet dominant" 


        if blocage_count > fatigue_count:
            probleme_recurrent = "blocage"
        

        elif fatigue_count > blocage_count :
            probleme_recurrent = "fatigue"
        

        else:
            probleme_recurrent = "aucun sujet dominant"











        memory_analysis = f"il existe déjà {len(memory)} échanges enregistrés. Python revient {python_count} fois. Anglais revient {anglais_count} fois . Blocage revient {blocage_count} fois. Fatigue revient {fatigue_count} fois. Sujet dominant : {dominant_topic} . Problème récurrent : {probleme_recurrent}."

    return memory_analysis






def central_agent(user_input,left_analysis,right_analysis,memory_analysis, debug_mode):

    clean_left = left_analysis.lower().strip()
    clean_right = right_analysis.lower().strip()
    clean_memory = memory_analysis.lower().strip()
    conclusion_immediate = "Conclusion immédiate : je  propose une action adaptée au message actuel"
    strategie_long_terme = " Stratégie long terme : aucun shéma récurrent fort détecté pour l'instant."
    mini_action = " Choisis une petite action simple et fais-la maintenant"
    action_rules = rules["action_rules"]
    memory_rules = rules["memory_rules"]
    decision_rules = rules["decision_rules"]
   

    for rule in action_rules:
        if rule["left"] in clean_left and rule["right"] in clean_right:
            mini_action = rule["action"]


    for rule in decision_rules:  
        if rule["left"] in clean_left and rule["right"] in clean_right:
            conclusion_immediate = rule["conclusion"]


    for rule in memory_rules:
        if rule["memory_keywords"] in clean_memory :
            strategie_long_terme = rule["conclusion"]

    if debug_mode:
        final_response = f"""
    
     Je comprends ta demande : 
         {user_input}


    Analyse logique :
        {left_analysis}

     Analyse causale :   
    {right_analysis}

    mémoire :
    {memory_analysis}

    Action immédiate :
    {conclusion_immediate}

    Stratégie long terme :
    {strategie_long_terme}

    Mini-action maintenant :
    {mini_action}

   
    """
    else:
        final_response = f""" Je comprends ta situation
        
        Action immédiate :
        {conclusion_immediate}

        Stratégie long terme : 
        {strategie_long_terme}

        Mini_action maintenant :
        {mini_action}
        
        """
    
    return final_response



def save_memory(user_input,final_response,memory):
    exchange= {
     "user": user_input,
        "assistant": final_response
     }
    memory.append(exchange)

    with open ("memory.json",'w') as file:
         json.dump(memory,file)



def save_backup(memory):
    with open("memory_backup.json",'w', encoding= "utf8") as file:
        json.dump(memory,file,indent=4,ensure_ascii=False)
        print("Sauvegarde créée")



def show_memory(memory):

    if memory==[]:
        print("Aucun échange en mémoire")
        return   
    for exchange in memory:
        print( " Utilisateur......: " + exchange["user"])
        print("Assistant ......: " + exchange["assistant"])

    

def clear_memory(memory):
      confirmation = input("Confirmer suppression mémoire ? oui/non :  ").lower().strip()

      if confirmation == "oui":
            save_backup(memory)
            memory.clear()
            with open("memory.json", "w",encoding="utf8") as file:
                json.dump(memory,file,indent=4,ensure_ascii=False)
            print("Mémoire effacée")
      else:
            print("Suppression annulée")


def restore_memory():

    try :
        with open("memory_backup.json",'r',encoding='utf8') as file:
            backup = json.load(file)
            
    except:
            print("Aucune sauvegarde trouvée.")
            return []

    with open("memory.json",'w', encoding="utf8") as file:
            json.dump(backup, file, indent=4, ensure_ascii=False)


    print("Mémoire restaurée")
    return backup



def show_rules(rules):
    
    if  not rules :
        print("Aucune règle chargée")
    else:
        print("=== Règles disponibles ===")
        for categories in rules:
            nombre = len(rules[categories])
            if nombre == 1 :
                mot ="règle"
            else: 
                mot ="règles"

            print(f"{categories} : { nombre}  {mot}")


def show_status(memory,rules,debug_mode):

    if memory:
        print("Mémoire chargée : oui ")
        
    else:
        print("Mémoire chargée : non")


    print(f"Nombre d'échanges : {len(memory)}")

    if rules:

        print("Règles chargées : oui ")

    else:

        print("Règle chargées : non")

    print(f"Catégories de règles : {len(rules)}")

    print (f"Mode debug : {debug_mode}")





def show_help():
    print("=== Commandes disponible ===")
    print ("stop : arrêt du programme.")
    print("memory : affiche la mémoire.")
    print("clear_memory : effacer la mémoire.")
    print("show_rules : afficher  les catégories de règles.")
    print("status : afficher l'état du coach.")
    print("help : afficher cette aide.")    
    print("save_backup : mémoire suvegardée")



def export_status(memory, rules, debug_mode):

         with open('status.txt','w',encoding='utf8') as file:

            file.write("=== NeuroCoach Status ===\n")

            if memory :
                file.write("Mémoire chargée : oui\n")
                file.write(f" Nombre d'échanges : {len(memory)}\n")

            else:
                file.write("Mémoire chargée : non\n")

            if rules:  
                file.write("Règles chargées : oui\n") 
                file.write (f" Catégories de règles : {len(rules)}\n")

                file.write("=== Catégories de règles ===\n")
                for categorie in rules:
                    nombre = len(rules[categorie])
                    if nombre == 1:
                        mot = "règle"
                    else:
                        mot = "règles" 

                    file.write (f"{categorie} : {nombre} {mot}\n")

            else:
                file.write("Règles chargées : non \n")


            file.write(f" Mode debug : {debug_mode}\n")
         print("Status exporté dans status.txt")

        
        






def show_categories(rules):
    categorie = input("categorie : ").lower().strip()

    if categorie in rules:
        print(categorie)
        if categorie == "action_rules":
            print("left + right + action")
            for rule  in rules[categorie]:
                print (f"{rule['left']} + {rule['right']} : {rule['action']}")
        elif categorie == "causal_patterns":
            for name, data in rules["causal_patterns"].items():
                keywords_text = ", ".join(data["keywords"])
                print (name)
                print (f"keywords :  {keywords_text}")
                print (f"analysis : data['analysis']")
        elif categorie == "decision_rules":
            for rule in rules["decision_rules"]:
                print(f"{rule['left']} + {rule['right']} : {rule['conclusion']}")

        elif categorie == "memory_rules":
            for  rule in rules["memory_rules"]:
                print(f"keywords : {rule['memory_keywords']}")
                print(f"conclusion : {rule['conclusion']}")
        else : 
          print("Affichage détaillé pas encore disponible pour cette catégorie.")  
                   
    else:

        print("catégorie inconnue")




debug_mode = False

while True:
    
    user_input= input("YOU:  " )
    clean_input = user_input.lower().strip()

    if clean_input == "stop":
        print("fin de conversation")
        break

    if clean_input == "memory":
        show_memory(memory)
        continue
    if clean_input== "clear_memory":
        clear_memory(memory)
        continue

    if clean_input == "show_rules":
        show_rules(rules)
        continue
    
    if clean_input  == "status":
        show_status(memory,rules,debug_mode)
        continue

    if clean_input == "help":
        show_help()
        continue
    
    if clean_input == "categorie":
        show_categories(rules)
        continue

    if clean_input == "reload_rules":
        rules = load_rules()
        print("Règles rechargées")
        continue

    if clean_input == "reload_memory":
        memory = load_memory()
        print("Mémoire rechargée")
        continue

    if clean_input == "clear_screen":
        os.system("cls")
        continue

    
    if clean_input =="save_backup":
        save_backup(memory)
        continue

    

    if clean_input =="restore_memory":
        memory = restore_memory()
        continue

    if clean_input =="export_status":
        export_status(memory,rules,debug_mode)
        continue


    left_analysis= left_agent(user_input)
    right_analysis= right_agent(user_input)
    memory_analysis= memory_agent(user_input, memory)
    final_response= central_agent(user_input,left_analysis,right_analysis,memory_analysis,debug_mode)

    print(final_response)
    save_memory(user_input,final_response,memory)



