import json
import os

memory=[]


APP_VERSION = "1.0.0"

COMMANDS = [
        "stop",
        "memory",
        "clear_memory",
        "show_rules",
        "categorie",
        "status",
        "help" ,
        "reload_rules",
        "reload_memory",
        "clear_screen",
        "save_backup",
        "export_status",
        "restore_memory",
        "commands_count",
        "version"  
        
]


COMMAND_DESCRIPTIONS = {

     "stop": "arrêt du programme",
    "memory" : "afficher la mémoire",
    "clear_memory" : "nettoyage mémoire",
    "show_rules" : "affichage des règles",
     "categorie" : "afficher le détail d'une catégorie.",
     "status" : "afficher l'état du coach",
    "help" : "afficher la liste des commandes" ,
    "reload_rules" :"recharger rules.json",
    "reload_memory" : "recharger memory.json" ,
    "clear_screen" :"nettoyer le terminal" ,
     "save_backup" :"sauvegarder la mémoire" ,
     "export_status" :"exporte le status dans status.txt"  ,
     "restore_memory" :"restaurer la mémoire depuis la sauvegarde" ,
    "commands_count" : "compter les commandes disponibles",
    "version" : "version actuelle du coach"
 }





def show_version():
    print(f"NeuroCoach IA - version : {APP_VERSION}")



def load_memory():
    try:
      with open("memory.json","r", encoding='utf-8') as file:
          donnees = json.load(file)
          if not isinstance(donnees,list):
              return[]
          

      return donnees
    
      
    except FileNotFoundError as error:
        print("Fichier introuvable.")
        print(error)
        return []
    
    
    except json.JSONDecodeError as error:
        print("Fichier présent mais JSON mal écrit")
        print(error)
        return []
    
    
    except Exception as error:
        print("Erreur imprévue lors du chargement de la mémoire.")
        print(error)

        return []





def load_rules ():
    try:
        with open("rules.json","r", encoding= 'utf-8') as file:
            donnees = json.load(file)
        return donnees

    except FileNotFoundError as error:
        print("rules.json introuvable")
        print(error)
        return {}
    
    except  json.JSONDecodeError as error:
        print("rules.json existe, mais son contenu JSON est mal écrit.") 
        print(error)      
        return {}
    
    except Exception as error:
        print("Erreur imprévu lors du chargement des règles.")
        print(error)
        return {}



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

    causal_patterns = rules.get("causal_patterns", {})
    
    analysis = []
    for _ , data in causal_patterns.items():

        keywords = data["keywords"]

        category_analysis = data["analysis" ]

        if any (keyword in clean_input for keyword in keywords):
            analysis.append(category_analysis)
    
    if analysis ==[]: 
            return "analyse generale"
    else:
     return "\n".join(analysis)  

    
    
def memory_agent(user_input, memory):
    
        memory_count ={
            "python":0 ,
            "anglais" : 0 ,
            "fatigue" : 0,
            "blocage" : 0 

        }

        keyword_by_category = {

            "fatigue": ["fatigué","fatigue"],
           "blocage" : ["bloqué","blocage","bloque"] 
        
        }
           
        
        for exchange in memory:
            
            user_message = exchange["user"]
            user_message = user_message.lower()
    
            if "python" in user_message:
                memory_count["python"]+= 1

            if "anglais" in user_message:
                memory_count["anglais"]+= 1

    
            for categorie,liste_keywords in keyword_by_category.items():
                if any (keyword in user_message for keyword in liste_keywords): 
                     memory_count[categorie] += 1

        current_message = user_input.lower()
        if "python" in current_message:
            memory_count["python"]+= 1

        if "anglais" in current_message:
            memory_count["anglais"]+= 1

        for categorie,liste_keywords in keyword_by_category.items():
                          if any (keyword in current_message for keyword in liste_keywords): 
                               memory_count[categorie] += 1  

                     
        sujet_count = {
           "python": memory_count["python"],
           "anglais" : memory_count["anglais"]
    }

        if sujet_count["python"] == sujet_count["anglais"]:
            dominant_topic = "Aucun sujet dominant"
                
        else:
            dominant_topic = max(sujet_count, key= sujet_count.get)
                 
        if memory_count["blocage"]>= 2 and memory_count["fatigue"]>= 2:
            probleme_recurrent = "blocage et fatigue"

        elif  memory_count["blocage"] >= 2 :
            probleme_recurrent = "blocage "

        elif memory_count["fatigue"]>= 2 :
             probleme_recurrent = "fatigue"
        
        else:
             probleme_recurrent = " Aucun problème récurrent"


        memory_analysis = f"il existe déjà {len(memory)} échanges enregistrés. Python revient {memory_count['python']} fois. Anglais revient {memory_count['anglais']} fois . Blocage revient {memory_count['blocage']} fois. Fatigue revient {memory_count['fatigue']} fois. Sujet dominant : {dominant_topic} . Problème récurrent : {probleme_recurrent}."
         
        return memory_analysis






def central_agent(user_input,left_analysis,right_analysis,memory_analysis, debug_mode):

    clean_left = left_analysis.lower().strip()
    clean_right = right_analysis.lower().strip()
    clean_memory = memory_analysis.lower().strip()
    conclusion_immediate = "Conclusion immédiate : je  propose une action adaptée au message actuel"
    strategie_long_terme = " aucun schéma récurrent fort détecté pour l'instant."
    mini_action = " Choisis une petite action simple et fais-la maintenant"
    action_rules = rules.get("action_rules", [])
    memory_rules = rules.get("memory_rules", [])
    decision_rules = rules.get("decision_rules", [])
    priority_rules = rules.get("priority_rules", [])
    priority_found= False


    for rule in priority_rules:
            required_right_keyword = rule.get("right_all", [] )
    
            if required_right_keyword and all(keyword in clean_right for keyword in required_right_keyword):
                 conclusion_immediate = rule.get("conclusion")
                 mini_action = rule.get("action")
                 priority_found = True
                 break  



            if not priority_found :


                for rule in action_rules:
                    if rule.get("left", "left manquant") in clean_left and rule.get("right", "right manquant") in clean_right:
                         mini_action = rule.get("action", "action manquante")
                         break


                for rule in decision_rules:  
                     if rule.get("left", "left manquant") in clean_left and rule.get("right", "right manquant") in clean_right:
                        conclusion_immediate = rule.get("conclusion", "conclusion manquante")
                        break


    for rule in memory_rules:
        if rule.get("memory_keywords", "memory_keywords manquante")in clean_memory :
            strategie_long_terme = rule.get("conclusion", "conclusion manquante")
            break




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

        try :
            with open ("memory.json",'w', encoding='utf8') as file:
                json.dump(memory,file,ensure_ascii=False,indent=4)

                return True
            
            
        except TypeError as error:
            memory.pop()
            print(error)
            return False
        
        except FileNotFoundError as error:
            memory.pop()
            print(error)
            return False
        
        except Exception as error:
            memory.pop()
            print(error)
            return False
    

    

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
    print("=== Commandes disponibles ===")
    for command in COMMANDS:
        if command in COMMAND_DESCRIPTIONS:
            description = COMMAND_DESCRIPTIONS[command]
        else:
            description = "description non disponible."

        print (f"- {command} : {description}")



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
            for rule  in rules.get(categorie, []):
             print (f"{rule.get('left','left manquant')}+ {rule.get('right','right manquant')} : {rule.get('action','action manquant')}")

        elif categorie == "causal_patterns":
         for name, data in rules.get(categorie, {}).items():
                keywords_text = ", ".join(data.get("keywords", []))
                print (name)
                print (f"keywords :  {keywords_text}")
                print (f"analysis : {data.get('analysis','analysis manquant')}")

        elif categorie == "decision_rules":
            for rule in rules.get(categorie, []):
                print(f"{rule.get('left', 'left manquant')} + {rule.get('right', 'right manquant')} : {rule.get('conclusion','action manquante')}")

        elif categorie == "memory_rules":
            for  rule in rules.get(categorie, []):
                print(f"keywords : {rule.get('memory_keywords', 'memory_keywords manquant')}")
                print(f"conclusion : {rule.get('conclusion', 'conclusion manquante')}")
        else : 
          print("Affichage détaillé pas encore disponible pour cette catégorie.")  
                   
    else:

        print("catégorie inconnue")


def show_command_count():
   
    print(f"Nombre de commandes disponibles  : {len(COMMANDS)}")





def is_command(clean_input):

    return clean_input in COMMANDS



def reload_rules_command():
    new_rules = load_rules()
    print ("Règles chargées")
    return new_rules


def reload_memory_command():
    new_memory = load_memory()
    print("Mémoire rechargée")
    return new_memory



def handle_command(clean_input,memory,rules,debug_mode):

    simple_commands = {
    "help": show_help,
    "version": show_version,
    "commands_count":show_command_count,
    "clear_screen" : lambda: os.system('cls')
}
    
    context_command ={
        "status": lambda : show_status(memory, rules, debug_mode),
        "show_rules" : lambda : show_rules(rules),
        "memory": lambda : show_memory(memory),
        "categorie": lambda : show_categories(rules),
        "export_status": lambda : export_status(memory, rules, debug_mode),
        "save_backup": lambda : save_backup(memory),
         "clear_memory" : lambda : clear_memory(memory)
        
     }



    state_commands = {
        "reload_rules": reload_rules_command
        

    }


    memory_commands = {
        "reload_memory" : reload_memory_command,
        "restore_memory" : restore_memory
       
    }

    if clean_input in memory_commands:
         memory_function = memory_commands[clean_input]
         memory = memory_function()
         return True, memory, rules, False




    if clean_input in state_commands:
        state_function = state_commands[clean_input]
        rules = state_function()
        return True,memory, rules, False


    if clean_input in context_command:
        context_function = context_command[clean_input]
        context_function()
        return True, memory, rules, False


    if clean_input in simple_commands:
        command_function = simple_commands[clean_input]
        command_function()
        return True, memory, rules, False 


   
    
    if clean_input == "stop":
        print("fin de conversation")
        return True, memory, rules, True




    return False, memory, rules, False



debug_mode = True

while True:
    
    user_input= input("YOU:  " )
    clean_input = user_input.lower().strip()

    command_handled, memory, rules, should_stop = handle_command(clean_input, memory, rules, debug_mode)

    if should_stop:
        break

    if  command_handled:
     continue

    


    left_analysis= left_agent(user_input)
    right_analysis= right_agent(user_input)
    memory_analysis= memory_agent(user_input, memory)
    final_response= central_agent(user_input,left_analysis,right_analysis,memory_analysis,debug_mode)

    print(final_response)
    memory_result = save_memory(user_input,final_response,memory)
    if  not memory_result :
        print("l'échange n'a pas pu étre  sauvegardé")



