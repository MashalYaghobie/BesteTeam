# RushHour

In deze case is het de opdracht om verschillende borden van het Rush Hour spel op te lossen. Dit is normaal gesproken een fysiek bord van 6x6 met verschillende indelingen van auto's en vrachtwagens op het bord, welke horizontaal of verticaal staan georienteerd. Voor een mens kan het lastig zijn en veel tijd in beslag nemen om zulke borden op te lossen, zeker wanneer een bord een omvang heeft van 9x9 of zelfs 12x12. Daarom is het doel voor deze case om met verschillende algoritmes te proberen om verschillende indelingen van Rush Hour borden op te lossen in zo min mogelijk zetten. Het oplossen houdt dan ook in om de rode auto naar de uitgang te brengen door een pad voor deze auto vrij te maken.

## Algoritmes

Voor het oplossen van de Rush Hour case hebben we nagedacht over welke algoritmes we hier het best voor konden gebruiken. De eerste afweging werd gemaakt tussen het gebruiken van iteratieve of constructieve algoritmes. Gezien bij het Rush Hour probleem de volgorde ofwel sequentie van de zetten die gedaan wordt erg belangrijk is, hebben we gekozen om constructieve algoritmes gebruiken. We hebben uiteindelijk gekozen om een Breadth-First Search, Depth-First Search en A-star algoritme te implementeren. Onderstaand zullen we per algoritme toelichten waarom dit algoritme werkt voor onze casus en hoe we dit algoritme hebben toegepast.

### Breadth-First Search
Het Breadth-First Search algoritme (hierna: BFS) is het eerste algoritme die we hebben geimplementeerd. Dit algoritme werkt voor het Rush Hour probleem, omdat het systematisch alle mogelijke zetten vanaf de beginconfiguratie van het bord onderzoekt en zo het kortste pad vind van de beginconfiguratie naar de oplossing (als er een oplossing bestaat). Kort samengevat werkt dit algoritme stapsgewijs als volgt:
1. Het algoritme begint met de beginconfiguratie van het bord.
2. Het algoritme houdt een 'queue' bij met daarin alle verschillende opstellingen of 'states' van het bord dat het langs zal gaan.
3. Van alle states zal het algoritme alle mogelijke volgende states onderzoeken door een voertuig een stap te verplaatsen in een toegestane richting. Als dit een unieke staat is zal deze staat opgeslagen worden in onze queue.
4. Alle unieke bezochte staten worden dus bijgehouden om er voor te zorgen dat we een staat niet meerdere malen bezoeken.
5. Als het algoritme een pad heeft gevonden van de beginconfiguratie naar de oplossing dan geeft het algoritme het aantal moves en de eindconfiguratie van het bord.

### Depth-First Search
Het Depth-First Search algoritme (hierna: DFS) is het tweede algoritme die we hebben geimplementeerd. Dit algoritme werkt voor het Rush Hour probleem, omdat het systematisch door de gehele state space zoekt naar een oplossing. Het DFS algoritme is over het algemeen sneller dan het BFS algoritme maar leidt niet naar het kortste pad. Het geeft echter 'een' oplossing. Kort samengevat werkt dit algoritme stapsgewijs als volgt:
1. Het algoritme begint met de beginconfiguratie van het bord.
2. Het algoritme houdt een 'stack' bij met daarin alle configuraties van het bord dat het zal bezoeken.
3. Dit algoritme zoekt vanaf de huidige staat een nieuwe staat door het verplaatsen van een voertuig met een toegestane zet en het zal door blijven gaan met dit proces totdat het een staat vind waarin geen nieuwe zetten mogelijk zijn.
4. Ook dit algoritme houdt een set bij met de bezochte staten om geen staten meerdere malen tegen te komen.
5. Als het algoritme een pad heeft gevonden van de beginconfiguratie naar de oplossing dan geeft het algoritme het aantal moves en de eindconfiguratie van het bord.

### A-star
Het A-star algoritme is het derde en laatste algoritme die we hebben geimplementeerd. Dit algoritme werkt goed voor het Rush Hour probleem, omdat het op een efficiente manier met gebruik van heuristieken het kortste pad zoekt van de beginconfiguratie naar de oplossing. Het is als het ware een extensie van het Breadth-First Search algoritme. Kort samengevat werkt dit algoritme stapsgewijs als volgt:
1. Het algoritme begint met de beginconfiguratie van het bord.
2. Het algoritme houdt een 'queue' bij met daarin alle verschillende opstellingen of 'states' van het bord dat het langs zal gaan.
3. In tegenstelling tot het BFS algoritme, zal AStar niet langs alle states gaan d.m.v. een heuristische functie. De heuristisce functie plus de kostfunctie zijn de totale kosten. De state met de laagste totale kosten wordt gekozen.
4. Voor die state worden er gekeken naar alle mogelijke zetten en vervolgens wordt het toegevoegd aan de closed list. Dit om bij te houden welke state al bezocht is, zodat het niet meerdere keren wordt bezocht.
5. Dit wordt herhaald voor de volgende states totdat the goal state is gevonden. 
   
## Aan de slag

### Vereisten

We hebben de gehele case uitgewerkt in Python (versie op moment van schrijven is 3.9.18). We hebben verder geen bijzondere afhankelijkheden. We hebben voor de visualisatie de turtles library gebruikt, maar deze hoefden we niet te installeren daarom hebben we geen requirements.txt opgesteld.

### Gebruik

De file genaamd main.py bevat alle code voor het runnen van een van de algoritmes voor de Rush Hour game. De file kan met deze instructie gespeeld worden:
```
python main.py
```

Hierna zal gevraagd worden welk algoritme je wilt gebruiken en kan je vervolgens kiezen welk gameboard je wilt spelen.
Vervolgens zal het algoritme gaan runnen.

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
  - **/code/game**: bevat de algemene file welke gebruikt kan worden om zelf een rush hour bord te spelen
  - **/code/visualisation**: bevat de code voor de visualisatie
- **/gameboards**: bevat de verschillende aangeleverde gameboards voor deze case
- **/plots**: bevat plots die we gegenereerd hebben gedurende deze case

### Resultaten

De resultaten hebben we verzameld door met behulp van main.py alle algoritmes te runnen. Vervolgens hebben we deze resultaten opgeslagen en gebruikt om handmatig grafieken en plots te maken.
De gegevens die hierin zichtbaar zijn zijn echter goed te reproduceren door de algoritmes te runnen. De plots hebben we opgeslagen in de map /plots.

## Auteurs
  - Mashal Yaghobie
  - Morris van der Hulst
  - Bram van de Weert
