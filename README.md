To: "Pierre-Julien Bringer" <pierre-julien.bringer@polytechnique.edu>
Hello,
Je t'envoie la magouilleuse.
Le long mail qui suit aurait plus sa place sur le wikix, mais bon, n'hésite
pas à l'y placer toi même.
Voilà, amuse toi bien.
++
Boris
PS : dis moi quand tu veux me voir pour la sécurité.
PS2 : Le mail en question
Petite description :
Utilisation : ./MagApp.py < test.txt
Format du fichier :
Consulter les exemples. Dans les grandes lignes :
* Une ligne par candidat, un seul mot pour son nom.
* Un saut de ligne ( il y a possiblité de ne rien mettre je
crois... )
* Une ligne par candidature, un mot pour le nom, un mot pour le
nombre de places en décimal.
* Un saut de ligne
* Les voeux: le nom du mec, puis une liste de candidatures dans
l'ordre. Les candidatures à égalité peuvent être séparées par des "="
* Un saut de ligne
b* Une liste d'incapacités au même format ( sans les "=", bien sûr
).
Construction du programme :
Magouilleuse.py contient une classe de solveur "munkres". Ce module
doit être préalablement installé avec easy_install si ma mémoire fonctionne.
Le travail fait là dedans est d'implémenter la
construction de la matrice de poids à partir de collections de choix,
d'incapacités et d'égalités
et à partir de la définition de la fonction
d'utilité, puis d'appeler le solveur.
MagIO.py : fait quelques pré-traitements et error checks, avec
aussi construction des collections dont on parle plus haut.
MagApp.py : lit un fichier et lance la magouilleuse dessus. Les
résultats sont imprimés en sortie.
Tests : tout cela a été testé sur des exemples simples, les perfs sont
correctes ( n^3 ). L'optimisation psyco est utilisée si dispo je crois.
Améliorations possibles :
Fonction d'utilité : pour l'instant, on a une fonction qui prend les
voeux dans l'ordre décroissant, et :
compte = 0
à haque voeu, on donne en poids "compte"^2 et :
compte += ( nb de places / popularité en nb de 1ere demandes )
On a donc une courbe qui est strictement croissante. Les égalités
sont implémentées par une passe
supplémentaire sur la matrice qui ramène tous les voeux "égaux"
au "compte" le plus faible ( si Terre et Air étaien
égaux dans la liste, et attribués à 11 et 17, les deux reviennent à
17 ).
Améliorations possibles via la théorie des jeux... peut-être.
Attention, c'est une fonction auquel j'ai déjà pas mal réléchi,
ne la changez pas sans faire de même !
Choix dans le temps : à Normale, on dispose de jetons à placer
globalement sur tous les magouillages réunis. On les place sur le
magouillage qui nous importe le plus, si les choix nous indiffèrent, on ne
met pas de jetons. On pourrait appeler ça des "points fist". C'est du même
ordre d'idées que les "=" entre les choix. Cela disymétrise beaucoup le
problème et satisfait beaucoup de gens. En général le pire arrive quand tout
le monde a la même liste de veux. Plus généralement, des systèmes de
pondération plus fins sont aussi à étudier, le principal problème étant
qu'il est extrêmement difficile d'éviter les surcharges d'intérêt sur le
premier choix par exemple, qui sont indésirables ( un bon critère je pense
est de garder une borne à la pente de "compte", comme expliqué plus bas ).
Défense contre les attaques :
* type "blocage marine" c'est ok.
* Intuitivement, si on connait précisément la popularité des
choix, on peut arriver
à avoir le voeu qu'on souhaite en :
* évaluant le rang d'attribution moyen.
* Maximisant la pente de la fonction d'utilité ( c'est à
dire de "compte" ) de 0 à ce "rang d'attribution moyen"+"marge de sécurité"
( ici la conaissance de la popularité intervient )
On divise par la popularité précisément pour atténuer ce
phénomène ( le pari est que les choix connus comme populaires sont ceux qui
sont très populaires, les autres ne sont pas connus comme tels ). Placer
des "=" oblige en quelque sorte à jouer le jeu, car le relachement de
contraintes qu'ils donnent au solveur garantit plus de satisfaction au
candidat qu'une enquête sur la popularité. Il aura ainsi un moyen d'ajuster
son choix et d'y passer du temps, sans pour autant chercher à casser le
système.
Propagande : Il faut crier haut et fort que le système résiste aux
blocages, et qu'il faut passer beaucoup de temps à trier et égaliser
finement ses candidatures. Il ne faut pas hésiter à rajouter des jetons
bidule ou machin pour occuper les gens, même si ça ne sert à rien, du moment
que c'est individuel et non basé sur les choix des autres. Avec ça, tout le
monde donnera ses vrais choix, et non le résultat d'un calcul obscur pour
faire exploser le système.
Interface: de ce côté là, tout est à faire.
Packaging : ...
