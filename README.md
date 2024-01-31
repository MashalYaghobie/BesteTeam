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
Het A-star algoritme is het derde en laatste algoritme die we hebben geimplementeerd. Dit algoritme werkt goed voor het Rush Hour probleem, omdat het op een efficiente manier met gebruik van heuristieken het kortste pad zoekt van de beginconfiguratie naar de oplossing. Kort samengevat werkt dit algoritme stapsgewijs als volgt:
1. Het algoritme begint met de beginconfiguratie van het bord.
2. 

## Aan de slag

### Vereisten

We hebben de gehele case uitgewerkt in Python (versie op moment van schrijven is 3.9.18). In requirements.txt staan verdere opmerkingen omtrent welke packages er nodig zijn om alle code succesvol te kunnen runnen. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

### Gebruik

De file genaamd rush_hour.py bevat alle code voor het spelen van een Rush Hour game. Deze file kan gebruikt worden om zelf stap voor stap een Rush Hour bord op te lossen. De file kan met deze instructie gespeeld worden:
```
python rush_hour.py
```

Hierna zal gevraagd worden welk bord je wilt spelen en kunnen zetten op de volgende manier ingegeven worden <naam_voertuig afstand>, bijvoorbeeld A 1.
Als deze move niet mogelijk is zal de pop-up opnieuw verschijnen. Na elke zet wordt het nieuwe bord gedisplayd.

De algoritmes zijn eenvoudiger te runnen. Het enige wat voor deze files gedaan moet worden is voor bijvoorbeeld het Depth-First Search algoritme:
```
python dfs.py
```

Hierna zal gevraagd worden welk bord gespeeld moet worden en vervolgens zal het algoritme zijn werk doen.


### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
  - **/code/game**: bevat de algemene file welke gebruikt kan worden om zelf een rush hour bord te spelen
  - **/code/visualisation**: bevat de code voor de visualisatie
- **/gameboards**: bevat de verschillende aangeleverde gameboards voor deze case
- **/plots**: bevat plots die we gegenereerd hebben gedurende deze case

## Auteurs
  - Mashal Yaghobie
  - Morris van der Hulst
  - Bram van de Weert
