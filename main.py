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



debug_mode = False

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
    save_memory(user_input,final_response,memory)



